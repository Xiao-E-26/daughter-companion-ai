from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import List, Optional

from runtime.mentor_gateway import LessonStatus, MentorLesson, MentorSource


class PersistentLessonStore:
    """SQLite-backed, versioned lesson store for Daughter.

    Persistence does not imply immutability. Each update creates a new revision,
    preserving history while allowing verified lessons to be corrected,
    superseded, archived or rejected later.
    """

    ACTIVE_REUSABLE_STATUSES = {LessonStatus.VERIFIED.value}

    def __init__(self, db_path: str) -> None:
        self.db_path = str(Path(db_path))
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS lesson_revisions (
                lesson_id TEXT NOT NULL,
                revision INTEGER NOT NULL,
                title TEXT NOT NULL,
                domain TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                status TEXT NOT NULL,
                confidence REAL NOT NULL,
                supersedes_lesson_id TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (lesson_id, revision)
            )
            """
        )
        self._conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_lesson_status ON lesson_revisions(status)"
        )
        self._conn.commit()

    def _next_revision(self, lesson_id: str) -> int:
        row = self._conn.execute(
            "SELECT COALESCE(MAX(revision), 0) AS max_revision FROM lesson_revisions WHERE lesson_id = ?",
            (lesson_id,),
        ).fetchone()
        return int(row["max_revision"]) + 1

    def save(self, lesson: MentorLesson) -> int:
        revision = self._next_revision(lesson.lesson_id)
        payload = asdict(lesson)
        payload["status"] = lesson.status.value
        self._conn.execute(
            """
            INSERT INTO lesson_revisions
            (lesson_id, revision, title, domain, payload_json, status, confidence, supersedes_lesson_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lesson.lesson_id,
                revision,
                lesson.title,
                lesson.domain,
                json.dumps(payload, ensure_ascii=False, sort_keys=True),
                lesson.status.value,
                float(lesson.confidence),
                lesson.supersedes_lesson_id,
            ),
        )
        self._conn.commit()
        return revision

    def get_latest(self, lesson_id: str) -> Optional[MentorLesson]:
        row = self._conn.execute(
            """
            SELECT payload_json FROM lesson_revisions
            WHERE lesson_id = ? ORDER BY revision DESC LIMIT 1
            """,
            (lesson_id,),
        ).fetchone()
        return self._decode(row["payload_json"]) if row else None

    def history(self, lesson_id: str) -> List[MentorLesson]:
        rows = self._conn.execute(
            """
            SELECT payload_json FROM lesson_revisions
            WHERE lesson_id = ? ORDER BY revision ASC
            """,
            (lesson_id,),
        ).fetchall()
        return [self._decode(row["payload_json"]) for row in rows]

    def list_reusable(self, domain: Optional[str] = None) -> List[MentorLesson]:
        query = """
            SELECT lr.payload_json
            FROM lesson_revisions lr
            JOIN (
                SELECT lesson_id, MAX(revision) AS max_revision
                FROM lesson_revisions GROUP BY lesson_id
            ) latest
            ON lr.lesson_id = latest.lesson_id AND lr.revision = latest.max_revision
            WHERE lr.status = ?
        """
        params: List[object] = [LessonStatus.VERIFIED.value]
        if domain is not None:
            query += " AND lr.domain = ?"
            params.append(domain)
        rows = self._conn.execute(query, tuple(params)).fetchall()
        return [self._decode(row["payload_json"]) for row in rows]

    def supersede(self, old_lesson_id: str, replacement: MentorLesson) -> None:
        old = self.get_latest(old_lesson_id)
        if old is None:
            raise KeyError(old_lesson_id)
        old.status = LessonStatus.SUPERSEDED
        self.save(old)
        replacement.supersedes_lesson_id = old_lesson_id
        self.save(replacement)

    def reject(self, lesson_id: str, reason: str) -> MentorLesson:
        lesson = self.get_latest(lesson_id)
        if lesson is None:
            raise KeyError(lesson_id)
        lesson.status = LessonStatus.REJECTED
        lesson.failure_notes.append(reason)
        self.save(lesson)
        return lesson

    def close(self) -> None:
        self._conn.close()

    @staticmethod
    def _decode(payload_json: str) -> MentorLesson:
        payload = json.loads(payload_json)
        source = MentorSource(**payload["source"])
        return MentorLesson(
            lesson_id=payload["lesson_id"],
            title=payload["title"],
            domain=payload["domain"],
            objective=payload["objective"],
            explanation=payload["explanation"],
            demonstration=payload["demonstration"],
            practice_tasks=list(payload["practice_tasks"]),
            verification_checks=list(payload["verification_checks"]),
            reusable_principles=list(payload["reusable_principles"]),
            source=source,
            status=LessonStatus(payload["status"]),
            confidence=float(payload.get("confidence", 0.0)),
            evidence=list(payload.get("evidence", [])),
            failure_notes=list(payload.get("failure_notes", [])),
            supersedes_lesson_id=payload.get("supersedes_lesson_id"),
        )
