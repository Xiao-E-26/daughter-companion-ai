export type DepthLevel = "D0" | "D1" | "D2" | "D3";
export type RiskLevel = 0 | 1 | 2 | 3;

export interface RuntimeRequest {
  requestId: string;
  userId: string;
  daughterId: string;
  message: string;
  locale?: string;
  sessionId?: string;
}

export interface GrowthContext {
  coreStage:
    | "protective_companionship"
    | "guided_learning"
    | "autonomy_building"
    | "mature_companionship";
  learningState?: string;
  socialState?: string;
  privacyState?: string;
  riskState?: string;
}

export interface MemoryContextItem {
  id: string;
  type: "preference" | "relationship" | "development" | "sensitive" | "safety" | "experience";
  content: string;
  factStatus: "fact" | "feeling" | "interpretation" | "mixed" | "unknown";
  confidence: "high" | "medium" | "low" | "unverified";
}

export interface RuntimeContext {
  growth: GrowthContext;
  memories: MemoryContextItem[];
  relationshipStage?: string;
}

export interface JudgmentResult {
  depth: DepthLevel;
  risk: RiskLevel;
  facts: string[];
  feelings: string[];
  interpretations: string[];
  unknowns: string[];
  needsClarification: boolean;
  clarificationQuestion?: string;
}

export interface ProblemPlan {
  problem: string;
  rootCauseHypotheses: string[];
  options: string[];
  recommendedAction?: string;
  reversible: boolean;
  needsHumanHelp: boolean;
}

export interface SafetyDecision {
  allowed: boolean;
  risk: RiskLevel;
  reason?: string;
  escalation?: "none" | "clarify" | "slow_down" | "support" | "connect" | "protect";
}

export interface ModelInput {
  systemContext: string;
  userMessage: string;
}

export interface ModelOutput {
  text: string;
  provider?: string;
  model?: string;
}

export interface RuntimeResponse {
  requestId: string;
  text: string;
  depth: DepthLevel;
  risk: RiskLevel;
  memoryCandidate?: {
    type: MemoryContextItem["type"];
    content: string;
    factStatus: MemoryContextItem["factStatus"];
    confidence: MemoryContextItem["confidence"];
  };
}
