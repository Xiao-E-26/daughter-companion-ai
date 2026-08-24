from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from runtime.lesson_store import LessonStore
from runtime.mentor_gateway import LessonStatus, MentorLesson, XiaoEMentorGateway


@dataclass
class PracticeAttempt:
    lesson_id: str
    passed_checks: List[str]
    evidence: List[str]
    notes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class PracticeResult:
    lesson_id: str
    status: LessonStatus
    confidence: float
    missing_checks: List[str]
    reusable: bool


class PracticeRunner:
    def __init__(self, gateway: XiaoEMentorGateway, store: LessonStore) -> None:
        self.gateway = gateway
        self.store = store

    def begin(self, lesson: MentorLesson) -> MentorLesson:
        lesson = self.gateway.mark_practicing(lesson)
        return self.store.put(lesson)

    def submit(self, attempt: PracticeAttempt) -> PracticeResult:
        lesson = self.store.get(attempt.lesson_id)
        if lesson is None:
            raise KeyError(f"Unknown lesson: {attempt.lesson_id}")

        lesson = self.gateway.verify(
            lesson,
            passed_checks=attempt.passed_checks,
            evidence=attempt.evidence,
        )
        lesson.failure_notes.extend(attempt.notes)
        self.store.put(lesson)

        missing = sorted(set(lesson.verification_checks) - set(attempt.passed_checks))
        return PracticeResult(
            lesson_id=lesson.lesson_id,
            status=lesson.status,
            confidence=lesson.confidence,
            missing_checks=missing,
            reusable=lesson.status == LessonStatus.VERIFIED,
        )
