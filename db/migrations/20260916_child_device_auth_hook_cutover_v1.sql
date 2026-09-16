
-- XiaoAi child-device Auth enrollment cutover v1
-- Canonical anonymous signup gate: invite/enrollment-token only.

create or replace function public.hook_xiaoai_child_enrollment_before_user_created_v1(event jsonb)
returns jsonb
language plpgsql
as $$
declare
  v_is_anonymous boolean := coalesce((event->'user'->>'is_anonymous')::boolean,false);
  v_token text := nullif(btrim(event->'user'->'user_metadata'->>'xiaoai_enrollment_token'),'');
  v_client_type text := nullif(btrim(event->'user'->'user_metadata'->>'client_type'),'');
begin
  if not v_is_anonymous then
    return '{}'::jsonb;
  end if;
  if v_token is null or v_token !~ '^[0-9A-Fa-f]{64}$' or v_client_type is null then
    return jsonb_build_object('error',jsonb_build_object('http_code',403,'message','Valid child-device enrollment is required.'));
  end if;
  if not exists (
    select 1 from public.child_device_enrollment_challenges c
    where c.token_hash=extensions.digest(v_token,'sha256')
      and c.status='pending' and c.expires_at>now()
  ) then
    return jsonb_build_object('error',jsonb_build_object('http_code',403,'message','Valid child-device enrollment is required.'));
  end if;
  return '{}'::jsonb;
end;
$$;

grant usage on schema public to supabase_auth_admin;
grant usage on schema extensions to supabase_auth_admin;
grant execute on function public.hook_xiaoai_child_enrollment_before_user_created_v1(jsonb) to supabase_auth_admin;
revoke execute on function public.hook_xiaoai_child_enrollment_before_user_created_v1(jsonb)
  from authenticated,anon,public,service_role;

grant select on public.child_device_enrollment_challenges to supabase_auth_admin;
drop policy if exists "supabase_auth_admin_read_child_device_enrollment_challenges" on public.child_device_enrollment_challenges;
create policy "supabase_auth_admin_read_child_device_enrollment_challenges"
  on public.child_device_enrollment_challenges as permissive for select to supabase_auth_admin using(true);

create or replace function public.finalize_xiaoai_anonymous_child_enrollment_v1()
returns trigger
language plpgsql
security definer
set search_path=''
as $$
declare
  v_token text;
  v_client_type text;
  v_device_label text;
  v_challenge_id uuid;
  v_child_id uuid;
  v_user_id uuid;
begin
  if not coalesce(new.is_anonymous,false) then return new; end if;
  v_token:=nullif(btrim(new.raw_user_meta_data->>'xiaoai_enrollment_token'),'');
  v_client_type:=nullif(btrim(new.raw_user_meta_data->>'client_type'),'');
  v_device_label:=nullif(btrim(new.raw_user_meta_data->>'device_label'),'');
  if v_token is null or v_token !~ '^[0-9A-Fa-f]{64}$' or v_client_type is null then
    raise exception 'valid child-device enrollment required';
  end if;
  select c.id,c.child_id into v_challenge_id,v_child_id
  from public.child_device_enrollment_challenges c
  where c.token_hash=extensions.digest(v_token,'sha256')
    and c.status='pending' and c.expires_at>now()
  for update;
  if v_challenge_id is null then raise exception 'child-device enrollment unavailable'; end if;
  insert into public.users(auth_user_id,status)
  values(new.id,'active')
  on conflict(auth_user_id) do update set status='active',updated_at=now()
  returning id into v_user_id;
  insert into public.companion_access(child_id,user_id,role,status,verified_at)
  values(v_child_id,v_user_id,'child','active',now())
  on conflict(child_id,user_id,role) do update
    set status='active',verified_at=excluded.verified_at,updated_at=now();
  insert into public.client_connections(
    child_id,user_id,client_type,external_account_ref_hash,device_label,status,linked_at,last_seen_at
  ) values(
    v_child_id,v_user_id,v_client_type,
    encode(extensions.digest(new.id::text,'sha256'),'hex'),v_device_label,'active',now(),now()
  );
  update public.child_device_enrollment_challenges
  set status='claimed',claimed_at=now(),claimed_auth_user_id=new.id
  where id=v_challenge_id;
  update auth.users
  set raw_user_meta_data=coalesce(raw_user_meta_data,'{}'::jsonb)-'xiaoai_enrollment_token'
  where id=new.id;
  return new;
end;
$$;
revoke all on function public.finalize_xiaoai_anonymous_child_enrollment_v1()
  from public,anon,authenticated,service_role;

drop trigger if exists trg_finalize_xiaoai_anonymous_child_enrollment_v1 on auth.users;
create trigger trg_finalize_xiaoai_anonymous_child_enrollment_v1
after insert on auth.users
for each row
when (new.is_anonymous is true)
execute function public.finalize_xiaoai_anonymous_child_enrollment_v1();

revoke execute on function public.claim_child_device_enrollment_shadow_v1(text,text,text)
  from authenticated,service_role,anon,public;

comment on function public.hook_xiaoai_child_enrollment_before_user_created_v1(jsonb) is
'Canonical Before User Created hook for child anonymous signup. Anonymous signup is allowed only with a valid one-time child-device enrollment token.';
comment on function public.finalize_xiaoai_anonymous_child_enrollment_v1() is
'Canonical auth.users AFTER INSERT finalizer for anonymous child enrollment. Claims challenge, creates verified bindings, and removes plaintext enrollment token from auth metadata.';
