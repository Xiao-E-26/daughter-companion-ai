from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Optional

from runtime.shadow_runtime_comparator import ShadowComparison


@dataclass(frozen=True)
class ShadowTelemetryEnvelope:
    correlation_hash: str
    comparison: dict
    resolver_version: str
    comparator_version: str
    latency_ms: Optional[int]
    telemetry_schema_version: str = "shadow-runtime-telemetry-v1"

    def as_dict(self) -> dict:
        return asdict(self)


def build_shadow_telemetry(
    *,
    comparison: ShadowComparison,
    resolver_version: str,
    session_key: str,
    daughter_id: Optional[str],
    latency_ms: Optional[int] = None,
) -> ShadowTelemetryEnvelope:
    """Build an observation-only telemetry envelope.

    The correlation hash is intentionally one-way and derived from runtime identifiers.
    Raw message text, transcript, child name, authority scope, and direct identifiers are
    excluded from the envelope.
    """
    raw = f"{daughter_id or 'none'}|{session_key or 'default'}".encode("utf-8")
    correlation_hash = sha256(raw).hexdigest()
    safe_latency = None if latency_ms is None else max(0, int(latency_ms))
    return ShadowTelemetryEnvelope(
        correlation_hash=correlation_hash,
        comparison=comparison.telemetry(),
        resolver_version=resolver_version,
        comparator_version=comparison.telemetry_version,
        latency_ms=safe_latency,
    )
