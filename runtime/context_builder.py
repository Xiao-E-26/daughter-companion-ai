from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from runtime.memory_manager import MemoryRecord
from runtime.mentor_gateway import MentorLesson


@dataclass(frozen=True)
class BuiltContext:
    memory_lines: List[str]
    skill_lines: List[str]
    current_fact_lines: List[str]

    def as_text(self) -> str:
        sections: List[str] = []
        if self.current_fact_lines:
            sections.append("CURRENT VERIFIED FACTS:\n" + "\n".join(self.current_fact_lines))
        if self.memory_lines:
            sections.append("SUPPORTING LONG-TERM MEMORY (NOT AUTHORITY):\n" + "\n".join(self.memory_lines))
        if self.skill_lines:
            sections.append("VERIFIED REUSABLE SKILLS:\n" + "\n".join(self.skill_lines))
        return "\n\n".join(sections)


class ContextBuilder:
    """Builds model context without allowing memory/skills to become Authority.

    Precedence:
      current verified facts > verified memory > verified skills as supporting context.

    Memory and lessons may guide reasoning, but cannot grant permissions, override
    current verified facts, or rewrite Daughter's protected core.
    """

    def __init__(self, *, max_memories: int = 8, max_skills: int = 8) -> None:
        self.max_memories = max_memories
        self.max_skills = max_skills

    def build(
        self,
        *,
        current_facts: Dict[str, str],
        memories: Iterable[MemoryRecord],
        skills: Iterable[MentorLesson],
    ) -> BuiltContext:
        current_fact_lines = [f"- {key}: {value}" for key, value in current_facts.items()]

        memory_lines: List[str] = []
        for memory in list(memories)[: self.max_memories]:
            memory_lines.append(
                f"- [{memory.memory_id}] {memory.summary} "
                f"(confidence={memory.confidence:.2f}, source={','.join(memory.source_refs) or 'unknown'})"
            )

        skill_lines: List[str] = []
        for lesson in list(skills)[: self.max_skills]:
            principles = "; ".join(lesson.reusable_principles)
            skill_lines.append(
                f"- [{lesson.lesson_id}] {lesson.title}: {principles} "
                f"(confidence={lesson.confidence:.2f})"
            )

        return BuiltContext(
            memory_lines=memory_lines,
            skill_lines=skill_lines,
            current_fact_lines=current_fact_lines,
        )
