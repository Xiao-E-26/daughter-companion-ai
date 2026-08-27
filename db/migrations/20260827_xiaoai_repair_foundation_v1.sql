-- Applied to Supabase project daughter-companion-ai on 2026-08-27.
-- Structural repair only. No Behavior Logic changes.

alter table public.shared_continuity_state
  add column if not exists visibility text not null default 'shared_runtime';

do $$ begin
  if not exists (
    select 1 from pg_constraint
    where conrelid = 'public.shared_continuity_state'::regclass
      and conname = 'shared_continuity_state_visibility_check'
  ) then
    alter table public.shared_continuity_state
      add constraint shared_continuity_state_visibility_check
      check (visibility = any (array['shared_runtime'::text,'guardian_only'::text,'child_only'::text,'system_only'::text]));
  end if;
end $$;

drop policy if exists shared_continuity_select_active_companion on public.shared_continuity_state;
create policy shared_continuity_select_visible_companion
on public.shared_continuity_state
for select
to authenticated
using (
  exists (
    select 1
    from public.users u
    join public.companion_access ca on ca.user_id = u.id
    where u.auth_user_id = (select auth.uid())
      and u.status = 'active'
      and ca.daughter_id = shared_continuity_state.daughter_id
      and ca.status = 'active'
      and (
        shared_continuity_state.visibility = 'shared_runtime'
        or (shared_continuity_state.visibility = 'guardian_only' and ca.role = 'guardian')
        or (shared_continuity_state.visibility = 'child_only' and ca.role = 'child')
      )
  )
);

drop policy if exists users_select_self on public.users;
create policy users_select_self on public.users for select to authenticated
using ((select auth.uid()) = auth_user_id);

drop policy if exists users_insert_self on public.users;
create policy users_insert_self on public.users for insert to authenticated
with check ((select auth.uid()) = auth_user_id);

drop policy if exists users_update_self on public.users;
create policy users_update_self on public.users for update to authenticated
using ((select auth.uid()) = auth_user_id)
with check ((select auth.uid()) = auth_user_id);

drop policy if exists daughter_identities_select_self on public.daughter_identities;
create policy daughter_identities_select_self on public.daughter_identities for select to authenticated
using (exists (
  select 1 from public.users u
  where u.id = daughter_identities.user_id
    and u.auth_user_id = (select auth.uid())
));

drop policy if exists growth_states_select_self on public.growth_states;
create policy growth_states_select_self on public.growth_states for select to authenticated
using (exists (
  select 1 from public.users u
  where u.id = growth_states.user_id
    and u.auth_user_id = (select auth.uid())
));

create index if not exists runtime_sessions_user_id_idx on public.runtime_sessions(user_id);
create index if not exists runtime_sessions_client_connection_id_idx on public.runtime_sessions(client_connection_id);
create index if not exists guardians_user_id_idx on public.guardians(user_id);
create index if not exists guardians_auth_user_id_idx on public.guardians(auth_user_id);
create index if not exists guardian_link_requests_requested_by_user_id_idx on public.guardian_link_requests(requested_by_user_id);
create index if not exists guardian_link_requests_claimed_by_user_id_idx on public.guardian_link_requests(claimed_by_user_id);
create index if not exists continuity_updates_actor_user_id_idx on public.continuity_updates(actor_user_id);
create index if not exists continuity_updates_client_connection_id_idx on public.continuity_updates(client_connection_id);
create index if not exists shared_continuity_state_source_client_id_idx on public.shared_continuity_state(source_client_id);
create index if not exists shared_continuity_state_last_updated_by_user_id_idx on public.shared_continuity_state(last_updated_by_user_id);
create index if not exists safety_events_user_id_idx on public.safety_events(user_id);
create index if not exists safety_events_daughter_id_idx on public.safety_events(daughter_id);
create index if not exists experience_memories_user_id_idx on public.experience_memories(user_id);
create index if not exists experience_memories_daughter_id_idx on public.experience_memories(daughter_id);
create index if not exists audit_logs_user_id_idx on public.audit_logs(user_id);
create index if not exists audit_logs_daughter_id_idx on public.audit_logs(daughter_id);
create index if not exists relationships_user_id_idx on public.relationships(user_id);
create index if not exists xiaoai_device_enrollments_client_connection_id_idx on public.xiaoai_device_enrollments(client_connection_id);
create index if not exists xiaoai_device_enrollments_daughter_id_idx on public.xiaoai_device_enrollments(daughter_id);

revoke all on function public.get_companion_preferred_name(uuid) from public, anon;
grant execute on function public.get_companion_preferred_name(uuid) to authenticated, service_role;
