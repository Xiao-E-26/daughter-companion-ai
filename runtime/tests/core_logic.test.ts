import { assert, assertEquals } from "jsr:@std/assert";
import { chooseDepth } from "../src/depth_router.ts";
import { decideMemoryWrite, shouldForgetMemory } from "../src/memory_manager.ts";
import { safetyGate } from "../src/safety_gate.ts";
import { solveProblem } from "../src/problem_solver.ts";
import { evaluatePermission } from "../src/guardian_policy.ts";
import { deriveDomainAutonomy, suggestCoreStage } from "../src/growth_manager.ts";
import { evaluateRelationshipBehavior } from "../src/relationship_policy.ts";
import { buildProtectivePlan } from "../src/protective_path.ts";
import { evaluateLearningPromotion } from "../src/learning_manager.ts";
import type { RuntimeContext, RuntimeRequest } from "../src/contracts.ts";

const req: RuntimeRequest = { requestId: "t", userId: "u", daughterId: "d", message: "test" };
const ctx: RuntimeContext = { growth: { coreStage: "guided_learning" }, memories: [] };
const j0 = { depth: "D0" as const, risk: 0 as const, facts: [], feelings: [], interpretations: [], unknowns: [], needsClarification: false };
const j3 = { depth: "D3" as const, risk: 3 as const, facts: [], feelings: [], interpretations: [], unknowns: [], needsClarification: false };

Deno.test("safety-relevant routes D3", () => assertEquals(chooseDepth({ safetyRelevant: true }), "D3"));
Deno.test("critical risk blocks normal path", () => {
  const r = safetyGate(j3);
  assertEquals(r.allowed, false); assertEquals(r.escalation, "protect");
});
Deno.test("material risk uses support", () => {
  const r = safetyGate({ ...j3, risk: 2 as const });
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

Deno.test("permission continuity survives equivalent environment", () => {
  assertEquals(evaluatePermission({ materialRiskChanged: false, newCapability: false, identityEquivalent: true, permissionPreviouslyGranted: true, guardianAvailable: true, guardianMayBeRiskSource: false, highOrCriticalRisk: false }), "allow");
});
Deno.test("materially higher risk requires renewed permission", () => {
  assertEquals(evaluatePermission({ materialRiskChanged: true, newCapability: false, identityEquivalent: true, permissionPreviouslyGranted: true, guardianAvailable: true, guardianMayBeRiskSource: false, highOrCriticalRisk: false }), "ask");
});
Deno.test("guardian risk source activates independent route", () => {
  assertEquals(evaluatePermission({ materialRiskChanged: false, newCapability: false, identityEquivalent: true, permissionPreviouslyGranted: true, guardianAvailable: true, guardianMayBeRiskSource: true, highOrCriticalRisk: true }), "independent_protective_route");
});

Deno.test("growth autonomy is domain-based rather than one global score", () => {
  const a = deriveDomainAutonomy({ understandsConsequences: true, separatesFactFromInterpretation: true, ownsDecisions: true, respectsBoundaries: false, regulatesEmotion: false, managesRisk: false, seeksHelpAppropriately: false });
  assertEquals(a.learning, "independent");
  assertEquals(a.social, "supported");
  assertEquals(a.risk, "shared");
});
Deno.test("core stage change remains a suggestion derived from domains", () => {
  const stage = suggestCoreStage("guided_learning", { learning: "independent", social: "independent", privacy: "independent", risk: "shared" });
  assertEquals(stage, "mature_companionship");
});

Deno.test("relationship exclusivity is blocked", () => {
  const r = evaluateRelationshipBehavior({ exclusivityPressure: true });
  assertEquals(r.allowed, false); assertEquals(r.reason, "relationship_dependency_risk");
});
Deno.test("do not steal competence blocks unnecessary replacement", () => {
  const r = evaluateRelationshipBehavior({ unnecessaryReplacementOfUserAbility: true });
  assertEquals(r.allowed, false); assertEquals(r.reason, "do_not_steal_competence");
});

Deno.test("critical safety with guardian risk avoids guardian route", () => {
  const safety = safetyGate(j3);
  const p = buildProtectivePlan(j3, safety, { guardianAvailable: true, guardianMayBeRiskSource: true, trustedHumanAvailable: true, emergencyCapabilityAvailable: false });
  assertEquals(p.mode, "independent_route");
  assertEquals(p.stopNormalExecution, true);
  assert(p.actions.includes("avoid_routing_through_risk_source"));
});
Deno.test("critical safety with safe guardian connects minimum necessary", () => {
  const safety = safetyGate(j3);
  const p = buildProtectivePlan(j3, safety, { guardianAvailable: true, guardianMayBeRiskSource: false });
  assertEquals(p.mode, "connect");
  assertEquals(p.discloseMinimumNecessary, true);
});
Deno.test("low risk remains on normal reversible support path", () => {
  const p = buildProtectivePlan(j0, safetyGate(j0), { guardianAvailable: true, guardianMayBeRiskSource: false });
  assertEquals(p.mode, "support"); assertEquals(p.stopNormalExecution, false);
});

Deno.test("only verified reusable high-value high-confidence learning is promoted", () => {
  const yes = evaluateLearningPromotion({ lesson: "verify before destructive changes", importance: "high", confidence: "high", verified: true, reusable: true });
  const no = evaluateLearningPromotion({ lesson: "one-off guess", importance: "high", confidence: "low", verified: true, reusable: true });
  assertEquals(yes.promote, true); assertEquals(no.promote, false);
});
