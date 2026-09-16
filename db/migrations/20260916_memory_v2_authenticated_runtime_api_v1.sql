-- XiaoAi Memory v2 authenticated runtime API v1
-- Production-facing bridge from authenticated child runtime sessions into Memory v2.
-- Durable mode remains controlled by memory_v2_private.runtime_flags.

create or replace function public.request_child_pinned_memory_v2(
  p_child_id uuid,
  p_session_key text,
  p_user_utterance text,
  p_summary text,
  p_intent_class text,
  p_intent_confidence numeric,
  p_explicit_user_intent boolean,
  p_durable_value boolean,
  p_verified_or_explicit boolean,
  p_durable_storage_necessary boolean,
  p_memory_class text,
  p_sensitivity text,
  p_visibility_scope text,
  p_minimum_necessary boolean,
  p_idempotency_key text default null
)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog
as $$
declare
  a record;
  v_class text := upper(btrim(coalesce(p_memory_class,'')));
  v_sensitivity text := lower(btrim(coalesce(p_sensitivity,'')));
  v_visibility text := btrim(coalesce(p_visibility_scope,''));
  v_key text;
  v_visibility_ok boolean;
  v_sensitivity_ok boolean;
begin
  if p_child_id is null then
    return jsonb_build_object('accepted',false,'reason','child_id_required');
  end if;
  if btrim(coalesce(p_session_key,'')) = '' then
    return jsonb_build_object('accepted',false,'reason','session_key_required');
  end if;

  select * into a
  from public.resolve_memory_actor_evidence_shadow_v1(p_child_id,p_session_key)
  limit 1;

  if not coalesce(a.verified,false)
     or coalesce(a.actor_role_resolved,'') <> 'child'
     or coalesce(a.source_type,'') <> 'child_direct'
     or a.actor_account_id is null then
    return jsonb_build_object('accepted',false,'reason',coalesce(a.reason,'verified_child_identity_required'));
  end if;

  if coalesce(p_intent_class,'') <> 'long_term_memory_create' then
    return jsonb_build_object('accepted',false,'reason','not_long_term_memory_create');
  end if;
  if coalesce(p_explicit_user_intent,false) is not true then
    return jsonb_build_object('accepted',false,'reason','explicit_user_intent_required');
  end if;
  if btrim(coalesce(p_user_utterance,'')) = '' then
    return jsonb_build_object('accepted',false,'reason','original_user_utterance_required');
  end if;
  if btrim(coalesce(p_summary,'')) = '' then
    return jsonb_build_object('accepted',false,'reason','summary_required');
  end if;
  if coalesce(p_durable_value,false) is not true then
    return jsonb_build_object('accepted',false,'reason','durable_value_not_established');
  end if;
  if coalesce(p_verified_or_explicit,false) is not true then
    return jsonb_build_object('accepted',false,'reason','verification_not_established');
  end if;
  if coalesce(p_durable_storage_necessary,false) is not true then
    return jsonb_build_object('accepted',false,'reason','durable_storage_not_necessary');
  end if;
  if coalesce(p_intent_confidence,0) < 0.85 then
    return jsonb_build_object('accepted',false,'reason','intent_confidence_too_low');
  end if;

  v_visibility_ok := v_visibility in (
    'user_only','user_and_daughter','guardian_visible','guardian_summary_only',
    'safety_restricted','system_only_minimal'
  );

  if v_class in ('M3','M4') then
    v_sensitivity_ok := v_sensitivity in ('restricted','high');
    v_visibility_ok := v_visibility_ok and v_visibility in (
      'user_only','safety_restricted','system_only_minimal'
    );
  else
    v_sensitivity_ok := v_sensitivity in ('low','normal','moderate');
  end if;

  if not v_sensitivity_ok then
    return jsonb_build_object('accepted',false,'reason','sensitivity_gate_not_passed');
  end if;
  if coalesce(p_minimum_necessary,false) is not true then
    return jsonb_build_object('accepted',false,'reason','minimum_necessary_gate_not_passed');
  end if;
  if not v_visibility_ok then
    return jsonb_build_object('accepted',false,'reason','visibility_gate_not_passed');
  end if;

  v_key := nullif(btrim(coalesce(p_idempotency_key,'')),'');
  if v_key is null then
    v_key := encode(extensions.digest(
      concat_ws('|',p_child_id::text,a.actor_account_id::text,p_session_key,p_user_utterance,p_summary),
      'sha256'
    ),'hex');
  end if;

  return memory_v2_api.pin_child_memory(jsonb_build_object(
    'subject_id',p_child_id,
    'actor_account_id',a.actor_account_id,
    'actor_role_resolved','child',
    'intent_class','long_term_memory_create',
    'intent_confidence',p_intent_confidence,
    'source_type','child_direct',
    'summary',btrim(p_summary),
    'idempotency_key',v_key,
    'memory_class',v_class,
    'sensitivity',v_sensitivity,
    'disclosure_scope',v_visibility,
    'privacy_gate_passed',true,
    'sensitivity_gate_passed',true,
    'minimum_necessary_passed',true,
    'visibility_gate_passed',true,
    'source_ref',a.runtime_session_id::text,
    'meaning_text',btrim(p_summary),
    'child_voice_quote',left(p_user_utterance,1000)
  ));
end;
$$;

revoke all on function public.request_child_pinned_memory_v2(
  uuid,text,text,text,text,numeric,boolean,boolean,boolean,boolean,text,text,text,boolean,text
) from public, anon, service_role;
grant execute on function public.request_child_pinned_memory_v2(
  uuid,text,text,text,text,numeric,boolean,boolean,boolean,boolean,text,text,text,boolean,text
) to authenticated;

create or replace function public.retrieve_child_pinned_memories_v2(
  p_child_id uuid,
  p_session_key text,
  p_limit integer default 20
)
returns jsonb
language plpgsql
security definer
set search_path = pg_catalog
as $$
declare
  a record;
  v_memories jsonb;
begin
  if p_child_id is null or btrim(coalesce(p_session_key,'')) = '' then
    return jsonb_build_object('ok',false,'reason','child_and_session_required','memories','[]'::jsonb);
  end if;

  select * into a
  from public.resolve_memory_actor_evidence_shadow_v1(p_child_id,p_session_key)
  limit 1;

  if not coalesce(a.verified,false)
     or coalesce(a.actor_role_resolved,'') <> 'child'
     or coalesce(a.source_type,'') <> 'child_direct'
     or a.actor_account_id is null then
    return jsonb_build_object('ok',false,'reason',coalesce(a.reason,'verified_child_identity_required'),'memories','[]'::jsonb);
  end if;

  select coalesce(jsonb_agg(to_jsonb(m) order by m.created_at desc),'[]'::jsonb)
  into v_memories
  from memory_v2_api.retrieve_child_memories(
    p_child_id,
    a.actor_account_id,
    greatest(1,least(coalesce(p_limit,20),100))
  ) m;

  return jsonb_build_object('ok',true,'reason','verified_child_direct','memories',v_memories);
end;
$$;

revoke all on function public.retrieve_child_pinned_memories_v2(uuid,text,integer)
  from public, anon, service_role;
grant execute on function public.retrieve_child_pinned_memories_v2(uuid,text,integer)
  to authenticated;
