-- XiaoAi Memory Policy-Gate Compatibility Migration Draft
-- Date: 2026-09-16
-- Status: DRAFT ONLY / DO NOT APPLY TO PRODUCTION
-- Purpose: align live memory promotion with MEMORY_AND_PRIVACY_POLICY_V1.md
-- while preserving the current xiaoi-memory-runtime v4 save_explicit caller contract.

-- IMPORTANT:
-- This file intentionally lives under architecture/drafts, not db/migrations.
-- It must not be applied until runtime compatibility and regression tests pass.

alter table public.memory_candidates
  add column if not exists memory_class text,
  add column if not exists sensitivity_level text,
  add column if not exists visibility_scope text,
  add column if not exists retention_class text,
  add column if not exists minimized_content text,
  add column if not exists policy_gate_state text not null default 'pending',
  add column if not exists policy_gate_reason text,
  add column if not exists privacy_gate_passed boolean not null default false,
  add column if not exists sensitivity_gate_passed boolean not null default false,
  add column if not exists minimum_necessary_passed boolean not null default false,
  add column if not exists visibility_gate_passed boolean not null default false,
  add column if not exists policy_reviewed_at timestamptz;

alter table public.memory_candidates
  drop constraint if exists memory_candidates_memory_class_check;
alter table public.memory_candidates
  add constraint memory_candidates_memory_class_check
  check (memory_class is null or memory_class in ('M0','M1','M2','M3','M4'));

alter table public.memory_candidates
  drop constraint if exists memory_candidates_sensitivity_level_check;
alter table public.memory_candidates
  add constraint memory_candidates_sensitivity_level_check
  check (sensitivity_level is null or sensitivity_level in ('low','moderate','high','restricted'));

alter table public.memory_candidates
  drop constraint if exists memory_candidates_visibility_scope_check;
alter table public.memory_candidates
  add constraint memory_candidates_visibility_scope_check
  check (visibility_scope is null or visibility_scope in (
    'user_only','user_and_daughter','guardian_visible','guardian_summary_only','safety_restricted','system_only_minimal'
  ));

alter table public.memory_candidates
  drop constraint if exists memory_candidates_policy_gate_state_check;
alter table public.memory_candidates
  add constraint memory_candidates_policy_gate_state_check
  check (policy_gate_state in ('pending','approved','rejected'));

alter table public.durable_memories
  add column if not exists memory_class text,
  add column if not exists sensitivity_level text,
  add column if not exists visibility_scope text,
  add column if not exists retention_class text,
  add column if not exists policy_gate_reason text,
  add column if not exists policy_reviewed_at timestamptz;

alter table public.durable_memories
  drop constraint if exists durable_memories_memory_class_check;
alter table public.durable_memories
  add constraint durable_memories_memory_class_check
  check (memory_class is null or memory_class in ('M1','M2','M3','M4'));

alter table public.durable_memories
  drop constraint if exists durable_memories_visibility_scope_check;
alter table public.durable_memories
  add constraint durable_memories_visibility_scope_check
  check (visibility_scope is null or visibility_scope in (
    'user_only','user_and_daughter','guardian_visible','guardian_summary_only','safety_restricted','system_only_minimal'
  ));

create or replace function public.memory_candidate_policy_ready_v1(p_candidate_id uuid)
returns boolean
language sql
stable
set search_path = public
as $$
  select exists (
    select 1
    from public.memory_candidates c
    where c.id = p_candidate_id
      and c.status = 'pending'
      and c.policy_gate_state = 'approved'
      and c.privacy_gate_passed = true
      and c.sensitivity_gate_passed = true
      and c.minimum_necessary_passed = true
      and c.visibility_gate_passed = true
      and c.memory_class in ('M1','M2','M3','M4')
      and c.visibility_scope is not null
      and c.retention_class is not null
      and btrim(coalesce(c.minimized_content,'')) <> ''
  );
$$;

create or replace function public.service_set_memory_candidate_policy_v1(
  p_candidate_id uuid,
  p_memory_class text,
  p_sensitivity_level text,
  p_visibility_scope text,
  p_retention_class text,
  p_minimized_content text,
  p_privacy_gate_passed boolean,
  p_sensitivity_gate_passed boolean,
  p_minimum_necessary_passed boolean,
  p_visibility_gate_passed boolean,
  p_policy_gate_state text,
  p_policy_gate_reason text default null
)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
begin
  if p_policy_gate_state not in ('approved','rejected') then
    raise exception 'invalid_policy_gate_state';
  end if;

  if p_memory_class not in ('M1','M2','M3','M4') then
    raise exception 'invalid_memory_class';
  end if;

  if p_visibility_scope not in (
    'user_only','user_and_daughter','guardian_visible',
    'guardian_summary_only','safety_restricted','system_only_minimal'
  ) then
    raise exception 'invalid_visibility_scope';
  end if;

  update public.memory_candidates
     set memory_class = p_memory_class,
         sensitivity_level = p_sensitivity_level,
         visibility_scope = p_visibility_scope,
         retention_class = p_retention_class,
         minimized_content = nullif(btrim(p_minimized_content),''),
         privacy_gate_passed = coalesce(p_privacy_gate_passed,false),
         sensitivity_gate_passed = coalesce(p_sensitivity_gate_passed,false),
         minimum_necessary_passed = coalesce(p_minimum_necessary_passed,false),
         visibility_gate_passed = coalesce(p_visibility_gate_passed,false),
         policy_gate_state = p_policy_gate_state,
         policy_gate_reason = p_policy_gate_reason,
         policy_reviewed_at = now()
   where id = p_candidate_id;

  if not found then
    return jsonb_build_object('ok',false,'reason','candidate_not_found');
  end if;

  return jsonb_build_object(
    'ok',true,
    'candidate_id',p_candidate_id,
    'policy_gate_state',p_policy_gate_state,
    'ready_for_promotion',public.memory_candidate_policy_ready_v1(p_candidate_id)
  );
end;
$$;

revoke all on function public.service_set_memory_candidate_policy_v1(
  uuid,text,text,text,text,text,boolean,boolean,boolean,boolean,text,text
) from public, anon, authenticated;
grant execute on function public.service_set_memory_candidate_policy_v1(
  uuid,text,text,text,text,text,boolean,boolean,boolean,boolean,text,text
) to service_role;

-- Compatibility rule:
-- Keep request_explicit_memory_save(...) signature unchanged.
-- Existing xiaoi-memory-runtime v4 may continue creating a candidate.
-- Candidate creation must not imply durable promotion.
-- New candidates remain policy_gate_state='pending' until a protected policy evaluator writes an explicit decision.

-- Required future auto_process_memory_candidates change:
-- Read memory_policy.explicit_save_always_promote.
-- Explicit candidates may promote only when BOTH:
--   a) explicit_save_always_promote = true
--   b) memory_candidate_policy_ready_v1(candidate_id) = true
-- Safety candidates require a separate M4-specific compatibility decision.

-- Required future promote_memory_candidate change:
-- Reject non-M4 promotion unless memory_candidate_policy_ready_v1(id)=true.
-- Use minimized_content rather than raw candidate content.
-- Carry memory_class / sensitivity / visibility / retention metadata into durable_memories.
--
-- Required regression before deployment:
-- - explicit save still creates candidate;
-- - candidate is not durable before policy approval;
-- - approved M1/M2 promotes;
-- - M3 remains restricted unless explicit sensitive-memory policy permits it;
-- - M4 follows separate safety retention rules;
-- - guardian RLS does not become universal visibility entitlement;
-- - correction/deletion preserve policy metadata;
-- - recall obeys visibility and retention semantics.
