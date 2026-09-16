
-- XiaoAi verified memory actor resolver shadow v1
-- SHADOW ONLY. Does not alter the existing memory save/promotion path.

create or replace function public.resolve_memory_actor_evidence_shadow_v1(
  p_child_id uuid,
  p_session_key text
) returns table(
  verified boolean,
  actor_role_resolved text,
  source_type text,
  actor_account_id uuid,
  runtime_session_id uuid,
  client_connection_id uuid,
  reason text
)
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  v_auth_user_id uuid := auth.uid();
  v_user_id uuid;
  v_role text;
  v_session_id uuid;
  v_client_id uuid;
begin
  if v_auth_user_id is null then
    return query select false,'unverified','unverified',null::uuid,null::uuid,null::uuid,'authentication_required';
    return;
  end if;

  select u.id into v_user_id
  from public.users u
  where u.auth_user_id = v_auth_user_id
    and u.status = 'active'
  limit 1;

  if v_user_id is null then
    return query select false,'unverified','unverified',null::uuid,null::uuid,null::uuid,'active_user_binding_required';
    return;
  end if;

  select ca.role into v_role
  from public.companion_access ca
  where ca.child_id = p_child_id
    and ca.user_id = v_user_id
    and ca.status = 'active'
  order by case when ca.role='child' then 0 else 1 end
  limit 1;

  if v_role is null then
    return query select false,'unverified','unverified',v_user_id,null::uuid,null::uuid,'active_companion_access_required';
    return;
  end if;

  if v_role <> 'child' then
    return query select false,v_role,'not_child_direct',v_user_id,null::uuid,null::uuid,'actor_not_child';
    return;
  end if;

  if p_session_key is null or btrim(p_session_key) = '' then
    return query select false,'child','unverified',v_user_id,null::uuid,null::uuid,'session_key_required';
    return;
  end if;

  select rs.id,cc.id into v_session_id,v_client_id
  from public.runtime_sessions rs
  join public.client_connections cc on cc.id = rs.client_connection_id
  where rs.child_id = p_child_id
    and rs.user_id = v_user_id
    and rs.session_key = p_session_key
    and rs.status = 'active'
    and cc.child_id = p_child_id
    and cc.user_id = v_user_id
    and cc.status = 'active'
  limit 1;

  if v_session_id is null or v_client_id is null then
    return query select false,'child','unverified',v_user_id,null::uuid,null::uuid,'active_session_client_binding_required';
    return;
  end if;

  return query select true,'child','child_direct',v_user_id,v_session_id,v_client_id,'verified_child_direct';
end;
$$;

revoke all on function public.resolve_memory_actor_evidence_shadow_v1(uuid,text) from public, anon;
grant execute on function public.resolve_memory_actor_evidence_shadow_v1(uuid,text) to authenticated, service_role;

comment on function public.resolve_memory_actor_evidence_shadow_v1(uuid,text) is
'SHADOW ONLY. Verified child_direct evidence requires matching Supabase Auth identity plus active user, child access, client connection and runtime session. Speaker text and model inference are never identity evidence.';
