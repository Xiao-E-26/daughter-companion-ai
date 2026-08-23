-- Daughter Project MVP schema v0.1
-- Draft only. Not yet applied to any Supabase project.

create extension if not exists pgcrypto;

create table if not exists public.users (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique,
  preferred_name text,
  birth_context text,
  language text,
  status text not null default 'active' check (status in ('active','inactive','deleted')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.daughter_identities (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  identity_version text not null default '0.3',
  core_version text not null default '0.3',
  status text not null default 'active' check (status in ('active','paused','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(user_id)
);

create table if not exists public.relationships (
  id uuid primary key default gen_random_uuid(),
  daughter_id uuid not null references public.daughter_identities(id) on delete cascade,
  user_id uuid not null references public.users(id) on delete cascade,
  relationship_stage text,
  interaction_style text,
  proactivity text,
  started_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(daughter_id, user_id)
);

create table if not exists public.guardians (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  auth_user_id uuid,
  relationship text,
  status text not null default 'active' check (status in ('active','inactive','revoked')),
  is_primary boolean not null default false,
  emergency_contact text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.memories (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  daughter_id uuid not null references public.daughter_identities(id) on delete cascade,
  type text not null check (type in ('preference','relationship','development','sensitive','safety','experience')),
  content text not null,
  fact_status text not null default 'unknown' check (fact_status in ('fact','feeling','interpretation','mixed','unknown')),
  confidence text not null default 'unverified' check (confidence in ('high','medium','low','unverified')),
  sensitivity text not null default 'normal' check (sensitivity in ('normal','sensitive','high')),
  importance text not null default 'normal' check (importance in ('low','normal','high')),
  status text not null default 'active' check (status in ('active','historical','disputed','archived','deleted')),
  source text,
  last_confirmed_at timestamptz,
  expires_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists memories_user_id_idx on public.memories(user_id);
create index if not exists memories_daughter_id_idx on public.memories(daughter_id);
create index if not exists memories_status_idx on public.memories(status);
create index if not exists memories_type_idx on public.memories(type);

create table if not exists public.growth_states (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  core_stage text not null default 'protective_companionship' check (core_stage in ('protective_companionship','guided_learning','autonomy_building','mature_companionship')),
  learning_state text,
  social_state text,
  privacy_state text,
  risk_state text,
  updated_at timestamptz not null default now(),
  unique(user_id)
);

create table if not exists public.runtime_sessions (
  id uuid primary key default gen_random_uuid(),
  daughter_id uuid not null references public.daughter_identities(id) on delete cascade,
  user_id uuid not null references public.users(id) on delete cascade,
  runtime_version text not null default '0.1',
  status text not null default 'active' check (status in ('active','closed','revoked')),
  started_at timestamptz not null default now(),
  last_active_at timestamptz not null default now()
);

create table if not exists public.safety_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  daughter_id uuid references public.daughter_identities(id) on delete set null,
  risk_level integer not null check (risk_level between 0 and 3),
  summary text not null,
  guardian_conflict boolean not null default false,
  action_taken text,
  status text not null default 'open' check (status in ('open','monitoring','resolved','closed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.experience_memories (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  daughter_id uuid not null references public.daughter_identities(id) on delete cascade,
  problem_pattern text not null,
  context text,
  hypothesis text,
  action text,
  outcome text,
  lesson text,
  confidence text not null default 'unverified' check (confidence in ('high','medium','low','unverified')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.audit_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete set null,
  daughter_id uuid references public.daughter_identities(id) on delete set null,
  actor_type text not null check (actor_type in ('user','guardian','admin','runtime','system')),
  actor_id uuid,
  event_type text not null,
  event_summary text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

-- RLS is enabled now so no table is accidentally exposed by default.
alter table public.users enable row level security;
alter table public.daughter_identities enable row level security;
alter table public.relationships enable row level security;
alter table public.guardians enable row level security;
alter table public.memories enable row level security;
alter table public.growth_states enable row level security;
alter table public.runtime_sessions enable row level security;
alter table public.safety_events enable row level security;
alter table public.experience_memories enable row level security;
alter table public.audit_logs enable row level security;

-- No client-facing RLS policies are added in this migration.
-- Access remains denied by default until authentication ownership rules are finalized.
