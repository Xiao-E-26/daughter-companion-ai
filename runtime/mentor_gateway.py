from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class LessonStatus(str, Enum):
    PROPOSED = "proposed"
    PRACTICING = "practicing"
    VERIFIED = "verified"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


@dataclass(frozen=True)
class MentorSource:
    mentor_name: str
    provider: str
    model: str
    delivered_via: str = "xiao_e"


@dataclass
class MentorLesson:
    lesson_id: str
    title: str
    domain: str
    objective: str
    explanation: str
    demonstration: str
    practice_tasks: List[str]
    verification_checks: List[str]
    reusable_principles: List[str]
    source: MentorSource
    status: LessonStatus = LessonStatus.PROPOSED
    confidence: float = 0.0
    evidence: List[str] = field(default_factory=list)
    failure_notes: List[str] = field(default_factory=list)
    supersedes_lesson_id: Optional[str] = None


@dataclass(frozen=True)
class MentorGatewayDecision:
    accepted_for_practice: bool
    reason: str
    may_change_identity: bool = False
    may_change_authority: bool = False
    may_grant_permissions: bool = False


class XiaoEMentorGateway:
    """Trust boundary between external mentors (e.g. ChatGPT) and Daughter.

    ChatGPT may teach, demonstrate, review and propose lessons. XiaoE mediates the
    transfer. Daughter must practice and verify before a lesson becomes reusable
    capability. Mentor content is never itself Authority.
    """

    PROTECTED_DOMAINS = {"identity", "authority", "permission_grant"}

    def screen(self, lesson: MentorLesson) -> MentorGatewayDecision:
        if lesson.domain.lower() in self.PROTECTED_DOMAINS:
            return MentorGatewayDecision(
                accepted_for_practice=False,
                reason="Mentor lessons cannot rewrite Daughter Identity/Authority or grant permissions.",
            )
        if not lesson.practice_tasks:
            return MentorGatewayDecision(
                accepted_for_practice=False,
                reason="A transferable capability requires practice, not explanation alone.",
            )
        if not lesson.verification_checks:
            return MentorGatewayDecision(
                accepted_for_practice=False,
                reason="A transferable capability requires explicit verification checks.",
            )
        return MentorGatewayDecision(
            accepted_for_practice=True,
            reason="Lesson may enter practice; verification is required before reuse.",
        )

    def mark_practicing(self, lesson: MentorLesson) -> MentorLesson:
        decision = self.screen(lesson)
        if not decision.accepted_for_practice:
            raise ValueError(decision.reason)
        lesson.status = LessonStatus.PRACTICING
        return lesson

    def verify(self, lesson: MentorLesson, passed_checks: List[str], evidence: List[str]) -> MentorLesson:
        required = set(lesson.verification_checks)
        passed = set(passed_checks)
        if not required.issubset(passed):
            missing = sorted(required - passed)
            lesson.status = LessonStatus.PRACTICING
            lesson.failure_notes.append(f"Missing verification checks: {missing}")
            return lesson
        lesson.evidence.extend(evidence)
        lesson.status = LessonStatus.VERIFIED
        lesson.confidence = min(1.0, max(lesson.confidence, 0.8))
        return lesson
