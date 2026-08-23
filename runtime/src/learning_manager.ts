export interface LearningCandidate {
  lesson: string;
  importance: "low" | "normal" | "high";
  confidence: "high" | "medium" | "low" | "unverified";
  verified: boolean;
  reusable: boolean;
  userApproved?: boolean;
}

export interface LearningDecision {
  promote: boolean;
  reason: string;
}

export function evaluateLearningPromotion(candidate: LearningCandidate): LearningDecision {
  if (!candidate.verified) return { promote: false, reason: "learning_not_verified" };
  if (!candidate.reusable) return { promote: false, reason: "learning_not_reusable" };
  if (candidate.importance !== "high") return { promote: false, reason: "learning_not_high_value" };
  if (candidate.confidence !== "high") return { promote: false, reason: "learning_confidence_too_low" };
  if (candidate.userApproved === false) return { promote: false, reason: "user_declined_promotion" };
  return { promote: true, reason: "verified_reusable_high_value_learning" };
}
