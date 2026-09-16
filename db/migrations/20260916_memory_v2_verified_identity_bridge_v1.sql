-- XiaoAi Memory v2 verified identity bridge v1
-- Fail-closed bridge from canonical live identity/session evidence into Memory v2.
-- Does not enable durable memory mode; durable_memory_mode remains controlled separately.

create or replace function memory_v2_private.ensure_verified_child_link(
  p_subject_id uuid,
  p_account_id uuid
)
returns boolean
language plpgsql
security definer
set search_path = pg_catalog, memory_v2_private
as $$
declare
  v_auth_user_id uuid;
  v_link_ok boolean;
begin
  if p_subject_id is null or p_account_id is null then
    return false;
  end if;

  select u.auth_user_id into v_auth_user_id
  from public.users u
  join public.companion_access ca
    on ca.user_id = u.id
   and ca.child_id = p_subject_id
   and ca.role = 'child'
   and ca.status = 'active'
   and ca.verified_at is not null
  where u.id = p_account_id
    and u.status = 'active'
    and u.auth_user_id is not null
    and exists (
      select 1
      from public.runtime_sessions rs
      join public.client_connections cc
        on cc.id = rs.client_connection_id
       and cc.child_id = p_subject_id
       and cc.user_id = p_account_id
       and cc.status = 'active'
      where rs.child_id = p_subject_id
        and rs.user_id = p_account_id
        and rs.status = 'active'
    )
  limit 1;

  if v_auth_user_id is null then
    return false;
  end if;

  if exists (
    select 1 from memory_v2_private.accounts a
    where a.provider = 'supabase_auth'
      and a.provider_user_id = v_auth_user_id::text
      and a.account_id <> p_account_id
  ) then
    return false;
  end if;

  insert into memory_v2_private.subjects(subject_id,status)
  values(p_subject_id,'active')
  on conflict(subject_id) do update
    set status='active', updated_at=now();

  insert into memory_v2_private.accounts(
    account_id,provider,provider_user_id,status,revoked_at
  ) values (
    p_account_id,'supabase_auth',v_auth_user_id::text,'active',null
  )
  on conflict(account_id) do update
    set status='active', revoked_at=null
  where memory_v2_private.accounts.provider='supabase_auth'
    and memory_v2_private.accounts.provider_user_id=excluded.provider_user_id;

  if not exists (
    select 1 from memory_v2_private.accounts a
    where a.account_id=p_account_id
      and a.provider='supabase_auth'
      and a.provider_user_id=v_auth_user_id::text
      and a.status='active'
      and a.revoked_at is null
  ) then
    return false;
  end if;

  insert into memory_v2_private.subject_account_links(
    subject_id,account_id,relationship_role,status,
    can_submit_child_pinned,can_request_correction,can_request_deletion,revoked_at
  ) values (
    p_subject_id,p_account_id,'child','active',true,false,false,null
  )
  on conflict(subject_id,account_id) do update
    set status='active',
        can_submit_child_pinned=true,
        revoked_at=null
  where memory_v2_private.subject_account_links.relationship_role='child';

  select exists(
    select 1 from memory_v2_private.subject_account_links l
    where l.subject_id=p_subject_id
      and l.account_id=p_account_id
      and l.relationship_role='child'
      and l.status='active'
      and l.can_submit_child_pinned=true
      and l.revoked_at is null
  ) into v_link_ok;

  return coalesce(v_link_ok,false);
end;
$$;

revoke all on function memory_v2_private.ensure_verified_child_link(uuid,uuid)
  from public, anon, authenticated, service_role;

create or replace function memory_v2_api.pin_child_memory(payload jsonb)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, memory_v2_private
as $$
declare
  v_mode text;
  v_subject_id uuid;
  v_account_id uuid;
  v_memory_id uuid;
  v_key text;
  v_conf numeric;
  v_summary text;
  v_link_ok boolean;
begin
  select flag_value into v_mode
  from memory_v2_private.runtime_flags
  where flag_key = 'durable_memory_mode';

  if coalesce(v_mode, 'off') <> 'child_pinned_only' then
    return jsonb_build_object('accepted', false, 'reason', 'durable_memory_gate_off');
  end if;

  if coalesce(payload->>'intent_class', '') <> 'long_term_memory_create' then
    return jsonb_build_object('accepted', false, 'reason', 'not_long_term_memory_create');
  end if;

  if coalesce(payload->>'source_type', '') <> 'child_direct' then
    return jsonb_build_object('accepted', false, 'reason', 'source_not_verified_child_direct');
  end if;

  if coalesce(payload->>'actor_role_resolved', '') <> 'child' then
    return jsonb_build_object('accepted', false, 'reason', 'actor_not_verified_child');
  end if;

  v_conf := coalesce((payload->>'intent_confidence')::numeric, 0);
  if v_conf < 0.85 then
    return jsonb_build_object('accepted', false, 'reason', 'intent_confidence_too_low');
  end if;

  v_key := btrim(coalesce(payload->>'idempotency_key', ''));
  if v_key = '' then
    return jsonb_build_object('accepted', false, 'reason', 'missing_idempotency_key');
  end if;

  v_summary := btrim(coalesce(payload->>'summary', ''));
  if v_summary = '' then
    return jsonb_build_object('accepted', false, 'reason', 'empty_summary');
  end if;

  if coalesce((payload->>'privacy_gate_passed')::boolean, false) is not true then
    return jsonb_build_object('accepted', false, 'reason', 'privacy_gate_not_passed');
  end if;
  if coalesce((payload->>'sensitivity_gate_passed')::boolean, false) is not true then
    return jsonb_build_object('accepted', false, 'reason', 'sensitivity_gate_not_passed');
  end if;
  if coalesce((payload->>'minimum_necessary_passed')::boolean, false) is not true then
    return jsonb_build_object('accepted', false, 'reason', 'minimum_necessary_gate_not_passed');
  end if;
  if coalesce((payload->>'visibility_gate_passed')::boolean, false) is not true then
    return jsonb_build_object('accepted', false, 'reason', 'visibility_gate_not_passed');
  end if;

  begin
    v_subject_id := (payload->>'subject_id')::uuid;
    v_account_id := (payload->>'actor_account_id')::uuid;
  exception when invalid_text_representation then
    return jsonb_build_object('accepted', false, 'reason', 'invalid_identifier');
  end;

  if not memory_v2_private.ensure_verified_child_link(v_subject_id,v_account_id) then
    return jsonb_build_object('accepted', false, 'reason', 'verified_child_identity_binding_required');
  end if;

  select exists(
    select 1
    from memory_v2_private.subject_account_links l
    where l.subject_id = v_subject_id
      and l.account_id = v_account_id
      and l.relationship_role = 'child'
      and l.status = 'active'
      and l.can_submit_child_pinned = true
      and l.revoked_at is null
  ) into v_link_ok;

  if not v_link_ok then
    return jsonb_build_object('accepted', false, 'reason', 'subject_account_link_not_authorized');
  end if;

  select memory_id into v_memory_id
  from memory_v2_private.idempotency_keys
  where idempotency_key = v_key
    and operation = 'pin_child_memory';

  if v_memory_id is not null then
    return jsonb_build_object('accepted', true, 'reason', 'idempotent_replay', 'memory_id', v_memory_id);
  end if;

  insert into memory_v2_private.memories(
    subject_id, summary, category, source_type, confidence, sensitivity,
    status, retention_class, pinned_by_child, disclosure_scope,
    proactive_surface_allowed, reasoning_use_allowed, on_request_allowed
  ) values (
    v_subject_id,v_summary,coalesce(payload->>'category','event'),'child_direct',v_conf,
    coalesce(payload->>'sensitivity','low'),'active','child_pinned',true,
    coalesce(payload->>'disclosure_scope','subject_only'),false,true,true
  ) returning memory_id into v_memory_id;

  insert into memory_v2_private.revisions(
    memory_id,revision_number,summary,meaning_text,child_voice_quote,
    source_type,created_by_account_id
  ) values (
    v_memory_id,1,v_summary,payload->>'meaning_text',payload->>'child_voice_quote',
    'child_direct',v_account_id
  );

  insert into memory_v2_private.sources(
    memory_id,source_account_id,source_type,source_ref
  ) values (
    v_memory_id,v_account_id,'child_direct',payload->>'source_ref'
  );

  insert into memory_v2_private.idempotency_keys(idempotency_key,operation,memory_id)
  values(v_key,'pin_child_memory',v_memory_id);

  insert into memory_v2_private.audit_events(
    subject_id,memory_id,actor_account_id,action,decision,reason_code,metadata
  ) values (
    v_subject_id,v_memory_id,v_account_id,'pin_child_memory','accepted',
    'verified_child_direct_explicit_intent_policy_gates_passed',
    jsonb_build_object(
      'privacy_gate_passed',true,
      'sensitivity_gate_passed',true,
      'minimum_necessary_passed',true,
      'visibility_gate_passed',true,
      'identity_bridge','verified_live_child_session_v1'
    )
  );

  return jsonb_build_object('accepted',true,'reason','created','memory_id',v_memory_id);
end;
$$;

revoke all on function memory_v2_api.pin_child_memory(jsonb) from public, anon, authenticated;
grant execute on function memory_v2_api.pin_child_memory(jsonb) to service_role;
