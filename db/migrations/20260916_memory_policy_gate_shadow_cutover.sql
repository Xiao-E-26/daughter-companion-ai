-- XiaoAi memory policy gate shadow cutover
-- PREPARED ONLY. DO NOT APPLY TO PRODUCTION YET.
-- Purpose: establish one evidence contract before replacing legacy auto-promotion.

alter table public.memory_candidates
  add column if not exists actor_role_resolved text,
  add column if not exists source_type text,
  add column if not exists actor_account_id uuid,
  add column if not exists memory_class text,
  add column if not exists sensitivity text,
  add column if not exists visibility_scope text,
  add column if not exists privacy_gate_passed boolean not null default false,
  add column if not exists sensitivity_gate_passed boolean not null default false,
  add column if not exists minimum_necessary_passed boolean not null default false,
  add column if not exists visibility_gate_passed boolean not null default false,
  add column if not exists policy_gate_status text not null default 'pending',
  add column if not exists policy_gate_reason text,
  add column if not exists policy_gate_version text,
  add column if not exists policy_gate_evaluated_at timestamptz;

alter table public.memory_candidates
  drop constraint if exists memory_candidates_policy_gate_status_check;

alter table public.memory_candidates
  add constraint memory_candidates_policy_gate_status_check
  check (policy_gate_status in ('pending','passed','blocked'));

create or replace function public.promote_memory_candidate_shadow_v2(p_candidate_id uuid)
returns uuid
language plpgsql
set search_path = public
as $$
declare
  c public.memory_candidates%rowtype;
  v_id uuid;
begin
  select * into c
  from public.memory_candidates
  where id = p_candidate_id
  for update;

  if not found then
    raise exception 'candidate not found';
  end if;

  if c.status = 'discarded' then
    raise exception 'discarded candidate cannot be promoted';
  end if;

  if coalesce(c.actor_role_resolved,'') <> 'child' then
    raise exception 'actor identity not verified child';
  end if;
  if coalesce(c.source_type,'') <> 'child_direct' then
    raise exception 'source not verified child direct';
  end if;
  if c.policy_gate_status <> 'passed' then
    raise exception 'memory policy gate not passed';
  end if;
  if not coalesce(c.privacy_gate_passed,false)
     or not coalesce(c.sensitivity_gate_passed,false)
     or not coalesce(c.minimum_necessary_passed,false)
     or not coalesce(c.visibility_gate_passed,false) then
    raise exception 'memory policy evidence incomplete';
  end if;

  insert into public.durable_memories(
    child_id, source_candidate_id, memory_type, content,
    valence, importance, confidence, occurred_at
  ) values (
    c.child_id, c.id, c.memory_type, c.content,
    c.valence, c.importance, 1.000, c.created_at
  )
  on conflict (source_candidate_id) do update
    set content = excluded.content,
        memory_type = excluded.memory_type,
        valence = excluded.valence,
        importance = excluded.importance,
        updated_at = now()
  returning id into v_id;

  return v_id;
end;
$$;

comment on function public.promote_memory_candidate_shadow_v2(uuid) is
'SHADOW ONLY. Fail-closed promotion requiring verified child-direct actor evidence and canonical memory policy gate evidence. Must not replace legacy promotion until runtime identity and policy decision producers are live and regression-tested.';
