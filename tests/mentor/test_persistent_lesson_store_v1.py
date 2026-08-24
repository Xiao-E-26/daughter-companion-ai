from tempfile import TemporaryDirectory
from pathlib import Path

from runtime.mentor_gateway import LessonStatus, MentorLesson, MentorSource
from runtime.persistent_lesson_store import PersistentLessonStore


def make_lesson(lesson_id: str, status: LessonStatus, principle: str) -> MentorLesson:
    return MentorLesson(
        lesson_id=lesson_id,
        title="Debug lesson",
        domain="coding",
        objective="debug reliably",
        explanation="reproduce, isolate, verify",
        demonstration="example",
        practice_tasks=["practice"],
        verification_checks=["check"],
        reusable_principles=[principle],
        source=MentorSource("ChatGPT", "OpenAI", "provider-selected"),
        status=status,
        confidence=0.8 if status == LessonStatus.VERIFIED else 0.2,
    )


def test_persists_across_reopen_and_only_verified_reuses():
    with TemporaryDirectory() as td:
        db = str(Path(td) / "lessons.sqlite")
        store = PersistentLessonStore(db)
        store.save(make_lesson("l1", LessonStatus.VERIFIED, "verify both failure and normal case"))
        store.save(make_lesson("l2", LessonStatus.PRACTICING, "not reusable yet"))
        store.close()

        reopened = PersistentLessonStore(db)
        assert reopened.get_latest("l1") is not None
        reusable = reopened.list_reusable("coding")
        assert [x.lesson_id for x in reusable] == ["l1"]
        reopened.close()


def test_supersede_preserves_history_and_removes_old_from_reuse():
    with TemporaryDirectory() as td:
        db = str(Path(td) / "lessons.sqlite")
        store = PersistentLessonStore(db)
        old = make_lesson("old", LessonStatus.VERIFIED, "old principle")
        new = make_lesson("new", LessonStatus.VERIFIED, "improved principle")
        store.save(old)
        store.supersede("old", new)

        assert store.get_latest("old").status == LessonStatus.SUPERSEDED
        assert len(store.history("old")) == 2
        reusable_ids = {x.lesson_id for x in store.list_reusable("coding")}
        assert "old" not in reusable_ids
        assert "new" in reusable_ids
        store.close()


def test_reject_creates_new_revision_and_stops_reuse():
    with TemporaryDirectory() as td:
        db = str(Path(td) / "lessons.sqlite")
        store = PersistentLessonStore(db)
        store.save(make_lesson("l1", LessonStatus.VERIFIED, "principle"))
        store.reject("l1", "new evidence showed the lesson was wrong")

        assert store.get_latest("l1").status == LessonStatus.REJECTED
        assert len(store.history("l1")) == 2
        assert store.list_reusable("coding") == []
        store.close()
