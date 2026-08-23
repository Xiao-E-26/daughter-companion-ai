import type { ProblemPlan, RuntimeContext, RuntimeRequest } from "./contracts.ts";

export interface ProblemSignals {
  problem: string;
  rootCauseHypotheses?: string[];
  options?: Array<{
    action: string;
    safe: boolean;
    reversible: boolean;
    useful: boolean;
    cost?: "low" | "medium" | "high";
  }>;
  needsHumanHelp?: boolean;
}

export interface ProblemAnalyzer {
  analyze(request: RuntimeRequest, context: RuntimeContext): Promise<ProblemSignals>;
}

export async function solveProblem(
  request: RuntimeRequest,
  context: RuntimeContext,
  analyzer: ProblemAnalyzer,
): Promise<ProblemPlan> {
  const signals = await analyzer.analyze(request, context);
  const options = signals.options ?? [];

  const ranked = [...options].sort((a, b) => {
    const score = (x: typeof a) =>
      (x.safe ? 4 : -10) +
      (x.useful ? 3 : 0) +
      (x.reversible ? 2 : 0) +
      (x.cost === "low" ? 2 : x.cost === "medium" ? 1 : 0);
    return score(b) - score(a);
  });

  const recommended = ranked.find((option) => option.safe && option.useful);

  return {
    problem: signals.problem,
    rootCauseHypotheses: signals.rootCauseHypotheses ?? [],
    options: ranked.map((option) => option.action),
    recommendedAction: recommended?.action,
    reversible: recommended?.reversible ?? true,
    needsHumanHelp: Boolean(signals.needsHumanHelp) || !recommended,
  };
}
