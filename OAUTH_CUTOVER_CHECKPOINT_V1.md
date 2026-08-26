# XiaoAi OAuth Cutover Checkpoint v1

## Completed

- Mother Guardian binding: complete and frozen.
- `daughter-chat`: existing authenticated runtime primitive.
- `xiaoai-mcp-runtime`: deployed as Supabase Edge Function, ACTIVE v2.
- MCP tools: `xiaoai_activate`, `xiaoai_deactivate`, `xiaoai_message`.
- MCP protected-resource metadata and 401 `WWW-Authenticate` challenge added.
- Standalone OAuth consent page committed to GitHub and GitHub Pages deployment succeeded.
- `xiaoai-guardian-confirmed` upgraded to v2 and still preserves its original default confirmation response while also serving a consent UI on `/oauth/consent`.
- No service-role key is exposed client-side.

## Public endpoints

MCP resource:
`https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-mcp-runtime`

Supabase Auth issuer:
`https://vmegjuceiuplqixizwso.supabase.co/auth/v1`

GitHub Pages base:
`https://xiao-e-26.github.io/daughter-companion-ai/`

GitHub Pages consent page:
`https://xiao-e-26.github.io/daughter-companion-ai/oauth/consent.html`

Existing Site URL / guardian confirmation endpoint:
`https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-guardian-confirmed`

Consent-capable route added to the same Edge Function:
`https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-guardian-confirmed/oauth/consent`

## Remaining manual control-plane steps

These are Supabase Dashboard / ChatGPT UI settings and are not writable through the currently connected project tools.

1. Supabase Dashboard -> Authentication -> OAuth Server
   - Enable OAuth 2.1 Server.
   - Configure the Authorization Path only after confirming how the dashboard combines it with the current Site URL.
   - Prefer a path that resolves to a tested consent page without changing the already-working guardian verification behavior.
   - For initial MCP testing, dynamic client registration may be enabled. Before broader use, review whether to keep it enabled.

2. ChatGPT -> Developer Mode / Apps & Connectors
   - Add the remote MCP server URL:
     `https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-mcp-runtime`
   - Complete the Supabase OAuth authorization flow for each ChatGPT account separately.

3. Runtime verification
   - From the Mother ChatGPT account, call `小爱上线` through the connected MCP app.
   - Verify that exactly one runtime session is created/updated for the existing Mother Guardian user and existing mother `client_connections` row.
   - Do not create a new guardian identity.
   - Then test a normal XiaoAi message and `小爱收工`.

## Safety rules

- Do not send or recreate guardian invitations.
- Do not fabricate `runtime_sessions` for testing.
- Do not hard-code a mother/user ID into MCP requests.
- Identity must come from the authenticated Supabase OAuth access token.
- Do not expose service-role, secret, or management credentials in browser code or ChatGPT configuration.
- Preserve cross-account visibility restrictions and minimum-necessary retrieval.
