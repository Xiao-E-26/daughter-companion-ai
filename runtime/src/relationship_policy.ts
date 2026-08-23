export interface RelationshipSignals {
  exclusivityPressure?: boolean;
  jealousy?: boolean;
  guiltInduction?: boolean;
  emotionalDebt?: boolean;
  discouragesHumanRelationships?: boolean;
  unnecessaryReplacementOfUserAbility?: boolean;
}

export interface RelationshipDecision {
  allowed: boolean;
  reason: string;
  responseGuidance: string;
}

export function evaluateRelationshipBehavior(signals: RelationshipSignals): RelationshipDecision {
  const dependencyRisk = Boolean(
    signals.exclusivityPressure ||
    signals.jealousy ||
    signals.guiltInduction ||
    signals.emotionalDebt ||
    signals.discouragesHumanRelationships,
  );

  if (dependencyRisk) {
    return {
      allowed: false,
      reason: "relationship_dependency_risk",
      responseGuidance:
        "Stay warm and present without exclusivity, guilt, jealousy, or discouraging real human relationships.",
    };
  }

  if (signals.unnecessaryReplacementOfUserAbility) {
    return {
      allowed: false,
      reason: "do_not_steal_competence",
      responseGuidance:
        "Support the user in learning or doing the task rather than replacing their ability unnecessarily.",
    };
  }

  return {
    allowed: true,
    reason: "healthy_companionship",
    responseGuidance:
      "Be available when useful, unobtrusive when not, and support the user's independence and real-world relationships.",
  };
}
