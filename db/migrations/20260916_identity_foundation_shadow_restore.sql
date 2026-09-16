
-- XiaoAi minimal identity foundation shadow restore
-- PREPARED ONLY. DO NOT APPLY TO PRODUCTION YET.
-- Purpose: restore only the verified actor/session/client identity substrate required
-- by MemoryActorEvidenceResolver and the canonical durable-memory policy gate.
-- This migration does not activate users, does not alter existing memory tables,
-- and does not replace legacy production promotion.

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique,
  preferred_name text,
  status text not null default 'pending',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint users_status_check check (status in ('pending','active','revoked'))
);

create table if not exists public.companion_access (
  id uuid primary key default gen_random_uuid(),
  child_id uuid not null references public.child_profiles(id) on delete cascade,
  user_id uuid not null references public.users(id) on delete cascade,
  role text not null,
  status text not null default 'pending',
  authority_scope jsonb not null default '{}'::jsonb,
  verified_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(child_id,user_id,role),
  constraint companion_access_role_check check (role in ('child','guardian')),
  constraint companion_access_status_check check (status in ('pending','active','revoked'))
);

create table if not exists public.client_connections (
  id uuid primary key default gen_random_uuid(),
  child_id uuid not null references public.child_profiles(id) on delete cascade,
  user_id uuid not null references public.users(id) on delete cascade,
  client_type text not null,
  external_account_ref_hash text,
  device_label text,
  status text not null default 'pending',
  linked_at timestamptz,
  last_seen_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint client_connections_status_check check (status in ('pending','active','revoked'))
);

create table if not exists public.runtime_sessions (
  id uuid primary key default gen_random_uuid(),
  child_id uuid not null references public.child_profiles(id) on delete cascade,
  user_id uuid not null references public.users(id) on delete cascade,
  client_connection_id uuid not null references public.client_connections(id) on delete restrict,
  session_key text not null,
  status text not null default 'pending',
  started_at timestamptz,
  ended_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(child_id,session_key),
  constraint runtime_sessions_status_check check (status in ('pending','active','closed','revoked'))
);

create index if not exists users_auth_user_id_idx on public.users(auth_user_id);
create index if not exists companion_access_user_child_idx on public.companion_access(user_id,child_id,status);
create index if not exists client_connections_user_child_idx on public.client_connections(user_id,child_id,status);
create index if not exists runtime_sessions_user_child_idx on public.runtime_sessions(user_id,child_id,status);
create index if not exists runtime_sessions_client_connection_idx on public.runtime_sessions(client_connection_id);

alter table public.users enable row level security;
alter table public.companion_access enable row level security;
alter table public.client_connections enable row level security;
alter table public.runtime_sessions enable row level security;

-- No permissive authenticated policies are created in the shadow restore.
-- Until explicit cutover, only service-role workflows may populate/bind these rows.
-- Missing, pending, revoked, mismatched, or unverified bindings must resolve to no
-- child_direct actor evidence.

comment on table public.runtime_sessions is
'SHADOW identity substrate. runtime_sessions.user_id is the verified session actor candidate; it is authoritative only when matched to active users, active companion_access, an active verified client_connection, and an active runtime session.';
