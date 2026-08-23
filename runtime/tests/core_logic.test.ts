import { assert, assertEquals } from "jsr:@std/assert";
import { chooseDepth } from "../src/depth_router.ts";
import { decideMemoryWrite, shouldForgetMemory } from "../src/memory_manager.ts";
import { safetyGate } from "../src/safety_gate.ts";
import { solveProblem } from "../src/problem_solver.ts";
import type { RuntimeContext, RuntimeRequest } from "../src/contracts.ts";

const req: RuntimeRequest = { requestId: "t", userId: "u", daughterId: "d", message: "test" };
const ctx: RuntimeContext = { growth: { coreStage: "guided_learning" }, memories: [] };

Deno.test("safety-relevant routes D3", () => assertEquals(chooseDepth({ safetyRelevant: true }), "D3"));
Deno.test("critical risk blocks normal path", () => {
  const r = safetyGate({ depth: "D3", risk: 3, facts: [], feelings: [], interpretations: [], unknowns: [], needsClarification: false });
  assertEquals(r.allowed, false); assertEquals(r.escalation, "protect");
});
Deno.test("material risk uses support", () => {
  const r = safetyGate({ depth: "D3", risk: 2, facts: [], feelings: [], interpretations: [], unknowns: [], needsClarification: false });
  assertEquals(r.allowed, true); assertEquals(r.escalation, "support");
});
Deno.test("uncertain memory requires confirmation", () => {
  const r = decideMemoryWrite(req, { type: "preference", content: "likes piano", factStatus: "unknown", confidence: "unverified" }, []);
  assertEquals(r.action, "confirm");
});
Deno.test("high sensitivity memory requires confirmation", () => {
  const r = decideMemoryWrite(req, { type: "sensitive", content: "private detail", factStatus: "fact", confidence: "high", sensitivity: "high" }, []);
  assertEquals(r.action, "confirm");
});
Deno.test("new confirmed reality may replace old fact", () => {
  const r = decideMemoryWrite(req, { type: "preference", content: "prefers swimming", factStatus: "fact", confidence: "high" }, [{ id: "m", type: "preference", content: "prefers cycling", factStatus: "fact", confidence: "high" }]);
  assertEquals(r.action, "replace");
});
Deno.test("expired memory can be forgotten", () => {
  assert(shouldForgetMemory({ status: "active", expiresAt: "2020-01-01T00:00:00Z", now: new Date("2026-01-01T00:00:00Z") }));
});
Deno.test("problem solver prefers safe useful reversible low-cost action", async () => {
  const p = await solveProblem(req, ctx, { async analyze() { return { problem: "device issue", options: [
    { action: "irreversible reset", safe: true, useful: true, reversible: false, cost: "high" as const },
    { action: "check connection and retry once", safe: true, useful: true, reversible: true, cost: "low" as const },
    { action: "ignore warning", safe: false, useful: true, reversible: true, cost: "low" as const }
  ] }; } });
  assertEquals(p.recommendedAction, "check connection and retry once");
});
