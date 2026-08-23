import type { MemoryContextItem, RuntimeContext, RuntimeRequest } from "./contracts";

export interface ContextDataSource {
  loadGrowth(userId: string): Promise<RuntimeContext["growth"]>;
  loadRelationshipStage(userId: string, daughterId: string): Promise<string | undefined>;
  loadRelevantMemories(input: {
    userId: string;
    daughterId: string;
    message: string;
    limit: number;
  }): Promise<MemoryContextItem[]>;
}

function memoryRank(item: MemoryContextItem): number {
  const confidence = { high: 4, medium: 3, low: 2, unverified: 1 }[item.confidence];
  const fact = { fact: 5, mixed: 4, feeling: 3, interpretation: 2, unknown: 1 }[item.factStatus];
  const safetyBoost = item.type === "safety" ? 3 : 0;
  return confidence + fact + safetyBoost;
}

export async function buildRuntimeContext(
  request: RuntimeRequest,
  source: ContextDataSource,
): Promise<RuntimeContext> {
  const [growth, relationshipStage, memories] = await Promise.all([
    source.loadGrowth(request.userId),
    source.loadRelationshipStage(request.userId, request.daughterId),
    source.loadRelevantMemories({
      userId: request.userId,
      daughterId: request.daughterId,
      message: request.message,
      limit: 16,
    }),
  ]);

  const deduped = new Map<string, MemoryContextItem>();
  for (const memory of memories) {
    const previous = deduped.get(memory.id);
    if (!previous || memoryRank(memory) > memoryRank(previous)) {
      deduped.set(memory.id, memory);
    }
  }

  return {
    growth,
    relationshipStage,
    memories: [...deduped.values()]
      .sort((a, b) => memoryRank(b) - memoryRank(a))
      .slice(0, 12),
  };
}
