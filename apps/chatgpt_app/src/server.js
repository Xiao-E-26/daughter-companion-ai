import express from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import { callXiaoAiNativeEntry, XiaoAiEntryError } from "./native_entry_adapter.js";

const app = express();
app.use(express.json({ limit: "256kb" }));

const PORT = Number(process.env.PORT || 3000);

function jsonError(res, status, error) {
  return res.status(status).json({ ok: false, error });
}

function createMcpServer(authorization) {
  const server = new McpServer({
    name: "xiaoai-chatgpt-app",
    version: "0.1.0",
  });

  server.registerTool(
    "xiaoai_message",
    {
      title: "Talk to XiaoAi",
      description:
        "Use this when an authorized user wants to activate XiaoAi, talk with XiaoAi, or deactivate XiaoAi. Forward the user's exact message to the authoritative XiaoAi Runtime. Do not imitate XiaoAi locally if the tool fails.",
      inputSchema: {
        message: z.string().min(1).max(2000),
        session_key: z.string().min(1).max(200).optional(),
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: false,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
    async ({ message, session_key }) => {
      try {
        const result = await callXiaoAiNativeEntry({
          authorization,
          message,
          sessionKey: session_key,
        });

        return {
          content: [{ type: "text", text: result.reply }],
          structuredContent: result,
        };
      } catch (error) {
        const known = error instanceof XiaoAiEntryError;
        const code = known ? error.message : "xiaoai_entry_unavailable";
        return {
          isError: true,
          content: [{ type: "text", text: `XiaoAi unavailable: ${code}` }],
          structuredContent: {
            ok: false,
            error: code,
            reply_authoritative: false,
          },
        };
      }
    },
  );

  return server;
}

app.get("/health", (_req, res) => {
  res.json({
    ok: true,
    service: "xiaoai-chatgpt-app",
    persona_owned_here: false,
    memory_owned_here: false,
    runtime_authority: "xiaoai_native_entry",
  });
});

app.post("/mcp", async (req, res) => {
  const authorization = req.get("authorization") || "";
  if (!authorization.startsWith("Bearer ")) {
    return jsonError(res, 401, "authenticated_identity_required");
  }

  const server = createMcpServer(authorization);
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
  });

  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    if (!res.headersSent) {
      jsonError(res, 500, "mcp_request_failed");
    }
  } finally {
    await transport.close().catch(() => {});
    await server.close().catch(() => {});
  }
});

app.get("/mcp", (_req, res) => jsonError(res, 405, "method_not_allowed"));
app.delete("/mcp", (_req, res) => jsonError(res, 405, "method_not_allowed"));

app.listen(PORT, "0.0.0.0", () => {
  console.log(`xiaoai-chatgpt-app listening on ${PORT}`);
});
