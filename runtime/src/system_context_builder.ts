import type {
  JudgmentResult,
  ProblemPlan,
  RuntimeContext,
  RuntimeRequest,
} from "./contracts.ts";

function list(label: string, items: string[]): string {
  return `${label}: ${items.length ? items.join(" | ") : "none"}`;
}

export async function buildSystemContext(
  _request: RuntimeRequest,
  context: RuntimeContext,
  judgment: JudgmentResult,
  problemPlan?: ProblemPlan,
): Promise<string> {
  const memoryLines = context.memories.map(
    (memory) =>
      `- [${memory.type}/${memory.factStatus}/${memory.confidence}] ${memory.content}`,
  );

  const problemLines = problemPlan
    ? [
        `Problem: ${problemPlan.problem}`,
        list("Root-cause hypotheses", problemPlan.rootCauseHypotheses),
        list("Options", problemPlan.options),
        `Recommended smallest safe action: ${problemPlan.recommendedAction ?? "none"}`,
        `Reversible: ${problemPlan.reversible}`,
        `Needs human help: ${problemPlan.needsHumanHelp}`,
      ]
    : ["Problem plan: not required for this turn"];

  return [
    "You are Daughter, a long-term companion identity. The model is an engine; it is not the identity itself.",
    "Core operating order: Fact First → Understand → Judgment → Problem Solving → Action → Learn.",
    "Fact First does not mean Emotion Last. Separate facts, feelings, interpretations, and unknowns without dismissing emotion.",
    "Prefer the smallest safe useful and reversible action. Ask when uncertain. Do not invent certainty.",
    "Support real-world human relationships and user competence. Never create exclusivity, jealousy, guilt, or dependency.",
    "Growth direction: decide for → teach to decide → decide together → respect their decision.",
    "No surveillance by default. Use the least escalation necessary. Real risk matters more than keywords.",
    "Do not directly execute physical-world actions from model output.",
    "",
    `Growth stage: ${context.growth.coreStage}`,
    `Relationship stage: ${context.relationshipStage ?? "unknown"}`,
    `Depth: ${judgment.depth}`,
    `Risk: ${judgment.risk}`,
    list("Facts", judgment.facts),
    list("Feelings", judgment.feelings),
    list("Interpretations", judgment.interpretations),
    list("Unknowns", judgment.unknowns),
    "",
    "Relevant memories:",
    ...(memoryLines.length ? memoryLines : ["- none"]),
    "",
    ...problemLines,
  ].join("\n");
}
