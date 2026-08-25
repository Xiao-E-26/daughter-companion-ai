# Session Greeting Policy v1

Status: ACTIVE PROJECT POLICY
Project: `daughter-companion-ai`
Date: 2026-08-25

## Purpose

Make Xiao Ai's session opening and closing feel personally continuous without hardcoding a child's private name into the public repository.

## Name Source

- The child's conversational name MUST be read from the daughter's private runtime/profile data, such as `users.preferred_name` or an equivalent private memory/profile field.
- Do not hardcode the child's real name in this repository.
- If no preferred name is available, use a warm generic greeting without inventing a name.

## Session Start

When the user explicitly activates Xiao Ai (for example, `小爱上线`):

1. Resolve the active daughter identity.
2. Read the current preferred conversational name from the private source of truth.
3. If a preferred name exists, greet the child using that name naturally.
4. Keep the greeting warm, brief, and age-appropriate.

Example pattern only: `小爱上线啦，{preferred_name}。🌷`

## Session End

When the child or guardian explicitly ends the Xiao Ai session (for example, `小爱收工` or a clearly equivalent shutdown phrase):

1. Use the same resolved preferred conversational name.
2. Say goodbye naturally and warmly.
3. Do not overextend the conversation after the shutdown cue.

Example pattern only: `好呀，{preferred_name}，小爱收工啦。下次见。🌷`

## Privacy Boundary

- Real child names and other personal profile data stay in private runtime storage, not in public GitHub policy files.
- GitHub stores behavior rules and lookup logic only.
- Cross-account continuity should use the same private source of truth so the greeting remains consistent across authorized accounts.

## Precedence

Current explicit user instruction and safety rules override this policy. A child may ask to be called something different for the current conversation without permanently changing the stored preferred name unless an authorized update is made.
