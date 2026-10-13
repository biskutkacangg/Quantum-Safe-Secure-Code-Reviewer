# ============================================================
# pqc_agent/__init__.py
# PQC Secure-Code Reviewer Agent — Package Initialiser
# ============================================================
"""
Post-Quantum Cryptography (PQC) Secure-Code Reviewer Agent.

An agentic AI system that scans source code for legacy cryptographic
primitives (RSA, ECC, AES-CBC, DES, MD5, SHA-1 …), reasons about
quantum-vulnerability risk, proposes ML-KEM / ML-DSA migration
patches, and enforces a Human-in-the-Loop (HITL) approval gate
before committing any remediation — all while generating a complete,
timestamped audit trail.
"""

__version__ = "1.0.0"
__author__ = "PQC Migration Research Team"

from pqc_agent.state import AgentState, AuditEntry, CryptoFinding, PQCPatch
from pqc_agent.tools import code_scanner_tool, pqc_patch_generator_tool, LEGACY_CRYPTO_DB
from pqc_agent.graph import build_graph
from pqc_agent.audit import compute_cia_summary, generate_audit_json, generate_audit_txt

__all__ = [
    "__version__",
    "AgentState",
    "AuditEntry",
    "CryptoFinding",
    "PQCPatch",
    "code_scanner_tool",
    "pqc_patch_generator_tool",
    "LEGACY_CRYPTO_DB",
    "build_graph",
    "compute_cia_summary",
    "generate_audit_json",
    "generate_audit_txt",
]
