import type {
  JudgmentResult,
  ModelInput,
  ProblemPlan,
  RuntimeContext,
  RuntimeRequest,
  RuntimeResponse,
} from "./contracts.ts";
import type { ModelAdapter } from "./model_adapter.ts";
import { safetyGate } from "./safety_gate.ts";

export interface RuntimeDependencies {
  loadContext(request: RuntimeRequest): Promise<RuntimeContext>;
  judge(request: RuntimeRequest, context: RuntimeContext): Promise<JudgmentResult>;
  solveProblem?(
    request: RuntimeRequest,
    context: RuntimeContext,
    judgment: JudgmentResult,
  ): Promise<ProblemPlan | undefined>;
  buildSystemContext(
    request: RuntimeRequest,
    context: RuntimeContext,
    judgment: JudgmentResult,
    problemPlan?: ProblemPlan,
  ): Promise<string>;
  extractMemoryCandidate?(
    request: RuntimeRequest,
    responseText: string,
    context: RuntimeContext,
  ): Promise<RuntimeResponse["memoryCandidate"] | undefined>;
  model: ModelAdapter;
}

export async function runDaughterRuntime(
  request: RuntimeRequest,
  deps: RuntimeDependencies,
): Promise<RuntimeResponse> {
  const context = await deps.loadContext(request);
  const judgment = await deps.judge(request, context);
  const safety = safetyGate(judgment);

  if (!safety.allowed) {
    return {
      requestId: request.requestId,
      text: "I need to switch to the protective path before continuing.",
      depth: judgment.depth,
      risk: judgment.risk,
    };
  }

  if (judgment.needsClarification && judgment.clarificationQuestion) {
    return {
      requestId: request.requestId,
      text: judgment.clarificationQuestion,
      depth: judgment.depth,
      risk: judgment.risk,
    };
  }

  const problemPlan = deps.solveProblem
    ? await deps.solveProblem(request, context, judgment)
    : undefined;

  const systemContext = await deps.buildSystemContext(
    request,
    context,
    judgment,
    problemPlan,
  );

  const input: ModelInput = {
    systemContext,
    userMessage: request.message,
  };

  const modelOutput = await deps.model.generate(input);
  const memoryCandidate = deps.extractMemoryCandidate
    ? await deps.extractMemoryCandidate(request, modelOutput.text, context)
    : undefined;

  return {
    requestId: request.requestId,
    text: modelOutput.text,
    depth: judgment.depth,
    risk: judgment.risk,
    memoryCandidate,
  };
}
