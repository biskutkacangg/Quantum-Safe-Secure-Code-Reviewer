# ============================================================
# pqc_agent/cli.py
# Production DevSecOps CLI Entrypoint for PQC Code Review
# ============================================================
"""
Production-grade Command-Line Interface (CLI) for DevSecOps automation.
Enables headless scanning of repositories in CI/CD pipelines, pre-commit
hooks, and batch security review jobs.

Usage:
    python -m pqc_agent.cli scan --target src/ --fail-on CRITICAL --output-json audit.json
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
from pathlib import Path
from typing import Any

from pqc_agent.audit import generate_audit_json, generate_audit_txt
from pqc_agent.state import AuditEntry
from pqc_agent.tools import code_scanner_tool, pqc_patch_generator_tool


SEVERITY_LEVELS = {
    "NONE": 0,
    "INFO": 1,
    "LOW": 2,
    "MEDIUM": 3,
    "HIGH": 4,
    "CRITICAL": 5,
}


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load configuration from YAML or fallback to defaults."""
    default_config: dict[str, Any] = {
        "policy": {
            "fail_on_severity": "CRITICAL",
            "max_allowed_findings": 0,
        },
        "scanner": {
            "include_patterns": ["*.py", "*.java"],
            "exclude_patterns": [
                "*.venv*", "*venv*", "*node_modules*", "*tests*", "*test_*",
                "*vendor*", "*build*", "*dist*", "*.git*"
            ],
        },
        "audit": {
            "output_directory": "audit_outputs",
        },
    }

    if config_path and Path(config_path).exists():
        try:
            import yaml
            with open(config_path, "r", encoding="utf-8") as f:
                loaded = yaml.safe_load(f)
                if loaded and isinstance(loaded, dict):
                    default_config.update(loaded)
        except Exception as e:
            print(f"[WARN] Failed to load config from {config_path}: {e}. Using defaults.", file=sys.stderr)

    return default_config


def should_scan_file(file_path: Path, include_patterns: list[str], exclude_patterns: list[str]) -> bool:
    """Check whether a file matches include and not exclude patterns."""
    str_path = str(file_path).replace("\\", "/")
    
    # Check exclusion first
    for excl in exclude_patterns:
        if fnmatch.fnmatch(str_path, excl) or fnmatch.fnmatch(file_path.name, excl):
            return False

    # Check inclusion
    for incl in include_patterns:
        if fnmatch.fnmatch(str_path, incl) or fnmatch.fnmatch(file_path.name, incl):
            return True

    return False


def scan_target(
    target_path: Path,
    include_patterns: list[str],
    exclude_patterns: list[str],
) -> tuple[list[dict], list[dict]]:
    """Scan a file or directory recursively."""
    all_findings: list[dict] = []
    audit_entries: list[dict] = []

    files_to_scan: list[Path] = []
    if target_path.is_file():
        files_to_scan.append(target_path)
    elif target_path.is_dir():
        for root, dirs, files in os.walk(target_path):
            # Prune excluded directories in-place
            dirs[:] = [
                d for d in dirs
                if not any(fnmatch.fnmatch(d, p.strip("*/")) for p in exclude_patterns)
            ]
            for file in files:
                p = Path(root) / file
                if should_scan_file(p, include_patterns, exclude_patterns):
                    files_to_scan.append(p)

    audit_entries.append(
        AuditEntry(
            actor="system",
            action="SCAN_START",
            detail=f"Initiated headless scan of {len(files_to_scan)} file(s) in {target_path}",
        ).model_dump()
    )

    for fpath in files_to_scan:
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                code = f.read()

            lang = "python" if fpath.suffix.lower() == ".py" else "java" if fpath.suffix.lower() == ".java" else "unknown"
            if lang == "unknown":
                continue

            raw_res = code_scanner_tool.invoke({
                "source_code": code,
                "file_name": str(fpath),
                "language": lang,
            })
            findings = json.loads(raw_res)
            for item in findings:
                item["file_path"] = str(fpath)
            all_findings.extend(findings)

        except Exception as e:
            print(f"[ERROR] Failed scanning {fpath}: {e}", file=sys.stderr)

    audit_entries.append(
        AuditEntry(
            actor="agent",
            action="SCAN_COMPLETE",
            detail=f"Completed scan. Total findings detected: {len(all_findings)}",
            metadata={"findings_count": len(all_findings)},
        ).model_dump()
    )

    return all_findings, audit_entries


def format_table(findings: list[dict]) -> str:
    """Format findings into a clean CLI table."""
    if not findings:
        return "[CLEAN] No legacy cryptographic primitives detected."

    lines = [
        "=" * 88,
        f"{'SEVERITY':<10} | {'ALGORITHM':<12} | {'LINE':<6} | {'FILE PATH':<28} | {'CONFIDENCE':<10}",
        "-" * 88,
    ]
    for f in findings:
        sev = f.get("severity", "UNKNOWN")
        algo = f.get("algorithm_detected", "UNKNOWN")
        line = str(f.get("line_number", 0))
        fpath = Path(f.get("file_path", "unknown")).name[:28]
        conf = f"{f.get('confidence', 0.0):.2f}"
        lines.append(f"{sev:<10} | {algo:<12} | {line:<6} | {fpath:<28} | {conf:<10}")

    lines.append("=" * 88)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="PQC Secure-Code Reviewer — DevSecOps Static Analysis Engine",
        prog="pqc-review",
    )
    parser.add_argument(
        "--target",
        "-t",
        default=".",
        help="Target file or directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--config",
        "-c",
        default="pqc_config.yaml",
        help="Path to pqc_config.yaml (default: pqc_config.yaml)",
    )
    parser.add_argument(
        "--fail-on",
        choices=["NONE", "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
        default=None,
        help="Override fail-on severity threshold from config",
    )
    parser.add_argument(
        "--generate-patches",
        action="store_true",
        help="Generate post-quantum FIPS 203/204 replacement patches for detected findings",
    )
    parser.add_argument(
        "--output-json",
        help="Output file path for tamper-evident JSON audit trail",
    )
    parser.add_argument(
        "--output-txt",
        help="Output file path for human-readable TXT audit trail",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress console output (exit code only)",
    )

    args = parser.parse_args(argv)

    config = load_config(args.config)
    policy = config.get("policy", {})
    scanner_cfg = config.get("scanner", {})

    fail_on = args.fail_on or policy.get("fail_on_severity", "CRITICAL")
    fail_threshold = SEVERITY_LEVELS.get(fail_on, 5)

    include_pats = scanner_cfg.get("include_patterns", ["*.py", "*.java"])
    exclude_pats = scanner_cfg.get("exclude_patterns", ["*.venv*", "*venv*"])

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"[ERROR] Target path '{target_path}' does not exist.", file=sys.stderr)
        return 2

    findings, audit_entries = scan_target(target_path, include_pats, exclude_pats)

    patches = []
    if args.generate_patches and findings:
        patches_raw = pqc_patch_generator_tool.invoke({"findings_json": json.dumps(findings)})
        patches = json.loads(patches_raw)
        audit_entries.append(
            AuditEntry(
                actor="agent",
                action="PATCH_GENERATION_COMPLETE",
                detail=f"Generated {len(patches)} NIST-compliant PQC replacement patches.",
            ).model_dump()
        )

    # Save audit trail if requested
    meta = {
        "target": str(target_path),
        "total_findings": len(findings),
        "total_patches": len(patches),
        "fail_on_severity": fail_on,
    }

    if args.output_json:
        json_report = generate_audit_json(audit_entries, meta)
        out_p = Path(args.output_json)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(json_report)
        if not args.silent:
            print(f"[INFO] Audit JSON saved to: {out_p}")

    if args.output_txt:
        txt_report = generate_audit_txt(audit_entries, meta)
        out_p = Path(args.output_txt)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            f.write(txt_report)
        if not args.silent:
            print(f"[INFO] Audit TXT saved to: {out_p}")

    if not args.silent:
        print("\n" + format_table(findings))
        if patches:
            print(f"\n[INFO] Generated {len(patches)} PQC migration patches for detected vulnerabilities.")

    # Check policy threshold
    violating_findings = [
        f for f in findings
        if SEVERITY_LEVELS.get(f.get("severity", "LOW"), 0) >= fail_threshold
    ]

    if violating_findings:
        if not args.silent:
            print(
                f"\n[FAIL] Policy violation: Found {len(violating_findings)} finding(s) "
                f"at or above severity '{fail_on}'.",
                file=sys.stderr,
            )
        return 1

    if not args.silent:
        print(f"\n[PASS] Cryptographic compliance check passed for {target_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
