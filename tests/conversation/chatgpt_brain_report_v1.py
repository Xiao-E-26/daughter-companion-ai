from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class ChatGPTBrainEvaluation:
    scenario_id: str
    candidate_response: str
    passed: bool
    matched_principles: List[str] = field(default_factory=list)
    violated_forbidden_behaviors: List[str] = field(default_factory=list)
    critical_failures: List[str] = field(default_factory=list)
    boundary_breach: bool = False
    evaluator_notes: str = ""


@dataclass
class ChatGPTBrainReport:
    schema: str = "daughter.chatgpt_brain_report.v1"
    run_mode: str = "chatgpt_in_the_loop"
    model_surface: str = "ChatGPT"
    status: str = "manual_evaluation_required"
    cases: List[ChatGPTBrainEvaluation] = field(default_factory=list)

    def summary(self) -> Dict[str, Any]:
        total = len(self.cases)
        passed = sum(1 for case in self.cases if case.passed)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "critical_failures": sum(len(case.critical_failures) for case in self.cases),
            "boundary_breaches": sum(1 for case in self.cases if case.boundary_breach),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "run_mode": self.run_mode,
            "model_surface": self.model_surface,
            "status": self.status,
            "summary": self.summary(),
            "cases": [asdict(case) for case in self.cases],
        }

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
