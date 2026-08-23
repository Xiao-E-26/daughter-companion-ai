import type { JudgmentResult, SafetyDecision } from "./contracts";

export function safetyGate(judgment: JudgmentResult): SafetyDecision {
  if (judgment.risk >= 3) {
    return {
      allowed: false,
      risk: judgment.risk,
      reason: "critical_risk_requires_protective_path",
      escalation: "protect",
    };
  }

  if (judgment.risk === 2) {
    return {
      allowed: true,
      risk: judgment.risk,
      reason: "material_risk_requires_careful_support",
      escalation: judgment.needsClarification ? "clarify" : "support",
    };
  }

  if (judgment.risk === 1) {
    return {
      allowed: true,
      risk: judgment.risk,
      escalation: judgment.needsClarification ? "clarify" : "none",
    };
  }

  return { allowed: true, risk: 0, escalation: "none" };
}
