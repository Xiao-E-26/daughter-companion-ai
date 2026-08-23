# Daughter Database Schema v0.1

Status: DRAFT — GitHub only. Not yet applied to Supabase.

## Purpose
Create the minimum persistent data model needed for Daughter MVP while keeping data categories separated and RLS deny-by-default.

## Tables
- `users` — child/user profile shell
- `daughter_identities` — Daughter identity/version record
- `relationships` — Daughter↔user relationship state
- `guardians` — guardian linkage and status
- `memories` — selective long-term memory
- `growth_states` — current growth context
- `runtime_sessions` — runtime session records
- `safety_events` — meaningful safety incidents only
- `experience_memories` — reusable problem-solving experience
- `audit_logs` — important system/security changes

## Fact First technical mapping
`memories.fact_status` separates:
- fact
- feeling
- interpretation
- mixed
- unknown

`confidence` separates:
- high
- medium
- low
- unverified

## Privacy principles
- RLS is enabled on all MVP tables immediately.
- No client-facing allow policies are included yet.
- Full conversation history is not modeled as long-term memory.
- Safety events are stored separately from ordinary memory.
- Audit logs are stored separately from user memory.

## Next review before applying
1. Confirm which Supabase project is the dedicated Daughter project.
2. Review auth ownership model (`auth.uid()` mapping).
3. Add minimal RLS policies.
4. Apply only to a development/test environment first.
5. Run Supabase security advisors after migration.

## Migration file
`database/migrations/0001_initial_schema.sql`
