-- Daughter Project auth + RLS baseline v0.1
-- Principle: client access is minimal; sensitive/runtime data stays backend-only.

-- Link application identities to Supabase Auth when present.
alter table public.users
  add constraint users_auth_user_id_fkey
  foreign key (auth_user_id) references auth.users(id) on delete set null;

alter table public.guardians
  add constraint guardians_auth_user_id_fkey
  foreign key (auth_user_id) references auth.users(id) on delete set null;

-- Self profile: authenticated user may read, create, and update only their own row.
create policy users_select_self
on public.users
for select
to authenticated
using (auth.uid() = auth_user_id);

create policy users_insert_self
on public.users
for insert
to authenticated
with check (auth.uid() = auth_user_id);

create policy users_update_self
on public.users
for update
to authenticated
using (auth.uid() = auth_user_id)
with check (auth.uid() = auth_user_id);

-- Daughter identity: authenticated user may read the identity linked to their own user row.
-- Creation and mutation remain backend-only so identity continuity cannot be rewritten by a client.
create policy daughter_identities_select_self
on public.daughter_identities
for select
to authenticated
using (
  exists (
    select 1
    from public.users u
    where u.id = daughter_identities.user_id
      and u.auth_user_id = auth.uid()
  )
);

-- Relationship: user may read their own companion relationship state.
-- Writes remain backend-only.
create policy relationships_select_self
on public.relationships
for select
to authenticated
using (
  exists (
    select 1
    from public.users u
    where u.id = relationships.user_id
      and u.auth_user_id = auth.uid()
  )
);

-- Growth state: user may read their own current growth context.
-- Writes remain backend-only to avoid client-side maturity escalation.
create policy growth_states_select_self
on public.growth_states
for select
to authenticated
using (
  exists (
    select 1
    from public.users u
    where u.id = growth_states.user_id
      and u.auth_user_id = auth.uid()
  )
);

-- Intentionally no direct client policies yet on:
-- guardians, memories, runtime_sessions, safety_events,
-- experience_memories, audit_logs.
-- These contain authority-sensitive, safety-sensitive, or runtime-managed data
-- and remain deny-by-default behind the backend/service role until a mediated API is defined.
