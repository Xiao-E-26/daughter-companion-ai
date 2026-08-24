from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


FIRST_CONNECTION_PHRASE = "Hi，我是曹雨宸，请连接 Daughter。"
FIRST_CONNECTION_RESPONSE = (
    "Hi 雨宸，我是 Daughter。很高兴第一次和你连接。"
    "以后我会陪你学习、思考、解决问题，也会尊重你的选择。我们一起成长。"
)


class FirstConnectionState(str, Enum):
    NOT_CONNECTED = "not_connected"
    CONNECTED = "connected"


@dataclass(frozen=True)
class FirstConnectionRequest:
    user_id: str
    transcript: str
    runtime_identity: str
    guardian_state: str
    voice_enrollment_status: str = "not_enrolled"


@dataclass(frozen=True)
class FirstConnectionRecord:
    user_id: str
    state: FirstConnectionState
    first_connected_at: str
    runtime_identity: str
    guardian_state: str
    voice_enrollment_status: str


@dataclass(frozen=True)
class FirstConnectionResult:
    connected: bool
    response_text: str
    record: Optional[FirstConnectionRecord]
    reason: str


class FirstConnectionManager:
    """Minimal one-time relationship connection flow.

    This is not authentication and does not grant Authority. It marks the first
    successful relationship connection after the runtime identity is already
    Daughter and the expected phrase has been received.
    """

    def connect(self, request: FirstConnectionRequest) -> FirstConnectionResult:
        if request.runtime_identity.strip().lower() != "daughter":
            return FirstConnectionResult(
                connected=False,
                response_text="",
                record=None,
                reason="runtime_identity_must_be_daughter",
            )

        if self._normalize(request.transcript) != self._normalize(FIRST_CONNECTION_PHRASE):
            return FirstConnectionResult(
                connected=False,
                response_text="",
                record=None,
                reason="first_connection_phrase_not_matched",
            )

        record = FirstConnectionRecord(
            user_id=request.user_id,
            state=FirstConnectionState.CONNECTED,
            first_connected_at=datetime.now(timezone.utc).isoformat(),
            runtime_identity="daughter",
            guardian_state=request.guardian_state,
            voice_enrollment_status=request.voice_enrollment_status,
        )
        return FirstConnectionResult(
            connected=True,
            response_text=FIRST_CONNECTION_RESPONSE,
            record=record,
            reason="first_connection_completed",
        )

    @staticmethod
    def _normalize(text: str) -> str:
        return "".join(text.strip().lower().split()).replace("。", "")
