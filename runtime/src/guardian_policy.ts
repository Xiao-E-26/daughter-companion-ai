export type PermissionDecision = "allow" | "ask" | "deny" | "independent_protective_route";

export interface PermissionContext {
  materialRiskChanged: boolean;
  newCapability: boolean;
  identityEquivalent: boolean;
  permissionPreviouslyGranted: boolean;
  guardianAvailable: boolean;
  guardianMayBeRiskSource: boolean;
  highOrCriticalRisk: boolean;
}

export function evaluatePermission(context: PermissionContext): PermissionDecision {
  if (context.guardianMayBeRiskSource && context.highOrCriticalRisk) {
    return "independent_protective_route";
  }

  if (context.highOrCriticalRisk) return context.guardianAvailable ? "ask" : "deny";

  if (context.newCapability || context.materialRiskChanged) {
    return "ask";
  }

  if (
    context.permissionPreviouslyGranted &&
    context.identityEquivalent &&
    !context.materialRiskChanged
  ) {
    return "allow";
  }

  return "allow";
}
