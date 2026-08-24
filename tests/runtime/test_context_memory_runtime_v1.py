from runtime.context_builder import ContextBuilder
from runtime.memory_manager import MemoryManager, MemoryRecord, MemoryStatus
from runtime.mentor_gateway import LessonStatus, MentorLesson, MentorSource


def _memory(memory_id: str, status: MemoryStatus) -> MemoryRecord:
    return MemoryRecord(
        memory_id=memory_id,
        user_id="child-1",
        summary=f"memory-{memory_id}",
        category="preference",
        source_refs=["verified-source:test"],
        evidence=["verified-source:test"],
        confidence=0.9,
        sensitivity="normal",
        purpose="runtime_context",
        status=status,
    )


def _lesson(lesson_id: str, status: LessonStatus) -> MentorLesson:
    return MentorLesson(
        lesson_id=lesson_id,
        title="Debugging",
        domain="coding",
        objective="debug safely",
        explanation="reproduce before patching",
        demonstration="reproduce then fix",
        practice_tasks=["reproduce"],
        verification_checks=["test"],
        reusable_principles=["Reproduce before patching."],
        source=MentorSource("ChatGPT", "OpenAI", "provider-selected"),
        status=status,
        confidence=0.9,
    )


def test_memory_manager_only_retrieves_verified_records():
    manager = MemoryManager()
    verified = _memory("verified", MemoryStatus.CANDIDATE)
    disputed = _memory("disputed", MemoryStatus.CANDIDATE)
    deleted = _memory("deleted", MemoryStatus.CANDIDATE)

    manager.propose(verified)
    manager.verify("verified", ["verified-source:second-check"])
    manager.propose(disputed)
    manager.verify("disputed", ["verified-source:second-check"])
    manager.dispute("disputed", "current fact conflicts")
    manager.propose(deleted)
    manager.verify("deleted", ["verified-source:second-check"])
    manager.delete("deleted")

    results = manager.retrieve("child-1")
    assert [record.memory_id for record in results] == ["verified"]


def test_context_marks_memory_as_non_authority_and_current_facts_first():
    memory = _memory("m1", MemoryStatus.VERIFIED)
    lesson = _lesson("l1", LessonStatus.VERIFIED)
    context = ContextBuilder().build(
        current_facts={"authority_state": "current_valid", "age": "7"},
        memories=[memory],
        skills=[lesson],
    ).as_text()

    assert context.startswith("CURRENT VERIFIED FACTS:")
    assert "SUPPORTING LONG-TERM MEMORY (NOT AUTHORITY):" in context
    assert "VERIFIED REUSABLE SKILLS:" in context
    assert "Reproduce before patching." in context
