import type { MemoryContextItem, RuntimeRequest } from "./contracts.ts";

export type MemoryStatus = "active" | "historical" | "disputed" | "archived" | "deleted";

export interface MemoryWriteCandidate {
  type: MemoryContextItem["type"];
  content: string;
  factStatus: MemoryContextItem["factStatus"];
  confidence: MemoryContextItem["confidence"];
  sensitivity?: "normal" | "sensitive" | "high";
  importance?: "low" | "normal" | "high";
  expiresAt?: string;
}

export interface MemoryDecision {
  action: "ignore" | "store" | "confirm" | "replace" | "archive";
  reason: string;
  candidate?: MemoryWriteCandidate;
}

const prohibitedPermanentLabels = [
  "lazy",
  "bad child",
  "difficult person",
  "always lies",
  "never listens",
];

function containsPermanentNegativeLabel(content: string): boolean {
  const lower = content.toLowerCase();
  return prohibitedPermanentLabels.some((label) => lower.includes(label));
}

export function decideMemoryWrite(
  _request: RuntimeRequest,
  candidate: MemoryWriteCandidate | undefined,
  existing: MemoryContextItem[],
): MemoryDecision {
  if (!candidate || !candidate.content.trim()) {
    return { action: "ignore", reason: "no_meaningful_candidate" };
  }

  if (containsPermanentNegativeLabel(candidate.content)) {
    return { action: "ignore", reason: "reject_permanent_negative_label" };
  }

  if (candidate.factStatus === "unknown" || candidate.confidence === "unverified") {
    return { action: "confirm", reason: "uncertain_memory_requires_confirmation", candidate };
  }

  if (candidate.sensitivity === "high") {
    return { action: "confirm", reason: "high_sensitivity_requires_explicit_confirmation", candidate };
  }

  const sameType = existing.filter((item) => item.type === candidate.type);
  const contradiction = sameType.find(
    (item) => item.factStatus === "fact" && item.content.trim() !== candidate.content.trim(),
  );

  if (contradiction) {
    return { action: "replace", reason: "newer_confirmed_reality_supersedes_old_memory", candidate };
  }

  return { action: "store", reason: "selective_memory_candidate_accepted", candidate };
}

export function shouldForgetMemory(input: {
  status: MemoryStatus;
  expiresAt?: string | null;
  now?: Date;
  userRequestedDeletion?: boolean;
}): boolean {
  if (input.userRequestedDeletion) return true;
  if (input.status === "deleted" || input.status === "archived") return true;
  if (!input.expiresAt) return false;
  const now = input.now ?? new Date();
  return new Date(input.expiresAt).getTime() <= now.getTime();
}
