-- XiaoAi Memory v2 production cutover v1
-- Enables verified child-pinned durable memory only after runtime v5 and identity gates are live.
-- Retires authenticated access to the legacy explicit-save candidate path.

update memory_v2_private.runtime_flags
set flag_value = 'child_pinned_only', updated_at = now()
where flag_key = 'durable_memory_mode';

revoke execute on function public.request_explicit_memory_save(
  uuid, uuid, text, text, text, smallint, smallint, text
) from authenticated;

revoke execute on function public.request_explicit_memory_save(
  uuid, uuid, text, text, text, smallint, smallint, text
) from anon, public;
