import type { GrowthContext } from "./contracts";

export interface GrowthSignals {
  understandsConsequences?: boolean;
  separatesFactFromInterpretation?: boolean;
  respectsBoundaries?: boolean;
  managesRisk?: boolean;
  regulatesEmotion?: boolean;
  seeksHelpAppropriately?: boolean;
  ownsDecisions?: boolean;
}

export interface DomainAutonomy {
  learning: "supported" | "shared" | "independent";
  social: "supported" | "shared" | "independent";
  privacy: "supported" | "shared" | "independent";
  risk: "supported" | "shared" | "independent";
}

function domainLevel(score: number): DomainAutonomy[keyof DomainAutonomy] {
  if (score >= 3) return "independent";
  if (score >= 2) return "shared";
  return "supported";
}

export function deriveDomainAutonomy(signals: GrowthSignals): DomainAutonomy {
  const judgment = Number(Boolean(signals.understandsConsequences)) +
    Number(Boolean(signals.separatesFactFromInterpretation));
  const boundary = Number(Boolean(signals.respectsBoundaries));
  const risk = Number(Boolean(signals.managesRisk)) + Number(Boolean(signals.seeksHelpAppropriately));
  const ownership = Number(Boolean(signals.ownsDecisions));
  const emotion = Number(Boolean(signals.regulatesEmotion));

  return {
    learning: domainLevel(judgment + ownership),
    social: domainLevel(boundary + emotion + ownership),
    privacy: domainLevel(boundary + ownership),
    risk: domainLevel(risk + judgment),
  };
}

export function suggestCoreStage(
  current: GrowthContext["coreStage"],
  autonomy: DomainAutonomy,
): GrowthContext["coreStage"] {
  const values = Object.values(autonomy);
  const independent = values.filter((v) => v === "independent").length;
  const supported = values.filter((v) => v === "supported").length;

  // Growth is directional but not gamified. A stage change is only a suggestion;
  // persistence requires a separate reviewed decision.
  if (supported >= 3) return "protective_companionship";
  if (independent >= 3) return "mature_companionship";
  if (independent >= 1) return "autonomy_building";
  if (current === "mature_companionship" && supported <= 1) return current;
  return "guided_learning";
}
