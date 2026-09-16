-- XiaoAi Memory V1 residual cleanup v1
-- Safe production cleanup after Memory V2 cutover.
-- No CASCADE: unexpected dependencies must fail closed.

create or replace function public.bootstrap_xiaoai_identity(
  p_guardian_display_name text,
  p_child_display_name text,
  p_child_birth_date date default null,
  p_locale text default 'zh-MY',
  p_timezone text default 'Asia/Kuala_Lumpur'
)
returns table(guardian_user_id uuid, child_id uuid, session_id uuid)
language plpgsql
set search_path = public
as $$
declare
  v_uid uuid;
  v_child uuid;
  v_session uuid;
begin
  v_uid := auth.uid();
  if v_uid is null then
    raise exception 'authenticated user required';
  end if;

  insert into public.guardian_profiles(user_id, display_name, locale, timezone)
  values (
    v_uid,
    nullif(trim(p_guardian_display_name),''),
    coalesce(nullif(trim(p_locale),''),'zh-MY'),
    coalesce(nullif(trim(p_timezone),''),'Asia/Kuala_Lumpur')
  )
  on conflict (user_id) do update
    set display_name = excluded.display_name,
        locale = excluded.locale,
        timezone = excluded.timezone,
        updated_at = now();

  select c.id into v_child
  from public.child_profiles c
  where c.guardian_id = v_uid
    and lower(c.display_name) = lower(trim(p_child_display_name))
  order by c.created_at asc
  limit 1;

  if v_child is null then
    insert into public.child_profiles(guardian_id, display_name, birth_date, locale, timezone)
    values (
      v_uid,
      trim(p_child_display_name),
      p_child_birth_date,
      coalesce(nullif(trim(p_locale),''),'zh-MY'),
      coalesce(nullif(trim(p_timezone),''),'Asia/Kuala_Lumpur')
    )
    returning id into v_child;
  else
    update public.child_profiles
       set birth_date = coalesce(p_child_birth_date, birth_date),
           locale = coalesce(nullif(trim(p_locale),''), locale),
           timezone = coalesce(nullif(trim(p_timezone),''), timezone),
           updated_at = now()
     where id = v_child;
  end if;

  insert into public.chat_sessions(child_id, channel)
  values (v_child, 'system')
  returning id into v_session;

  return query select v_uid, v_child, v_session;
end;
$$;

create or replace function public.log_safety_event(
  p_child_id uuid,
  p_session_id uuid,
  p_category text,
  p_severity smallint,
  p_summary text
)
returns uuid
language plpgsql
set search_path = public
as $$
declare
  v_id uuid;
begin
  if length(trim(coalesce(p_summary,''))) = 0 then
    raise exception 'safety summary cannot be empty';
  end if;
  if length(p_summary) > 2000 then
    raise exception 'safety summary too long';
  end if;

  insert into public.safety_events(child_id, session_id, category, severity, summary)
  values (p_child_id, p_session_id, p_category, p_severity, trim(p_summary))
  returning id into v_id;

  return v_id;
end;
$$;

do $$
declare
  v_jobid bigint;
begin
  select jobid into v_jobid from cron.job where jobname='xiaoi-memory-jobs' limit 1;
  if v_jobid is not null then
    perform cron.unschedule(v_jobid);
  end if;
end;
$$;

drop trigger if exists trg_queue_memory_job on public.memory_candidates;
drop function if exists public.queue_memory_job();
drop function if exists public.process_memory_jobs(integer);
drop function if exists public.auto_process_memory_candidates(uuid);
drop function if exists public.enqueue_memory_candidate(uuid,uuid,text,text,smallint,smallint,boolean);
drop function if exists public.enqueue_memory_candidate_v2(uuid,uuid,text,text,smallint,smallint,boolean,text);
drop function if exists public.promote_memory_candidate(uuid);
drop function if exists public.request_explicit_memory_save(uuid,uuid,text,text,text,smallint,smallint,text);
drop function if exists public.recall_memories(uuid,integer,text[]);

-- Dependency-safe order; deliberately no CASCADE.
drop table if exists public.memory_jobs;
drop table if exists public.durable_memories;
drop table if exists public.memory_candidates;
drop table if exists public.memory_policy;
drop table if exists public.memory_save_phrases;
