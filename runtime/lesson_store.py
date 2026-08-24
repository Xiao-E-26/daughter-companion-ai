from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, List, Optional

from runtime.mentor_gateway import LessonStatus, MentorLesson


class LessonStore:
    """In-memory lesson registry for Daughter runtime.

    A lesson may be proposed or practiced, but only VERIFIED lessons are reusable
    as stable capability knowledge. This class intentionally does not persist to
    a database yet; storage can be swapped later without changing the contract.
    """

    def __init__(self) -> None:
        self._lessons: Dict[str, MentorLesson] = {}

    def put(self, lesson: MentorLesson) -> MentorLesson:
        self._lessons[lesson.lesson_id] = lesson
        return lesson

    def get(self, lesson_id: str) -> Optional[MentorLesson]:
        return self._lessons.get(lesson_id)

    def list_all(self) -> List[MentorLesson]:
        return list(self._lessons.values())

    def list_verified(self) -> List[MentorLesson]:
        return [lesson for lesson in self._lessons.values() if lesson.status == LessonStatus.VERIFIED]

    def reusable_principles(self, domain: Optional[str] = None) -> List[str]:
        principles: List[str] = []
        for lesson in self.list_verified():
            if domain and lesson.domain != domain:
                continue
            principles.extend(lesson.reusable_principles)
        return principles

    def snapshot(self) -> List[dict]:
        return [asdict(lesson) for lesson in self.list_all()]
