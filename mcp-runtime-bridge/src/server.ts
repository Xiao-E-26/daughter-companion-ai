import express from "express";

const PORT = Number(process.env.PORT || 8787);
const SUPABASE_URL = process.env.SUPABASE_URL || "https://vmegjuceiuplqixizwso.supabase.co";
const XIAOAI_RUNTIME_URL = `${SUPABASE_URL}/functions/v1/xiaoai-mcp-runtime`;

const app = express();
app.use(express.json({ limit: "1mb" }));

app.get("/health", (_req, res) => {
  res.json({
    ok: true,
    service: "xiaoai-runtime-bridge",
    mode: "compatibility_proxy",
    canonical_runtime: "xiaoai-mcp-runtime",
    conversational_brain: "connected_chatgpt",
  });
});

app.all("/mcp", async (req, res) => {
  try {
    const authorization = req.header("authorization");
    const upstreamHeaders: Record<string, string> = {
      "content-type": "application/json",
    };
    if (authorization) upstreamHeaders.authorization = authorization;

    const upstream = await fetch(XIAOAI_RUNTIME_URL, {
      method: req.method,
      headers: upstreamHeaders,
      body: ["GET", "HEAD"].includes(req.method) ? undefined : JSON.stringify(req.body ?? {}),
    });

    const body = await upstream.text();
    res.status(upstream.status);
    const contentType = upstream.headers.get("content-type");
    if (contentType) res.setHeader("content-type", contentType);
    res.send(body);
  } catch (error) {
    const message = error instanceof Error ? error.message : "runtime_proxy_failed";
    res.status(502).json({ error: message });
  }
});

app.listen(PORT, () => {
  console.log(`xiaoai-runtime-bridge compatibility proxy listening on :${PORT}`);
});
