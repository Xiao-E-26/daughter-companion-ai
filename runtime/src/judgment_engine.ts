import { chooseDepth } from "./depth_router.ts";
import type { JudgmentResult, RuntimeContext, RuntimeRequest } from "./contracts.ts";

export interface JudgmentSignals {
  facts?: string[];
  feelings?: string[];
  interpretations?: string[];
  unknowns?: string[];
  emotionalIntensity?: "low" | "medium" | "high";
  consequenceLevel?: "low" | "medium" | "high";
  ambiguity?: "low" | "medium" | "high";
  safetyRelevant?: boolean;
  risk?: 0 | 1 | 2 | 3;
  clarificationQuestion?: string;
}

export interface JudgmentAnalyzer {
  analyze(request: RuntimeRequest, context: RuntimeContext): Promise<JudgmentSignals>;
}

export async function judgeRuntimeRequest(
  request: RuntimeRequest,
  context: RuntimeContext,
  analyzer: JudgmentAnalyzer,
): Promise<JudgmentResult> {
  const signals = await analyzer.analyze(request, context);
  const facts = signals.facts ?? [];
  const feelings = signals.feelings ?? [];
  const interpretations = signals.interpretations ?? [];
  const unknowns = signals.unknowns ?? [];
  const risk = signals.risk ?? 0;

  const depth = chooseDepth({
    emotionalIntensity: signals.emotionalIntensity,
    consequenceLevel: signals.consequenceLevel,
    ambiguity: signals.ambiguity,
    safetyRelevant: signals.safetyRelevant || risk >= 2,
  });

  const needsClarification =
    Boolean(signals.clarificationQuestion) ||
    (unknowns.length > 0 && (depth === "D2" || depth === "D3"));

  return {
    depth,
    risk,
    facts,
    feelings,
    interpretations,
    unknowns,
    needsClarification,
    clarificationQuestion:
      signals.clarificationQuestion ??
      (needsClarification
        ? "I may be missing an important part. What happened next, or what are you most worried about?"
        : undefined),
  };
}
