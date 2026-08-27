const DEFAULT_NATIVE_ENTRY_URL = "https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-native-entry-shadow";
const DEFAULT_SESSION_KEY = "xiaoai-current";

export class XiaoAiEntryError extends Error {
  constructor(message, status = 500, details = null) {
    super(message);
    this.name = "XiaoAiEntryError";
    this.status = status;
    this.details = details;
  }
}

export function normalizeBearer(authorization) {
  if (typeof authorization !== "string" || !authorization.startsWith("Bearer ")) {
    throw new XiaoAiEntryError("authenticated_identity_required", 401);
  }
  const token = authorization.slice(7).trim();
  if (!token) throw new XiaoAiEntryError("authenticated_identity_required", 401);
  return `Bearer ${token}`;
}

export function normalizeMessage(message) {
  if (typeof message !== "string" || !message.trim()) {
    throw new XiaoAiEntryError("message_required", 400);
  }
  return message.trim().slice(0, 2000);
}

export function normalizeSessionKey(sessionKey) {
  if (typeof sessionKey !== "string" || !sessionKey.trim()) return DEFAULT_SESSION_KEY;
  return sessionKey.trim().slice(0, 200);
}

export async function callXiaoAiNativeEntry({
  authorization,
  message,
  sessionKey,
  fetchImpl = fetch,
  nativeEntryUrl = process.env.XIAOAI_NATIVE_ENTRY_URL || DEFAULT_NATIVE_ENTRY_URL,
}) {
  const bearer = normalizeBearer(authorization);
  const cleanMessage = normalizeMessage(message);
  const cleanSessionKey = normalizeSessionKey(sessionKey);

  const response = await fetchImpl(nativeEntryUrl, {
    method: "POST",
    headers: {
      authorization: bearer,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      message: cleanMessage,
      session_key: cleanSessionKey,
      identity: "xiaoai",
    }),
  });

  const payload = await response.json().catch(() => null);

  if (!response.ok || !payload?.ok) {
    throw new XiaoAiEntryError(
      payload?.error || "xiaoai_native_entry_failed",
      response.status || 502,
      payload,
    );
  }

  if (
    payload.reply_authoritative !== true ||
    payload.reply_source !== "xiaoai_runtime" ||
    typeof payload.reply !== "string" ||
    !payload.reply.trim()
  ) {
    throw new XiaoAiEntryError("non_authoritative_xiaoai_reply_rejected", 502, payload);
  }

  return {
    ok: true,
    reply: payload.reply,
    reply_source: payload.reply_source,
    reply_authoritative: true,
    daughter_id: payload.daughter_id ?? null,
    persona_state: payload.persona_state ?? null,
    transition: payload.transition ?? null,
    session_key: payload.session_key ?? cleanSessionKey,
    provider: payload.provider ?? null,
    model: payload.model ?? null,
  };
}
