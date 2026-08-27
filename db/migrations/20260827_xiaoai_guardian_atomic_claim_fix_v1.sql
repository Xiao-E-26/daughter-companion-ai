-- Applied to Supabase project daughter-companion-ai on 2026-08-27.
-- Fixes atomic Guardian claim prerequisite without deleting data or changing Behavior Logic.

do $$ begin
  if not exists (
    select 1 from pg_constraint
    where conrelid='public.guardians'::regclass
      and conname='guardians_user_id_key'
  ) then
    alter table public.guardians
      add constraint guardians_user_id_key unique (user_id);
  end if;
end $$;
