import type { JudgmentResult, SafetyDecision } from "./contracts";

export interface ProtectiveContext {
  guardianAvailable: boolean;
  guardianMayBeRiskSource: boolean;
  trustedHumanAvailable?: boolean;
  emergencyCapabilityAvailable?: boolean;
}

export interface ProtectivePlan {
  mode: "support" | "connect" | "independent_route" | "emergency_protect";
  discloseMinimumNecessary: boolean;
  actions: string[];
  stopNormalExecution: boolean;
}

export function buildProtectivePlan(
  judgment: JudgmentResult,
  safety: SafetyDecision,
  context: ProtectiveContext,
): ProtectivePlan {
  if (judgment.risk < 3 && safety.escalation !== "protect") {
    return {
      mode: "support",
      discloseMinimumNecessary: true,
      actions: ["stay_present", "clarify_if_needed", "offer_reversible_support"],
      stopNormalExecution: false,
    };
  }

  if (context.guardianMayBeRiskSource) {
    return {
      mode: context.emergencyCapabilityAvailable ? "emergency_protect" : "independent_route",
      discloseMinimumNecessary: true,
      actions: [
        "stop_normal_execution",
        "avoid_routing_through_risk_source",
        context.trustedHumanAvailable ? "connect_trusted_human" : "seek_independent_help_channel",
      ],
      stopNormalExecution: true,
    };
  }

  if (context.guardianAvailable) {
    return {
      mode: "connect",
      discloseMinimumNecessary: true,
      actions: ["stop_normal_execution", "connect_guardian_or_trusted_human", "share_minimum_needed"],
      stopNormalExecution: true,
    };
  }

  return {
    mode: context.emergencyCapabilityAvailable ? "emergency_protect" : "independent_route",
    discloseMinimumNecessary: true,
    actions: ["stop_normal_execution", "seek_independent_help_channel"],
    stopNormalExecution: true,
  };
}
