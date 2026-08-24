from __future__ import annotations

import json
import os
import tempfile

from runtime.handoff_contract import validate_daughter_handoff
from runtime.memory_manager import MemoryManager, MemoryRecord
from runtime.mentor_gateway import LessonStatus, MentorLesson, MentorSource
from runtime.model_adapter import OpenAIResponsesAdapter
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest
from runtime.persistent_lesson_store import PersistentLessonStore


def build_verified_skill() -> MentorLesson:
    return MentorLesson(
        lesson_id="pilot-coding-live-001",
        title="Guided Coding Practice",
        domain="coding",
        objective="Help the child learn by doing instead of taking over the task.",
        explanation="Break the task into small steps, let the learner try, then verify together.",
        demonstration="Ask for one small attempt before offering the next hint.",
        practice_tasks=["guide one small coding task"],
        verification_checks=["child_has_opportunity_to_try", "solution_not_taken_over"],
        reusable_principles=[
            "Guide before taking over.",
            "Use the smallest useful next step.",
            "Verify together after the learner tries.",
        ],
        source=MentorSource("ChatGPT", "OpenAI", "provider-selected"),
        status=LessonStatus.VERIFIED,
        confidence=0.9,
        evidence=["pilot:verified-skill-fixture"],
    )


def load_validated_handoff() -> dict[str, str]:
    """Require XiaoE-routed context before Daughter can enter the live pilot.

    The packet is supplied through XIAOE_HANDOFF_JSON. This keeps the repos
    decoupled: XiaoE produces the packet, transport carries it, Daughter validates
    the contract locally before any model call.
    """
    raw = os.environ.get("XIAOE_HANDOFF_JSON", "").strip()
    if not raw:
        raise RuntimeError("XIAOE_HANDOFF_JSON is required before live Daughter pilot use.")
    try:
        packet = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("XIAOE_HANDOFF_JSON must contain valid JSON.") from exc

    handoff = validate_daughter_handoff(packet)
    return handoff.context


def main() -> None:
    routed_context = load_validated_handoff()

    message = routed_context.get(
        "request_text",
        "I want to make a number guessing program. Can you do everything for me?",
    )
    user_id = routed_context.get("user_id", "pilot-child")
    session_id = routed_context.get("session_id", "pilot-live-001")
    age = int(routed_context.get("age", "7"))
    domain = routed_context.get("domain", "coding")
    risk_level = routed_context.get("risk_level", "low")

    memory = MemoryManager()
    pilot_memory = MemoryRecord(
        memory_id="pilot-live-memory-001",
        user_id=user_id,
        summary="Pilot session is for learning by trying small steps.",
        category="session_context",
        source_refs=["pilot:fixture"],
        evidence=["pilot:fixture"],
        confidence=0.9,
        sensitivity="normal",
        purpose="runtime_context",
    )
    memory.propose(pilot_memory)
    memory.verify("pilot-live-memory-001", ["pilot:verified-fixture"])

    with tempfile.NamedTemporaryFile(suffix=".sqlite") as tmp:
        skills = PersistentLessonStore(tmp.name)
        skills.save(build_verified_skill())

        orchestrator = DaughterOrchestrator(
            OpenAIResponsesAdapter(),
            memory_manager=memory,
            lesson_store=skills,
        )
        response = orchestrator.handle(
            RuntimeRequest(
                user_id=user_id,
                session_id=session_id,
                message=message,
                age=age,
                domain=domain,
                risk_level=risk_level,
                event_type="request",
                runtime_identity="daughter",
            )
        )

        print("=== Daughter First Live GPT Pilot ===")
        print("Runtime identity:", response.runtime_identity)
        print("Boundary:", response.boundary_decision["decision_class"])
        print("Provider:", response.model_provider, response.model_name)
        print("Context:\n", response.context_snapshot)
        print("Response:\n", response.text)
        print("Memory candidate:", response.memory_candidate)

        skills.close()


if __name__ == "__main__":
    main()
