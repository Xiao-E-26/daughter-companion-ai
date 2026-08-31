-- XiaoAi Memory v2 independent foundation
-- Prepared 2026-08-31.
-- This migration is intentionally dormant: durable_memory_mode defaults to 'off'.
-- Legacy memory tables are not read, written, altered, or required.

create schema if not exists memory_v2_private;
create schema if not exists memory_v2_api;

revoke all on schema memory_v2_private from public, anon, authenticated;
revoke all on schema memory_v2_api from public, anon, authenticated;

grant usage on schema memory_v2_api to service_role;

create table if not exists memory_v2_private.runtime_flags (
  flag_key text primary key,
  flag_value text not null,
  updated_at timestamptz not null default now(),
  constraint memory_v2_runtime_flags_mode_check
    check (
      flag_key <> 'durable_memory_mode'
      or flag_value in ('off', 'child_pinned_only')
    )
);

insert into memory_v2_private.runtime_flags(flag_key, flag_value)
values ('durable_memory_mode', 'off')
on conflict (flag_key) do nothing;

create table if not exists memory_v2_private.subjects (
  subject_id uuid primary key,
  status text not null default 'active',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists memory_v2_private.accounts (
  account_id uuid primary key,
  provider text not null,
  provider_user_id text not null,
  status text not null default 'active',
  created_at timestamptz not null default now(),
  revoked_at timestamptz,
  unique(provider, provider_user_id)
);

create table if not exists memory_v2_private.subject_account_links (
  link_id uuid primary key default gen_random_uuid(),
  subject_id uuid not null references memory_v2_private.subjects(subject_id),
  account_id uuid not null references memory_v2_private.accounts(account_id),
  relationship_role text not null,
  status text not null default 'active',
  can_submit_child_pinned boolean not null default false,
  can_request_correction boolean not null default false,
  can_request_deletion boolean not null default false,
  created_at timestamptz not null default now(),
  revoked_at timestamptz,
  unique(subject_id, account_id)
);

create table if not exists memory_v2_private.memories (
  memory_id uuid primary key default gen_random_uuid(),
  subject_id uuid not null references memory_v2_private.subjects(subject_id),
  summary text not null,
  category text not null default 'event',
  source_type text not null,
  confidence numeric(4,3) not null default 1.0 check (confidence >= 0 and confidence <= 1),
  sensitivity text not null default 'low',
  status text not null default 'active',
  retention_class text not null default 'child_pinned',
  pinned_by_child boolean not null default true,
  disclosure_scope text not null default 'subject_only',
  proactive_surface_allowed boolean not null default false,
  reasoning_use_allowed boolean not null default true,
  on_request_allowed boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  deleted_at timestamptz,
  superseded_by uuid references memory_v2_private.memories(memory_id)
);

create table if not exists memory_v2_private.revisions (
  revision_id uuid primary key default gen_random_uuid(),
  memory_id uuid not null references memory_v2_private.memories(memory_id),
  revision_number bigint not null,
  summary text not null,
  meaning_text text,
  child_voice_quote text,
  source_type text not null,
  created_by_account_id uuid references memory_v2_private.accounts(account_id),
  created_at timestamptz not null default now(),
  unique(memory_id, revision_number)
);

create table if not exists memory_v2_private.sources (
  source_id uuid primary key default gen_random_uuid(),
  memory_id uuid not null references memory_v2_private.memories(memory_id),
  source_account_id uuid references memory_v2_private.accounts(account_id),
  source_type text not null,
  source_ref text,
  observed_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create table if not exists memory_v2_private.tombstones (
  tombstone_id uuid primary key default gen_random_uuid(),
  memory_id uuid not null unique references memory_v2_private.memories(memory_id),
  subject_id uuid not null references memory_v2_private.subjects(subject_id),
  deleted_by_account_id uuid references memory_v2_private.accounts(account_id),
  deleted_at timestamptz not null default now(),
  delete_reason text,
  version bigint not null default 1
);

create table if not exists memory_v2_private.audit_events (
  audit_id uuid primary key default gen_random_uuid(),
  subject_id uuid,
  memory_id uuid,
  actor_account_id uuid,
  action text not null,
  decision text not null,
  reason_code text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists memory_v2_private.idempotency_keys (
  idempotency_key text primary key,
  operation text not null,
  memory_id uuid,
  created_at timestamptz not null default now()
);

create index if not exists memory_v2_memories_subject_status_idx
  on memory_v2_private.memories(subject_id, status);
create index if not exists memory_v2_links_account_subject_idx
  on memory_v2_private.subject_account_links(account_id, subject_id, status);
create index if not exists memory_v2_revisions_memory_idx
  on memory_v2_private.revisions(memory_id, revision_number);
create index if not exists memory_v2_sources_memory_idx
  on memory_v2_private.sources(memory_id);
create index if not exists memory_v2_audit_subject_idx
  on memory_v2_private.audit_events(subject_id, created_at desc);

create or replace function memory_v2_api.get_mode()
returns text
language sql
security definer
set search_path = pg_catalog, memory_v2_private
as $$
  select coalesce(
    (select flag_value from memory_v2_private.runtime_flags where flag_key = 'durable_memory_mode'),
    'off'
  );
$$;

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

  v_subject_id := (payload->>'subject_id')::uuid;
  v_account_id := (payload->>'actor_account_id')::uuid;

  select exists(
    select 1
    from memory_v2_private.subject_account_links l
    where l.subject_id = v_subject_id
      and l.account_id = v_account_id
      and l.relationship_role = 'child'
      and l.status = 'active'
      and l.can_submit_child_pinned = true
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
    v_subject_id,
    payload->>'summary',
    coalesce(payload->>'category', 'event'),
    'child_direct',
    v_conf,
    coalesce(payload->>'sensitivity', 'low'),
    'active',
    'child_pinned',
    true,
    coalesce(payload->>'disclosure_scope', 'subject_only'),
    false,
    true,
    true
  ) returning memory_id into v_memory_id;

  insert into memory_v2_private.revisions(
    memory_id, revision_number, summary, meaning_text, child_voice_quote,
    source_type, created_by_account_id
  ) values (
    v_memory_id, 1, payload->>'summary', payload->>'meaning_text',
    payload->>'child_voice_quote', 'child_direct', v_account_id
  );

  insert into memory_v2_private.sources(
    memory_id, source_account_id, source_type, source_ref
  ) values (
    v_memory_id, v_account_id, 'child_direct', payload->>'source_ref'
  );

  insert into memory_v2_private.idempotency_keys(idempotency_key, operation, memory_id)
  values (v_key, 'pin_child_memory', v_memory_id);

  insert into memory_v2_private.audit_events(
    subject_id, memory_id, actor_account_id, action, decision, reason_code
  ) values (
    v_subject_id, v_memory_id, v_account_id, 'pin_child_memory', 'accepted', 'child_direct_explicit_intent'
  );

  return jsonb_build_object('accepted', true, 'reason', 'created', 'memory_id', v_memory_id);
exception
  when invalid_text_representation then
    return jsonb_build_object('accepted', false, 'reason', 'invalid_identifier');
end;
$$;

create or replace function memory_v2_api.retrieve_child_memories(
  p_subject_id uuid,
  p_account_id uuid,
  p_limit integer default 20
)
returns table(
  memory_id uuid,
  summary text,
  category text,
  sensitivity text,
  created_at timestamptz
)
language sql
security definer
set search_path = pg_catalog, memory_v2_private
as $$
  select m.memory_id, m.summary, m.category, m.sensitivity, m.created_at
  from memory_v2_private.memories m
  where m.subject_id = p_subject_id
    and m.status = 'active'
    and m.deleted_at is null
    and m.reasoning_use_allowed = true
    and exists (
      select 1
      from memory_v2_private.subject_account_links l
      where l.subject_id = p_subject_id
        and l.account_id = p_account_id
        and l.status = 'active'
        and l.relationship_role = 'child'
    )
  order by m.created_at desc
  limit greatest(1, least(coalesce(p_limit, 20), 100));
$$;

revoke all on function memory_v2_api.get_mode() from public, anon, authenticated;
revoke all on function memory_v2_api.pin_child_memory(jsonb) from public, anon, authenticated;
revoke all on function memory_v2_api.retrieve_child_memories(uuid, uuid, integer) from public, anon, authenticated;

grant execute on function memory_v2_api.get_mode() to service_role;
grant execute on function memory_v2_api.pin_child_memory(jsonb) to service_role;
grant execute on function memory_v2_api.retrieve_child_memories(uuid, uuid, integer) to service_role;
