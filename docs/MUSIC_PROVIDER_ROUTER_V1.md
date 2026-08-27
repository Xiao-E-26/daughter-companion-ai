# Music Provider Router V1

## Goal
Generalize XiaoAi music playback from a Spotify-specific tool into one shared music capability with pluggable providers.

## Architectural rule
XiaoAi remains one Persona, one Behavior Core, one Runtime, one Memory/Session/Context system.

`Chat/Voice -> XiaoAi Runtime -> music intent -> Music Provider Router -> provider adapter -> playback`

Provider integrations are adapters only. They must never bypass the existing Behavior Core or create a provider-specific persona/runtime path.

## Unified music interface
Suggested logical contract:

```text
music.search(query, type?, provider?)
music.play(item_uri | context_uri, provider?, device_id?)
music.pause(provider?, device_id?)
music.resume(provider?, device_id?)
music.next(provider?, device_id?)
music.previous(provider?, device_id?)
music.set_volume(percent, provider?, device_id?)
music.devices(provider?)
```

The runtime should call the unified `music.*` interface. Provider-specific details stay behind adapters.

## Providers
### Spotify adapter
Wrap existing Spotify capability behind the unified interface.

### YouTube / YouTube Music adapter
Add a separate provider adapter for YouTube or YouTube Music where official capabilities permit.

Important: provider capability is not assumed to be identical to Spotify. Search, playback launch, device control, queue control, and background playback may differ depending on platform/API/account/device constraints.

The adapter must expose capability metadata so the router can avoid claiming unsupported actions.

Suggested capability flags:

```text
can_search
can_direct_play
can_pause
can_resume
can_next
can_previous
can_set_volume
can_list_devices
can_control_remote_device
```

## Provider selection
Default selection order should be configurable.

Suggested behavior:
1. If user explicitly names a provider, use it.
2. Otherwise use the user's preferred/default provider if available.
3. If unavailable, fall back to another authorized provider only when the requested action is supported.
4. Never silently claim fallback playback if no provider confirms success.

Examples:
- `用 YouTube 播 River Flows in You` -> YouTube provider.
- `Spotify 播` -> Spotify provider.
- `我要听安静的歌` -> use default provider and XiaoAi recommendation logic.
- If Spotify cannot find/play the requested item and YouTube is authorized, router may offer or execute fallback according to configured policy.

## Authentication and security
- Provider credentials/tokens are isolated per adapter.
- Never store access/refresh tokens in prompts, logs, durable child memory, or conversational memory.
- Use least-privilege scopes.
- Authentication state is operational state only.

## Session state
Short-lived operational state may include:
- active provider
- active device/session target
- current media item
- previous successful provider
- provider capability snapshot

These are not durable child-memory facts.

## Failure behavior
The router must preserve truthful execution semantics:
- unauthorized provider -> request authorization
- unsupported action -> explain limitation or select another capable provider when policy allows
- no active device/session -> ask user to open/activate the provider where required
- media unavailable -> offer another result/provider
- playback API failure -> report failure; do not say playback started

## Voice/text consistency
Voice and text must call the same `music.*` interface and the same provider router. No Voice-only music path.

## Migration from Spotify V1
The existing Spotify V1 design remains valid as a provider adapter definition, but runtime-facing calls should migrate from `music.spotify.*` to unified `music.*` calls.

No frozen Behavior Core changes are required.

## Acceptance tests
1. `播放 River Flows in You` uses the configured default provider.
2. `用 Spotify 播 River Flows in You` routes explicitly to Spotify.
3. `用 YouTube 播 River Flows in You` routes explicitly to YouTube/YouTube Music adapter.
4. `我要听安静的歌` performs XiaoAi recommendation logic, then uses the selected provider.
5. Unsupported YouTube control actions never return false success.
6. Spotify failure may trigger a policy-approved YouTube fallback only when YouTube is authorized and capable.
7. Voice and text traverse the same unified music interface.
8. No Behavior Core file is modified.

## Implementation boundary
Land this as an isolated router/provider design first. Provider OAuth and runtime playback implementations remain separate implementation steps and should be tested in shadow/dry-run mode before production rollout.
