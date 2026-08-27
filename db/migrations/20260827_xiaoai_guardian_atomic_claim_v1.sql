-- Applied to Supabase project daughter-companion-ai on 2026-08-27.
-- Adds a service-role-only atomic Guardian claim primitive.
-- Existing Edge Function remains unchanged until explicit cutover.

create or replace function public.claim_xiaoai_guardian_link_atomic(
  p_token_hash text,
  p_guardian_user_id uuid,
  p_auth_user_id uuid,
  p_external_account_ref_hash text,
  p_email_verified boolean default false
) returns jsonb
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  v_invite public.guardian_link_requests%rowtype;
  v_now timestamptz := now();
  v_existing_auth uuid;
  v_existing_guardian_auth uuid;
  v_guardian_status text;
begin
  select * into v_invite
  from public.guardian_link_requests
  where token_hash = p_token_hash
  for update;

  if not found then raise exception 'invite_not_found'; end if;
  if v_invite.status <> 'pending' then raise exception 'invite_not_pending'; end if;
  if v_invite.expires_at <= v_now then
    update public.guardian_link_requests set status='expired', updated_at=v_now where id=v_invite.id;
    raise exception 'invite_expired';
  end if;

  select auth_user_id into v_existing_auth
  from public.users where id=p_guardian_user_id for update;
  if not found then raise exception 'guardian_user_missing'; end if;

  select auth_user_id, status into v_existing_guardian_auth, v_guardian_status
  from public.guardians where user_id=p_guardian_user_id for update;

  if v_existing_auth is not null and v_existing_auth <> p_auth_user_id
     and coalesce(v_guardian_status,'active')='active' then
    raise exception 'guardian_identity_already_bound';
  end if;
  if v_existing_guardian_auth is not null and v_existing_guardian_auth <> p_auth_user_id
     and coalesce(v_guardian_status,'active')='active' then
    raise exception 'guardian_identity_already_bound';
  end if;

  if exists (select 1 from public.users where auth_user_id=p_auth_user_id and id<>p_guardian_user_id) then
    raise exception 'auth_identity_already_bound';
  end if;

  update public.users
    set auth_user_id=p_auth_user_id, preferred_name='Mother Guardian', status='active', updated_at=v_now
    where id=p_guardian_user_id;

  insert into public.guardians(user_id,auth_user_id,relationship,status,is_primary,created_at,updated_at)
  values (p_guardian_user_id,p_auth_user_id,'mother','active',true,v_now,v_now)
  on conflict (user_id) do update
    set auth_user_id=excluded.auth_user_id,
        relationship='mother',
        status='active',
        is_primary=true,
        updated_at=v_now;

  update public.companion_access
    set status='active', verified_at=v_now, updated_at=v_now
    where daughter_id=v_invite.daughter_id and user_id=p_guardian_user_id and role='guardian';
  if not found then raise exception 'guardian_access_missing'; end if;

  update public.client_connections
    set status='active', external_account_ref_hash=p_external_account_ref_hash,
        device_label='Mother ChatGPT - verified', linked_at=v_now,
        last_seen_at=v_now, updated_at=v_now
    where daughter_id=v_invite.daughter_id and user_id=p_guardian_user_id and client_type='chatgpt';
  if not found then raise exception 'guardian_client_missing'; end if;

  update public.guardian_link_requests
    set status='claimed', claimed_by_user_id=p_guardian_user_id, claimed_at=v_now, updated_at=v_now
    where id=v_invite.id and status='pending';
  if not found then raise exception 'invite_claim_race'; end if;

  insert into public.audit_logs(user_id,daughter_id,actor_type,actor_id,event_type,event_summary,metadata)
  values (
    v_invite.child_user_id,
    v_invite.daughter_id,
    'guardian',
    p_guardian_user_id,
    'mother_guardian_linked',
    'Mother Guardian linked through verified Supabase Auth identity',
    jsonb_build_object('email_verified',p_email_verified,'provider','supabase_auth','client_type','chatgpt','atomic',true)
  );

  return jsonb_build_object(
    'ok',true,
    'role','guardian',
    'relationship','mother',
    'daughter_id',v_invite.daughter_id,
    'guardian_user_id',p_guardian_user_id
  );
end;
$$;

revoke all on function public.claim_xiaoai_guardian_link_atomic(text,uuid,uuid,text,boolean) from public, anon, authenticated;
grant execute on function public.claim_xiaoai_guardian_link_atomic(text,uuid,uuid,text,boolean) to service_role;
