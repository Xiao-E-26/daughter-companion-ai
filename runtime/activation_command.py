"""Command recognition for the GitHub-side XiaoAi runtime.

This module only recognizes activation commands. It does not claim that a
runtime session is active; session activation must still be verified by the
authoritative runtime.
"""

from __future__ import annotations

CANONICAL_ACTIVATION_PHRASE = "小I上线"
LEGACY_ACTIVATION_PHRASES = ("小爱上线",)


def is_xiaoi_activation_command(text: str) -> bool:
    """Return True only for an exact supported activation phrase."""
    normalized = " ".join(text.strip().split())
    return normalized == CANONICAL_ACTIVATION_PHRASE or normalized in LEGACY_ACTIVATION_PHRASES
