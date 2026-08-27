# Spotify Music Tool V1

## Goal
Add Spotify as an external music capability for XiaoAi without creating a second persona, second behavior system, or alternate runtime.

## Architectural rule
XiaoAi remains one system:

`Chat/Voice input -> existing XiaoAi Runtime -> music intent/tool routing -> Spotify adapter -> Spotify playback`

The Spotify integration is a tool only. It must not replace or bypass the existing Behavior Core, Memory, Session, Context, or safety rules.

## Supported intents (V1)
- play a specific song
- play a specific artist
- play a calm / happy / bedtime style request
- pause
- resume
- next track
- previous track
- set playback volume

## Example
User: `我要听安静的歌`

Runtime behavior:
1. XiaoAi interprets the request and chooses an appropriate track or Spotify search query.
2. Runtime calls the `music.spotify` tool.
3. Spotify adapter resolves a playable item.
4. Playback starts on an available Spotify device.
5. XiaoAi responds naturally, e.g. `好呀，小爱帮你放一首安静的。`

## Tool contract
Suggested logical interface:

```text
music.spotify.search(query, type)
music.spotify.play(uri | context_uri, device_id?)
music.spotify.pause(device_id?)
music.spotify.resume(device_id?)
music.spotify.next(device_id?)
music.spotify.previous(device_id?)
music.spotify.set_volume(percent, device_id?)
music.spotify.devices()
```

## Authentication
Use Spotify OAuth. Do not store user passwords.

Required scopes should be kept minimal and only added as needed. Typical playback-control scopes may include:
- `user-read-playback-state`
- `user-modify-playback-state`

If search or library features are added later, request only the additional scopes required for those features.

## Runtime guardrails
- Do not modify the frozen Behavior Core.
- Do not create a Voice-only Spotify persona or path.
- Voice and text must invoke the same music tool.
- If no Spotify device is available, XiaoAi should say playback cannot start yet and may ask the user to open Spotify on a device.
- Never claim a song started unless Spotify returns a successful playback result.
- Never persist OAuth access tokens in logs, prompts, or long-term memory.

## State model
The runtime may keep short-lived session state for:
- active Spotify device
- current track URI
- last successful music intent

These are operational session values, not durable child-memory facts.

## Failure behavior
If Spotify returns an error:
- authentication expired -> request re-authentication
- no active device -> ask the user to open Spotify on a device
- item unavailable -> offer another version or song
- rate limited -> retry according to Spotify response headers; do not spin in a tight loop

## Implementation boundary
V1 should be introduced as an isolated adapter/tool layer and validated in shadow/dry-run mode first. No production deployment should be required just to land this design.

## Acceptance tests
1. `播放 River Flows in You` routes to Spotify search/play.
2. `我要听安静的歌` resolves a suitable search/query and plays one result.
3. `暂停` pauses the current Spotify device.
4. `下一首` advances playback.
5. No active Spotify device produces a graceful XiaoAi response instead of a false success claim.
6. Voice and text use the exact same runtime tool path.
7. No Behavior Core file is modified.
