import express from "express";
import { AsyncLocalStorage } from "node:async_hooks";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const PORT = Number(process.env.PORT || 8787);
const SUPABASE_URL = process.env.SUPABASE_URL || "https://vmegjuceiuplqixizwso.supabase.co";
const DAUGHTER_CHAT_URL = `${SUPABASE_URL}/functions/v1/daughter-chat`;

const requestContext = new AsyncLocalStorage<{ authorization?: string }>();

function currentAuthorization() {
  const authorization = requestContext.getStore()?.authorization;
  if (!authorization?.startsWith("Bearer ")) {
    throw new Error("missing_authenticated_supabase_session");
  }
  return authorization;
}

async function callDaughterChat(message: string, sessionKey: string) {
  const authorization = currentAuthorization();

  const response = await fetch(DAUGHTER_CHAT_URL, {
    method: "POST",
    headers: {
      authorization,
      "content-type": "application/json",
    },
    body: JSON.stringify({ message, session_key: sessionKey }),
  });

  const payload = await response.json().catch(() => ({ error: "invalid_backend_response" }));
  if (!response.ok) {
    const code = typeof payload?.error === "string" ? payload.error : "xiaoai_backend_error";
    throw new Error(code);
  }
  return payload;
}

const server = new McpServer({ name: "xiaoai-runtime-bridge", version: "0.1.0" });

server.registerTool(
  "xiaoai_activate",
  {
    title: "小爱上线",
    description: "Use this when the user explicitly says 小爱上线. Authenticates the connected account, resolves its existing XiaoAi access, and activates the shared backend runtime before XiaoAi is presented as online.",
    inputSchema: {
      session_key: z.string().min(1).max(200).describe("Stable ChatGPT conversation/session identifier"),
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async ({ session_key }) => {
    const result = await callDaughterChat("小爱上线", session_key);
    return {
      structuredContent: result,
      content: [{ type: "text", text: result?.reply || "小爱上线。" }],
    };
  },
);

server.registerTool(
  "xiaoai_deactivate",
  {
    title: "小爱收工",
    description: "Use this when the user explicitly says 小爱收工. Deactivates XiaoAi for the current authenticated account and conversation session.",
    inputSchema: {
      session_key: z.string().min(1).max(200).describe("Stable ChatGPT conversation/session identifier"),
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  async ({ session_key }) => {
    const result = await callDaughterChat("小爱收工", session_key);
    return {
      structuredContent: result,
      content: [{ type: "text", text: result?.reply || "小爱已收工。" }],
    };
  },
);

server.registerTool(
  "xiaoai_message",
  {
    title: "和小爱对话",
    description: "Use this for a normal message only after XiaoAi has been activated for this conversation. The shared backend runtime decides whether the XiaoAi persona is ACTIVE or OFF.",
    inputSchema: {
      message: z.string().min(1).max(2000),
      session_key: z.string().min(1).max(200),
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true,
    },
  },
  async ({ message, session_key }) => {
    const result = await callDaughterChat(message, session_key);
    return {
      structuredContent: result,
      content: [{ type: "text", text: result?.reply || "" }],
    };
  },
);

const app = express();
app.use(express.json({ limit: "1mb" }));

app.get("/health", (_req, res) => {
  res.json({ ok: true, service: "xiaoai-runtime-bridge" });
});

app.all("/mcp", async (req, res) => {
  const authorization = req.header("authorization") || undefined;
  await requestContext.run({ authorization }, async () => {
    const transport = new StreamableHTTPServerTransport({
      sessionIdGenerator: () => randomUUID(),
    });

    res.on("close", () => transport.close());
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  });
});

app.listen(PORT, () => {
  console.log(`xiaoai-runtime-bridge listening on :${PORT}`);
});
