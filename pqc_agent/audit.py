# ============================================================
# pqc_agent/audit.py
# Audit Trail Generator — Secure Timestamped Logging
# ============================================================
"""
Generates tamper-evident, timestamped audit logs in both JSON and
human-readable TXT formats.  Each entry is cryptographically
fingerprinted with SHA-256 for integrity verification.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _compute_chain_hash(entries: list[dict]) -> str:
    """
    Compute a SHA-256 chain hash over all entries to detect tampering.
    Each entry's hash includes the previous entry's hash, creating
    a blockchain-like integrity chain.
    """
    prev_hash = "0" * 64  # Genesis hash
    for entry in entries:
        payload = json.dumps(entry, sort_keys=True) + prev_hash
        prev_hash = hashlib.sha256(payload.encode()).hexdigest()
    return prev_hash


def generate_audit_json(
    audit_trail: list[dict],
    metadata: dict[str, Any] | None = None,
) -> str:
    """
    Generate a JSON audit report with integrity hash.

    Args:
        audit_trail: List of AuditEntry dicts from the agent state.
        metadata: Optional additional metadata (file_name, language, etc.)

    Returns:
        Pretty-printed JSON string of the complete audit report.
    """
    chain_hash = _compute_chain_hash(audit_trail)

    report = {
        "audit_report": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "agent": "PQC Secure-Code Reviewer Agent",
            "integrity_hash_sha256": chain_hash,
            "entry_count": len(audit_trail),
            "metadata": metadata or {},
        },
        "entries": audit_trail,
    }

    return json.dumps(report, indent=2, default=str)


def generate_audit_txt(
    audit_trail: list[dict],
    metadata: dict[str, Any] | None = None,
) -> str:
    """
    Generate a human-readable TXT audit report.

    Args:
        audit_trail: List of AuditEntry dicts from the agent state.
        metadata: Optional additional metadata.

    Returns:
        Formatted text string of the audit report.
    """
    chain_hash = _compute_chain_hash(audit_trail)
    lines: list[str] = []

    lines.append("=" * 72)
    lines.append("  PQC SECURE-CODE REVIEWER AGENT — AUDIT TRAIL")
    lines.append("=" * 72)
    lines.append(f"  Generated : {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"  Entries   : {len(audit_trail)}")
    lines.append(f"  Integrity : SHA-256 chain hash = {chain_hash}")

    if metadata:
        lines.append(f"  File      : {metadata.get('file_name', 'N/A')}")
        lines.append(f"  Language  : {metadata.get('language', 'N/A')}")

    lines.append("=" * 72)
    lines.append("")

    for i, entry in enumerate(audit_trail, start=1):
        lines.append(f"  [{i:03d}] {entry.get('timestamp', 'N/A')}")
        lines.append(f"        Actor  : {entry.get('actor', 'N/A')}")
        lines.append(f"        Action : {entry.get('action', 'N/A')}")
        lines.append(f"        Detail : {entry.get('detail', 'N/A')}")
        if entry.get("metadata"):
            for k, v in entry["metadata"].items():
                lines.append(f"        {k}: {v}")
        lines.append("")

    lines.append("=" * 72)
    lines.append("  END OF AUDIT TRAIL")
    lines.append("=" * 72)

    return "\n".join(lines)


def save_audit_file(
    audit_trail: list[dict],
    output_dir: str | Path = ".",
    file_name: str = "audit_trail",
    metadata: dict[str, Any] | None = None,
    formats: tuple[str, ...] = ("json", "txt"),
) -> dict[str, Path]:
    """
    Save audit trail to disk in the specified formats.

    Returns:
        Dict mapping format name to the saved file path.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: dict[str, Path] = {}

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if "json" in formats:
        json_path = output_dir / f"{file_name}_{timestamp}.json"
        json_path.write_text(
            generate_audit_json(audit_trail, metadata), encoding="utf-8"
        )
        saved["json"] = json_path

    if "txt" in formats:
        txt_path = output_dir / f"{file_name}_{timestamp}.txt"
        txt_path.write_text(
            generate_audit_txt(audit_trail, metadata), encoding="utf-8"
        )
        saved["txt"] = txt_path

    return saved
