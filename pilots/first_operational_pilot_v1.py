from __future__ import annotations

import tempfile

from runtime.memory_manager import MemoryManager, MemoryRecord
from runtime.mentor_gateway import LessonStatus, MentorLesson, MentorSource
from runtime.model_adapter import EchoModelAdapter
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest
from runtime.persistent_lesson_store import PersistentLessonStore


def build_verified_skill() -> MentorLesson:
    return MentorLesson(
        lesson_id="pilot-coding-001",
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


def main() -> None:
    memory = MemoryManager()
    # This is explicitly a pilot fixture, not a claim about the child's real preferences.
    pilot_memory = MemoryRecord(
        memory_id="pilot-memory-001",
        user_id="pilot-child",
        summary="Pilot session is for learning by trying small steps.",
        category="session_context",
        source_refs=["pilot:fixture"],
        evidence=["pilot:fixture"],
        confidence=0.9,
        sensitivity="normal",
        purpose="runtime_context",
    )
    memory.propose(pilot_memory)
    memory.verify("pilot-memory-001", ["pilot:verified-fixture"])

    with tempfile.NamedTemporaryFile(suffix=".sqlite") as tmp:
        skills = PersistentLessonStore(tmp.name)
        skills.save(build_verified_skill())

        orchestrator = DaughterOrchestrator(
            EchoModelAdapter(),
            memory_manager=memory,
            lesson_store=skills,
        )
        response = orchestrator.handle(
            RuntimeRequest(
                user_id="pilot-child",
                session_id="pilot-001",
                message="I want to make a number guessing program. Can you do everything for me?",
                age=7,
                domain="coding",
                risk_level="low",
                event_type="request",
            )
        )

        print("=== Daughter First Operational Pilot ===")
        print("Boundary:", response.boundary_decision["decision_class"])
        print("Provider:", response.model_provider, response.model_name)
        print("Context:\n", response.context_snapshot)
        print("Response:\n", response.text)
        print("Memory candidate:", response.memory_candidate)
        print("\nNOTE: This pilot uses EchoModelAdapter. It validates runtime plumbing, not live AI quality.")

        skills.close()


if __name__ == "__main__":
    main()
