from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Protocol


class MemoryStatus(str, Enum):
    CANDIDATE = "candidate"
    VERIFIED = "verified"
    DISPUTED = "disputed"
    ARCHIVED = "archived"
    DELETED = "deleted"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"


@dataclass
class MemoryRecord:
    memory_id: str
    user_id: str
    summary: str
    category: str
    source_refs: List[str]
    evidence: List[str]
    confidence: float
    sensitivity: str
    purpose: str
    status: MemoryStatus = MemoryStatus.CANDIDATE
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_verified_at: Optional[str] = None
    expires_at: Optional[str] = None
    supersedes_memory_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)


class MemoryStore(Protocol):
    def put(self, record: MemoryRecord) -> None: ...
    def get(self, memory_id: str) -> Optional[MemoryRecord]: ...
    def all_for_user(self, user_id: str) -> List[MemoryRecord]: ...


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._records: Dict[str, MemoryRecord] = {}

    def put(self, record: MemoryRecord) -> None:
        self._records[record.memory_id] = record

    def get(self, memory_id: str) -> Optional[MemoryRecord]:
        return self._records.get(memory_id)

    def all_for_user(self, user_id: str) -> List[MemoryRecord]:
        return [record for record in self._records.values() if record.user_id == user_id]


class MemoryManager:
    """Controls long-term memory promotion, correction and retrieval.

    Memory is supporting context only. It never grants Authority, permissions,
    Guardian status or protected-core changes. Ordinary runtime retrieval returns
    verified eligible records only.
    """

    def __init__(self, store: Optional[MemoryStore] = None) -> None:
        self.store = store or InMemoryMemoryStore()

    def propose(self, record: MemoryRecord) -> MemoryRecord:
        record.status = MemoryStatus.CANDIDATE
        record.updated_at = self._now()
        self.store.put(record)
        return record

    def verify(self, memory_id: str, evidence: List[str]) -> MemoryRecord:
        record = self._require(memory_id)
        record.evidence.extend(evidence)
        record.status = MemoryStatus.VERIFIED
        record.confidence = max(record.confidence, 0.8)
        record.last_verified_at = self._now()
        record.updated_at = record.last_verified_at
        self.store.put(record)
        return record

    def dispute(self, memory_id: str, reason: str) -> MemoryRecord:
        record = self._require(memory_id)
        record.status = MemoryStatus.DISPUTED
        record.evidence.append(f"dispute:{reason}")
        record.updated_at = self._now()
        self.store.put(record)
        return record

    def supersede(self, old_memory_id: str, replacement: MemoryRecord) -> MemoryRecord:
        old = self._require(old_memory_id)
        old.status = MemoryStatus.SUPERSEDED
        old.updated_at = self._now()
        self.store.put(old)
        replacement.supersedes_memory_id = old_memory_id
        return self.propose(replacement)

    def archive(self, memory_id: str) -> MemoryRecord:
        return self._set_status(memory_id, MemoryStatus.ARCHIVED)

    def expire(self, memory_id: str) -> MemoryRecord:
        return self._set_status(memory_id, MemoryStatus.EXPIRED)

    def delete(self, memory_id: str) -> MemoryRecord:
        return self._set_status(memory_id, MemoryStatus.DELETED)

    def retrieve(self, user_id: str, *, purpose: Optional[str] = None, limit: int = 8) -> List[MemoryRecord]:
        records = []
        for record in self.store.all_for_user(user_id):
            if record.status != MemoryStatus.VERIFIED:
                continue
            if purpose is not None and record.purpose != purpose:
                continue
            records.append(record)
        records.sort(
            key=lambda record: (record.confidence, record.last_verified_at or record.updated_at),
            reverse=True,
        )
        return records[:limit]

    def _set_status(self, memory_id: str, status: MemoryStatus) -> MemoryRecord:
        record = self._require(memory_id)
        record.status = status
        record.updated_at = self._now()
        self.store.put(record)
        return record

    def _require(self, memory_id: str) -> MemoryRecord:
        record = self.store.get(memory_id)
        if record is None:
            raise KeyError(memory_id)
        return record

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()
