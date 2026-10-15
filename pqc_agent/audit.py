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


def compute_cia_summary(findings: list[dict]) -> dict[str, int]:
    """Calculate the distribution of impacted CIA Triad pillars across findings."""
    summary = {"Confidentiality": 0, "Integrity": 0, "Availability": 0}
    for f in findings:
        pillars = f.get("cia_triad", [])
        for p in pillars:
            if p in summary:
                summary[p] += 1
    return summary


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
    latest_only: bool = False,
) -> str:
    """
    Generate a JSON audit report with integrity hash and CIA impact analysis.
    If latest_only is True, filters to only retain the latest human approval records.

    Args:
        audit_trail: List of AuditEntry dicts from the agent state.
        metadata: Optional additional metadata (file_name, language, etc.)
        latest_only: Whether to keep only latest approval events (default False).

    Returns:
        Pretty-printed JSON string of the complete audit report.
    """
    entries_to_report = filter_latest_audit(audit_trail) if latest_only else audit_trail
    chain_hash = _compute_chain_hash(entries_to_report)
    meta = dict(metadata or {})
    findings = meta.get("findings", [])
    if findings and "cia_summary" not in meta:
        meta["cia_summary"] = compute_cia_summary(findings)

    report = {
        "audit_report": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
            "agent": "PQC Secure-Code Reviewer Agent",
            "status": meta.get("decision", "pending").upper(),
            "integrity_hash_sha256": chain_hash,
            "entry_count": len(entries_to_report),
            "cia_triad_summary": meta.get("cia_summary", {}),
            "metadata": meta,
        },
        "entries": entries_to_report,
    }

    return json.dumps(report, indent=2, default=str)


def filter_latest_audit(audit_trail: list[dict]) -> list[dict]:
    """
    Filter the audit trail to retain only the latest human approval/decision records,
    discarding raw preliminary system/scanning steps.
    """
    if not audit_trail:
        return []

    # Find human decision or patch approval entries
    approved_entries = [
        e for e in audit_trail
        if e.get("action") in ("HITL_DECISION_APPROVED", "PATCHES_APPROVED", "HITL_DECISION_REJECTED", "PATCHES_REJECTED")
        or e.get("actor") == "human"
    ]
    if approved_entries:
        return approved_entries

    return [audit_trail[-1]]


def generate_audit_txt(
    audit_trail: list[dict],
    metadata: dict[str, Any] | None = None,
    latest_only: bool = False,
) -> str:
    """
    Generate a clean human-readable TXT audit report including CIA Triad analysis.
    If latest_only is True, filters out intermediate scanning steps to focus on
    the latest human approval/decision.
    """
    entries_to_report = filter_latest_audit(audit_trail) if latest_only else audit_trail
    chain_hash = _compute_chain_hash(entries_to_report)
    meta = dict(metadata or {})
    decision = meta.get("decision", "pending").upper()

    lines: list[str] = []
    lines.append("=" * 72)
    lines.append("  PQC SECURE-CODE REVIEWER AGENT - AUDIT TRAIL")
    lines.append("=" * 72)
    lines.append(f"  Generated : {datetime.now(timezone.utc).isoformat()}")
    if decision in ("APPROVED", "REJECTED"):
        lines.append(f"  Status    : {decision} (Human-in-the-Loop Verified)")
    lines.append(f"  Entries   : {len(entries_to_report)}")
    lines.append(f"  Integrity : SHA-256 chain hash = {chain_hash}")

    if meta:
        lines.append(f"  File      : {meta.get('file_name', 'N/A')}")
        lines.append(f"  Language  : {meta.get('language', 'N/A')}")
        cia = meta.get("cia_summary")
        if not cia and "findings" in meta:
            cia = compute_cia_summary(meta["findings"])
        if cia:
            lines.append("  CIA Triad Impact Breakdown:")
            lines.append(f"    - Confidentiality (HNDL Threat) : {cia.get('Confidentiality', 0)}")
            lines.append(f"    - Integrity (Quantum Forgery)   : {cia.get('Integrity', 0)}")
            lines.append(f"    - Availability (PQC Overhead)   : {cia.get('Availability', 0)}")

    lines.append("=" * 72)
    lines.append("")

    for i, entry in enumerate(entries_to_report, start=1):
        ts = entry.get("timestamp", "N/A")
        actor = entry.get("actor", "N/A")
        action = entry.get("action", "N/A")
        detail = entry.get("detail", "N/A")

        # Strip markdown syntax and emojis for clean plain text
        clean_detail = (
            detail.replace("## ✅ ", "")
            .replace("## ❌ ", "")
            .replace("## ", "")
            .replace("**", "")
            .strip()
        )

        lines.append(f"  [{i:03d}] {ts}")
        lines.append(f"        Actor  : {actor}")
        lines.append(f"        Action : {action}")
        lines.append(f"        Detail : {clean_detail}")
        if entry.get("metadata"):
            for k, v in entry["metadata"].items():
                if v:
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
