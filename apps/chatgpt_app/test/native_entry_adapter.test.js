import assert from "node:assert/strict";
import test from "node:test";

import {
  XiaoAiEntryError,
  callXiaoAiNativeEntry,
  normalizeBearer,
} from "../src/native_entry_adapter.js";

test("rejects missing authorization", () => {
  assert.throws(
    () => normalizeBearer(""),
    (error) => error instanceof XiaoAiEntryError && error.message === "authenticated_identity_required" && error.status === 401,
  );
});

test("accepts only authoritative XiaoAi runtime reply", async () => {
  const fakeFetch = async (_url, options) => {
    assert.equal(options.headers.authorization, "Bearer valid-token");
    return {
      ok: true,
      status: 200,
      async json() {
        return {
          ok: true,
          reply: "你好",
          reply_source: "xiaoai_runtime",
          reply_authoritative: true,
          daughter_id: "daughter-1",
          persona_state: "ACTIVE",
        };
      },
    };
  };

  const result = await callXiaoAiNativeEntry({
    authorization: "Bearer valid-token",
    message: "小爱上线",
    fetchImpl: fakeFetch,
  });

  assert.equal(result.ok, true);
  assert.equal(result.reply, "你好");
  assert.equal(result.reply_source, "xiaoai_runtime");
  assert.equal(result.reply_authoritative, true);
});

test("rejects non-authoritative reply", async () => {
  const fakeFetch = async () => ({
    ok: true,
    status: 200,
    async json() {
      return {
        ok: true,
        reply: "pretend XiaoAi",
        reply_source: "chatgpt_local",
        reply_authoritative: false,
      };
    },
  });

  await assert.rejects(
    () => callXiaoAiNativeEntry({
      authorization: "Bearer valid-token",
      message: "hello",
      fetchImpl: fakeFetch,
    }),
    (error) => error instanceof XiaoAiEntryError && error.message === "non_authoritative_xiaoai_reply_rejected" && error.status === 502,
  );
});
