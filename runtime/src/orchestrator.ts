import type {
  JudgmentResult,
  ModelInput,
  RuntimeContext,
  RuntimeRequest,
  RuntimeResponse,
} from "./contracts";
import type { ModelAdapter } from "./model_adapter";
import { safetyGate } from "./safety_gate";

export interface RuntimeDependencies {
  loadContext(request: RuntimeRequest): Promise<RuntimeContext>;
  judge(request: RuntimeRequest, context: RuntimeContext): Promise<JudgmentResult>;
  buildSystemContext(
    request: RuntimeRequest,
    context: RuntimeContext,
    judgment: JudgmentResult,
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

  const systemContext = await deps.buildSystemContext(request, context, judgment);
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
