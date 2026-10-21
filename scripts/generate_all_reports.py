# ============================================================
# scripts/generate_all_reports.py
# Master Build Script: Re-compiles active project reports
# into reports/ and synchronizes them to Downloads.
# ============================================================

import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPTS_DIR.parent
REPORTS_DIR = WORKSPACE / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
HTML_DIR = REPORTS_DIR / "html"
HTML_DIR.mkdir(parents=True, exist_ok=True)

PYTHON_EXE = sys.executable

ACTIVE_REPORT_SCRIPTS = [
    ("Official Hackathon Proposal (1-2 Page PDF)", "generate_proposal_pdf.py"),
    ("System Framework & Architecture Dossier (2-Page PDF)", "generate_framework_and_architecture_pdf.py"),
    ("Executive Pitch Deck (6-Slide Presentation PDF)", "generate_pitch_deck_pdf.py"),
    ("High-Impact Digital Poster (1-Page PDF & Image)", "generate_poster_pdf.py"),
    ("Paper Comparative Review & Literature Review (4-Page)", "generate_papers_comparison_pdf.py"),
    ("Cryptographic Replacements Catalog (NIST FIPS 203/204)", "generate_catalog_pdf.py"),
    ("Lecturer Academic Presentation Slide Deck: AST Tree & Compiler Architecture (9-Slide)", "generate_lecturer_presentation_pdf.py"),
    ("Lecturer Presentation Master Script & Academic Defence Companion Guide (A4 Portrait)", "generate_presentation_script_companion_pdf.py"),
    ("NOTA RINGKAS ALL TERMS AND CODING (A4 Portrait Study Guide)", "generate_nota_ringkas_pdf.py"),
]

def run_all():
    print("=" * 65)
    print("REBUILDING ACTIVE PQC RESEARCH DELIVERABLES")
    print(f"Destination: {REPORTS_DIR}")
    print("=" * 65)

    success_count = 0
    for label, script_name in ACTIVE_REPORT_SCRIPTS:
        script_path = SCRIPTS_DIR / script_name
        if not script_path.exists():
            print(f"[SKIP] {script_name} not found.")
            continue

        print(f"\n[RUNNING] {label} ({script_name}) ...")
        res = subprocess.run([PYTHON_EXE, str(script_path)], cwd=str(WORKSPACE), capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[SUCCESS] {label} compiled cleanly.")
            success_count += 1
        else:
            print(f"[ERROR] {label} failed:")
            print(res.stderr or res.stdout)

    print("\n" + "=" * 65)
    print(f"ACTIVE DELIVERABLES COMPILED: {success_count} reports processed.")
    print(f"Destination: {REPORTS_DIR}")
    print("=" * 65)

if __name__ == "__main__":
    run_all()
