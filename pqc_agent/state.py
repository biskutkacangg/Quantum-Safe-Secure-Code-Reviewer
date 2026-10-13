# ============================================================
# pqc_agent/state.py
# LangGraph State Schema — Single Source of Truth
# ============================================================
"""
Defines the canonical TypedDict that flows through every node in the
LangGraph state machine.  Every field is documented so that downstream
nodes, tools, and the Streamlit UI can introspect the schema.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated, Any, Literal

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


# ── Pydantic sub-models used inside the state ──────────────────────

class CryptoFinding(BaseModel):
    """A single occurrence of a legacy cryptographic primitive."""

    finding_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    file_path: str = Field(..., description="Relative path of the scanned file")
    language: Literal["python", "java", "unknown"] = "unknown"
    line_number: int = Field(..., ge=1)
    code_snippet: str = Field(..., description="Verbatim source line(s)")
    algorithm_detected: str = Field(
        ...,
        description="Canonical name, e.g. RSA-2048, ECDSA-P256, AES-128-CBC",
    )
    category: Literal[
        "key_exchange",
        "digital_signature",
        "symmetric_encryption",
        "hashing",
        "other",
    ] = "other"
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"] = "HIGH"
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Scanner confidence that this is a true positive",
    )
    rationale: str = Field(
        "",
        description="Human-readable explanation of why this is flagged",
    )
    quantum_threat_level: str = Field(
        "",
        description="Explanation of quantum vulnerability (Shor / Grover impact)",
    )
    cia_triad: list[str] = Field(
        default_factory=list,
        description="CIA Triad pillars impacted (Confidentiality, Integrity, Availability)",
    )


class PQCPatch(BaseModel):
    """A proposed quantum-safe code patch for a single finding."""

    patch_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    finding_id: str = Field(..., description="Links back to CryptoFinding.finding_id")
    original_code: str = Field(..., description="Legacy code block to be replaced")
    patched_code: str = Field(..., description="PQC-safe replacement code")
    pqc_algorithm: str = Field(
        ...,
        description="Target algorithm, e.g. ML-KEM-768, ML-DSA-65",
    )
    migration_notes: str = Field(
        "",
        description="Caveats, compatibility notes, hybrid considerations",
    )
    is_hybrid: bool = Field(
        False,
        description="True if the patch uses a hybrid classical + PQC approach",
    )


class AuditEntry(BaseModel):
    """Immutable audit log entry."""

    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    actor: Literal["agent", "human", "system"] = "system"
    action: str = ""
    detail: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


# ── LangGraph State ────────────────────────────────────────────────

class AgentState(TypedDict):
    """
    Canonical state flowing through the PQC Reviewer LangGraph.

    Every node reads from / writes to this dict.  The ``messages``
    field is managed by LangGraph's built-in ``add_messages`` reducer
    so that tool calls and LLM responses accumulate correctly.
    """

    # --- LangGraph message history (managed by add_messages) ---
    messages: Annotated[list, add_messages]

    # --- Input artefacts ---
    source_code: str                          # Raw uploaded source code
    file_name: str                            # Original filename
    language: str                             # "python" | "java" | "unknown"

    # --- Scanner output ---
    findings: list[dict]                      # list[CryptoFinding.model_dump()]
    scan_summary: str                         # Natural-language summary

    # --- LLM reasoning ---
    chain_of_thought: str                     # Full CoT from the investigation node
    uncertainty_statement: str                # Explicit uncertainty / caveats
    risk_assessment: str                      # Composite risk narrative

    # --- Patches ---
    patches: list[dict]                       # list[PQCPatch.model_dump()]

    # --- Human-in-the-Loop ---
    human_decision: str                       # "approved" | "rejected" | "pending"
    human_feedback: str                       # Free-text reviewer comment

    # --- Audit trail ---
    audit_trail: list[dict]                   # list[AuditEntry.model_dump()]

    # --- Control flow helpers ---
    current_phase: str                        # Tracks which node is active
    error: str                                # Carries error messages
