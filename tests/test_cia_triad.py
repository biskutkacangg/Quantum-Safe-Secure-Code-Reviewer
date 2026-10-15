# ============================================================
# test_cia_triad.py — Unit Tests for CIA Triad Integration
# ============================================================
"""
Tests verification of CIA Triad mapping across:
1. LEGACY_CRYPTO_DB entries
2. Code scanner tool output findings
3. Audit summary computation and reporting (JSON & TXT)
"""

import json
import sys
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from pqc_agent.tools import LEGACY_CRYPTO_DB, code_scanner_tool
from pqc_agent.audit import compute_cia_summary, generate_audit_json, generate_audit_txt


def test_legacy_crypto_db_cia_impact():
    valid_pillars = {"Confidentiality", "Integrity", "Availability"}
    assert len(LEGACY_CRYPTO_DB) > 0
    for algo, entry in LEGACY_CRYPTO_DB.items():
        assert "cia_impact" in entry, f"Missing cia_impact in {algo}"
        assert isinstance(entry["cia_impact"], list), f"cia_impact in {algo} must be a list"
        assert len(entry["cia_impact"]) > 0, f"cia_impact in {algo} must not be empty"
        for pillar in entry["cia_impact"]:
            assert pillar in valid_pillars, f"Invalid pillar {pillar} in {algo}"
    print("[PASS] LEGACY_CRYPTO_DB cia_impact mapping verified.")


def test_code_scanner_findings_contain_cia_triad():
    sample_py = """
from cryptography.hazmat.primitives.asymmetric import rsa, ec
import hashlib

def example():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ec_key = ec.generate_private_key(ec.SECP256R1())
    h = hashlib.md5(b"test").hexdigest()
"""
    raw_results = code_scanner_tool.invoke({
        "source_code": sample_py,
        "file_name": "sample.py",
        "language": "python"
    })
    findings = json.loads(raw_results)
    assert len(findings) > 0, "Expected findings to be detected"
    for f in findings:
        assert "cia_triad" in f, f"Finding {f.get('algorithm_detected')} missing cia_triad"
        assert isinstance(f["cia_triad"], list)
    print(f"[PASS] Code scanner output verified: {len(findings)} findings have cia_triad.")


def test_compute_cia_summary_and_audit():
    mock_findings = [
        {"algorithm_detected": "RSA", "cia_triad": ["Confidentiality", "Integrity"]},
        {"algorithm_detected": "ECDSA", "cia_triad": ["Integrity"]},
        {"algorithm_detected": "AES-128", "cia_triad": ["Confidentiality"]},
    ]
    summary = compute_cia_summary(mock_findings)
    assert summary["Confidentiality"] == 2
    assert summary["Integrity"] == 2
    assert summary["Availability"] == 0

    mock_audit = [
        {"timestamp": "2026-10-13T00:00:00Z", "actor": "agent", "action": "SCAN", "detail": "Test scan"}
    ]
    json_str = generate_audit_json(mock_audit, metadata={"findings": mock_findings})
    report = json.loads(json_str)
    assert "cia_triad_summary" in report["audit_report"]
    assert report["audit_report"]["cia_triad_summary"]["Confidentiality"] == 2

    txt_str = generate_audit_txt(mock_audit, metadata={"findings": mock_findings})
    assert "CIA Triad Impact Breakdown:" in txt_str
    assert "Confidentiality (HNDL Threat) : 2" in txt_str
    print("[PASS] CIA Triad audit computation & export formatting verified.")


if __name__ == "__main__":
    test_legacy_crypto_db_cia_impact()
    test_code_scanner_findings_contain_cia_triad()
    test_compute_cia_summary_and_audit()
    print("ALL CIA TRIAD TESTS PASSED!")
