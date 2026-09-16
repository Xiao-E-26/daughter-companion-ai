
-- XiaoAi child device enrollment shadow v1
-- SHADOW ONLY. Anonymous Auth remains disabled until abuse protection is configured.
-- Purpose: give a child device a cryptographically authenticated Supabase identity
-- without requiring email/password, then bind it to child/client/runtime-session state.

create table if not exists public.child_device_enrollment_challenges (
  id uuid primary key default gen_random_uuid(),
  child_id uuid not null references public.child_profiles(id) on delete cascade,
  guardian_auth_user_id uuid not null,
  token_hash bytea not null unique,
  status text not null default 'pending',
  expires_at timestamptz not null,
  claimed_at timestamptz,
  claimed_auth_user_id uuid,
  created_at timestamptz not null default now(),
  constraint child_device_enrollment_status_check
    check (status in ('pending','claimed','revoked','expired'))
);

create index if not exists child_device_enrollment_child_status_idx
  on public.child_device_enrollment_challenges(child_id,status,expires_at);

alter table public.child_device_enrollment_challenges enable row level security;

create or replace function public.create_child_device_enrollment_shadow_v1(
  p_child_id uuid,
  p_ttl_minutes integer default 10
) returns table(
  challenge_id uuid,
  enrollment_token text,
  expires_at timestamptz
)
language plpgsql
security definer
set search_path = public, auth, extensions
as $$
declare
  v_uid uuid := auth.uid();
  v_token text;
  v_hash bytea;
  v_id uuid;
  v_expires timestamptz;
begin
  if v_uid is null then
    raise exception 'authenticated guardian required';
  end if;
  if not exists (
    select 1 from public.child_profiles c
    where c.id=p_child_id and c.guardian_id=v_uid
  ) then
    raise exception 'guardian does not own child';
  end if;
  if p_ttl_minutes < 2 or p_ttl_minutes > 30 then
    raise exception 'enrollment ttl out of range';
  end if;

  update public.child_device_enrollment_challenges
     set status='revoked'
   where child_id=p_child_id and status='pending';

  v_token := encode(extensions.gen_random_bytes(32),'hex');
  v_hash := extensions.digest(v_token,'sha256');
  v_expires := now() + make_interval(mins => p_ttl_minutes);

  insert into public.child_device_enrollment_challenges(
    child_id,guardian_auth_user_id,token_hash,status,expires_at
  ) values (p_child_id,v_uid,v_hash,'pending',v_expires)
  returning id into v_id;

  return query select v_id,v_token,v_expires;
end;
$$;

create or replace function public.claim_child_device_enrollment_shadow_v1(
  p_enrollment_token text,
  p_client_type text,
  p_device_label text default null
) returns table(
  child_id uuid,
  user_id uuid,
  client_connection_id uuid,
  reason text
)
language plpgsql
security definer
set search_path = public, auth, extensions
as $$
declare
  v_uid uuid := auth.uid();
  v_is_anonymous boolean := coalesce((auth.jwt()->>'is_anonymous')::boolean,false);
  v_challenge public.child_device_enrollment_challenges%rowtype;
  v_user_id uuid;
  v_client_id uuid;
begin
  if v_uid is null then
    raise exception 'authenticated child device required';
  end if;
  if not v_is_anonymous then
    raise exception 'anonymous child device auth required for first enrollment';
  end if;
  if p_enrollment_token is null or length(btrim(p_enrollment_token)) < 32 then
    raise exception 'invalid enrollment token';
  end if;
  if p_client_type is null or btrim(p_client_type) = '' then
    raise exception 'client type required';
  end if;

  select * into v_challenge
  from public.child_device_enrollment_challenges c
  where c.token_hash = extensions.digest(btrim(p_enrollment_token),'sha256')
    and c.status='pending'
  for update;

  if not found then
    raise exception 'enrollment challenge not found';
  end if;
  if v_challenge.expires_at <= now() then
    update public.child_device_enrollment_challenges
       set status='expired'
     where id=v_challenge.id;
    raise exception 'enrollment challenge expired';
  end if;

  select u.id into v_user_id
  from public.users u
  where u.auth_user_id=v_uid
  limit 1;

  if v_user_id is null then
    insert into public.users(auth_user_id,status)
    values(v_uid,'active')
    returning id into v_user_id;
  elsif exists (
    select 1 from public.companion_access ca
    where ca.user_id=v_user_id
      and ca.child_id<>v_challenge.child_id
      and ca.status='active'
      and ca.role='child'
  ) then
    raise exception 'anonymous auth identity already bound to another child';
  else
    update public.users set status='active',updated_at=now() where id=v_user_id;
  end if;

  insert into public.companion_access(
    child_id,user_id,role,status,verified_at
  ) values (
    v_challenge.child_id,v_user_id,'child','active',now()
  )
  on conflict(child_id,user_id,role) do update
    set status='active',verified_at=excluded.verified_at,updated_at=now();

  insert into public.client_connections(
    child_id,user_id,client_type,external_account_ref_hash,device_label,
    status,linked_at,last_seen_at
  ) values (
    v_challenge.child_id,v_user_id,btrim(p_client_type),
    encode(extensions.digest(v_uid::text,'sha256'),'hex'),
    nullif(btrim(p_device_label),''),'active',now(),now()
  ) returning id into v_client_id;

  update public.child_device_enrollment_challenges
     set status='claimed',claimed_at=now(),claimed_auth_user_id=v_uid
   where id=v_challenge.id;

  return query select v_challenge.child_id,v_user_id,v_client_id,'child_device_enrolled';
end;
$$;

create or replace function public.start_child_runtime_session_shadow_v1(
  p_child_id uuid,
  p_client_connection_id uuid
) returns table(
  runtime_session_id uuid,
  session_key text,
  reason text
)
language plpgsql
security definer
set search_path = public, auth, extensions
as $$
declare
  v_uid uuid := auth.uid();
  v_user_id uuid;
  v_session_id uuid;
  v_session_key text;
begin
  if v_uid is null then
    raise exception 'authenticated child device required';
  end if;

  select u.id into v_user_id
  from public.users u
  join public.companion_access ca on ca.user_id=u.id
  join public.client_connections cc on cc.user_id=u.id
  where u.auth_user_id=v_uid
    and u.status='active'
    and ca.child_id=p_child_id
    and ca.role='child'
    and ca.status='active'
    and cc.id=p_client_connection_id
    and cc.child_id=p_child_id
    and cc.status='active'
  limit 1;

  if v_user_id is null then
    raise exception 'verified child/client binding required';
  end if;

  v_session_key := encode(extensions.gen_random_bytes(24),'hex');
  insert into public.runtime_sessions(
    child_id,user_id,client_connection_id,session_key,status,started_at
  ) values (
    p_child_id,v_user_id,p_client_connection_id,v_session_key,'active',now()
  ) returning id into v_session_id;

  update public.client_connections set last_seen_at=now(),updated_at=now()
   where id=p_client_connection_id;

  return query select v_session_id,v_session_key,'runtime_session_started';
end;
$$;

revoke all on table public.child_device_enrollment_challenges from public, anon, authenticated;
revoke all on function public.create_child_device_enrollment_shadow_v1(uuid,integer) from public, anon;
revoke all on function public.claim_child_device_enrollment_shadow_v1(text,text,text) from public, anon;
revoke all on function public.start_child_runtime_session_shadow_v1(uuid,uuid) from public, anon;
grant execute on function public.create_child_device_enrollment_shadow_v1(uuid,integer) to authenticated, service_role;
grant execute on function public.claim_child_device_enrollment_shadow_v1(text,text,text) to authenticated, service_role;
grant execute on function public.start_child_runtime_session_shadow_v1(uuid,uuid) to authenticated, service_role;

comment on table public.child_device_enrollment_challenges is
'SHADOW ONLY. Stores only hashed one-time enrollment tokens. Anonymous Auth provider remains disabled until abuse protection is configured.';
