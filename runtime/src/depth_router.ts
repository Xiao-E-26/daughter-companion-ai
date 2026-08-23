import type { DepthLevel } from "./contracts.ts";

export interface DepthSignals {
  emotionalIntensity?: "low" | "medium" | "high";
  consequenceLevel?: "low" | "medium" | "high";
  ambiguity?: "low" | "medium" | "high";
  safetyRelevant?: boolean;
}

export function chooseDepth(signals: DepthSignals): DepthLevel {
  if (signals.safetyRelevant || signals.consequenceLevel === "high") return "D3";
  if (signals.emotionalIntensity === "high" || signals.ambiguity === "high") return "D2";
  if (
    signals.consequenceLevel === "medium" ||
    signals.emotionalIntensity === "medium" ||
    signals.ambiguity === "medium"
  ) return "D1";
  return "D0";
}
