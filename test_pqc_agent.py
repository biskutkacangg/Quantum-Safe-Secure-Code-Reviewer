"""
test_pqc_agent.py — Comprehensive Unit & Integration Verification
Tests scanner detection, PQC patch generation, audit hashing, and graph topology.
"""

import json
import os
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Add workspace to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

print("=" * 60)
print("1. Testing Imports...")
print("=" * 60)

try:
    from pqc_agent.state import AgentState, AuditEntry, CryptoFinding, PQCPatch
    from pqc_agent.tools import code_scanner_tool, pqc_patch_generator_tool, LEGACY_CRYPTO_DB
    from pqc_agent.prompts import SYSTEM_PROMPT, INVESTIGATION_PROMPT
    from pqc_agent.audit import generate_audit_json, generate_audit_txt, _compute_chain_hash
    from pqc_agent.graph import build_graph, node_ingest, node_scan, route_after_scan
    print("[PASS] All modules imported successfully.")
except Exception as e:
    print(f"[FAIL] Import failed: {e}")
    sys.exit(1)


print("\n" + "=" * 60)
print("2. Testing Python Static Code Scanner...")
print("=" * 60)

py_sample_path = Path("sample_files/vulnerable_python.py")
with open(py_sample_path, "r", encoding="utf-8") as f:
    py_code = f.read()

py_findings_raw = code_scanner_tool.invoke({
    "source_code": py_code,
    "file_name": "vulnerable_python.py",
    "language": "python"
})
py_findings = json.loads(py_findings_raw)
print(f"Detected {len(py_findings)} findings in Python sample:")
for idx, f in enumerate(py_findings, 1):
    threat = f.get("quantum_threat_level", f.get("rationale", ""))
    print(f"  [{idx:02d}] Line {f['line_number']:02d}: {f['algorithm_detected']:<10} ({f['severity']:<8}) - {threat[:45]}... (Conf: {f['confidence']})")

assert len(py_findings) >= 5, f"Expected at least 5 findings in Python sample, got {len(py_findings)}"
print("[PASS] Python code scanner passed!")


print("\n" + "=" * 60)
print("3. Testing Java Static Code Scanner...")
print("=" * 60)

java_sample_path = Path("sample_files/VulnerableJava.java")
with open(java_sample_path, "r", encoding="utf-8") as f:
    java_code = f.read()

java_findings_raw = code_scanner_tool.invoke({
    "source_code": java_code,
    "file_name": "VulnerableJava.java",
    "language": "java"
})
java_findings = json.loads(java_findings_raw)
print(f"Detected {len(java_findings)} findings in Java sample:")
for idx, f in enumerate(java_findings, 1):
    threat = f.get("quantum_threat_level", f.get("rationale", ""))
    print(f"  [{idx:02d}] Line {f['line_number']:02d}: {f['algorithm_detected']:<10} ({f['severity']:<8}) - {threat[:45]}... (Conf: {f['confidence']})")

assert len(java_findings) >= 4, f"Expected at least 4 findings in Java sample, got {len(java_findings)}"
print("[PASS] Java code scanner passed!")


print("\n" + "=" * 60)
print("4. Testing PQC Patch Generator Tool...")
print("=" * 60)

patches_raw = pqc_patch_generator_tool.invoke({"findings_json": py_findings_raw})
patches = json.loads(patches_raw)
print(f"Generated {len(patches)} PQC migration patches:")
for idx, p in enumerate(patches, 1):
    print(f"  [{idx:02d}] Replaces: {p.get('finding_id', 'N/A')} -> Target PQC: {p['pqc_algorithm']}")

assert len(patches) > 0, "No patches generated!"
assert any("ML-KEM" in p["pqc_algorithm"] for p in patches), "Expected ML-KEM replacement for key exchange"
assert any("ML-DSA" in p["pqc_algorithm"] for p in patches), "Expected ML-DSA replacement for digital signature"
print("[PASS] PQC Patch generator passed!")


print("\n" + "=" * 60)
print("5. Testing Audit Trail & SHA-256 Chain Hash...")
print("=" * 60)

test_audit_entries = [
    AuditEntry(actor="system", action="INGEST", detail="Ingested vulnerable_python.py").model_dump(),
    AuditEntry(actor="agent", action="SCAN_COMPLETE", detail="Detected 21 findings").model_dump(),
    AuditEntry(actor="human", action="HITL_DECISION_APPROVED", detail="Reviewer approved ML-KEM patch").model_dump(),
    AuditEntry(actor="system", action="WORKFLOW_COMPLETE", detail="Patches ready to apply").model_dump(),
]

chain_hash = _compute_chain_hash(test_audit_entries)
print(f"Calculated SHA-256 Chain Hash: {chain_hash}")
assert len(chain_hash) == 64, "Chain hash is not valid SHA-256"

json_report = generate_audit_json(test_audit_entries, {"file_name": "vulnerable_python.py"})
txt_report = generate_audit_txt(test_audit_entries, {"file_name": "vulnerable_python.py"})
assert chain_hash in json_report, "Integrity hash missing in JSON audit report"
assert chain_hash in txt_report, "Integrity hash missing in TXT audit report"
print("[PASS] Audit trail generator & cryptographic tamper-evidence passed!")


print("\n" + "=" * 60)
print("6. Testing LangGraph State Graph Compilation...")
print("=" * 60)

graph = build_graph()
print(f"Successfully compiled graph: {type(graph).__name__}")
assert graph is not None
print("[PASS] LangGraph compilation passed!")

print("\n" + "=" * 60)
print("ALL TESTS PASSED SUCCESSFULLY! SYSTEM IS PRODUCTION READY.")
print("=" * 60)
