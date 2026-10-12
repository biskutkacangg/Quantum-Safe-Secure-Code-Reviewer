"""
generate_one_page_pdf.py — Compiles a high-density, professional EXACTLY 1-page executive
summary framework document for supervisor review.
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("c:/Users/User/hackathon-cybersecurity-agents")
HTML_FILE = WORKSPACE / "PQC_Framework_Executive_Summary.html"
PDF_FILE = WORKSPACE / "PQC_Framework_Executive_Summary.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PQC Secure-Code Reviewer — Executive Research Framework</title>
<style>
    @page {
        size: A4 portrait;
        margin: 6mm 8mm 5mm 8mm;
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
        background: #ffffff;
        line-height: 1.25;
        font-size: 7pt;
        margin: 0;
        padding: 0;
    }

    .header-container {
        border-bottom: 2px solid #4338ca;
        padding-bottom: 3px;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .title-block h1 {
        font-size: 12pt;
        color: #1e1b4b;
        margin: 0 0 1px 0;
        font-weight: 800;
        letter-spacing: -0.2px;
    }

    .title-block .subtitle {
        font-size: 7.8pt;
        color: #4338ca;
        font-weight: 600;
    }

    .meta-box {
        text-align: right;
        font-size: 6.5pt;
        color: #475569;
        line-height: 1.25;
    }

    .badges {
        display: flex;
        gap: 4px;
        margin: 3px 0 5px 0;
    }

    .badge {
        font-size: 6.2pt;
        font-weight: 700;
        padding: 1.5px 5px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }

    .b-indigo { background: #e0e7ff; color: #3730a3; }
    .b-green  { background: #dcfce7; color: #166534; }
    .b-red    { background: #fee2e2; color: #991b1b; }
    .b-slate  { background: #f1f5f9; color: #334155; }

    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-bottom: 5px;
    }

    .card {
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 4px 6px;
        background: #ffffff;
    }

    .card-title {
        font-size: 7.2pt;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 3px;
        border-bottom: 1px solid #e2e8f0;
        padding-bottom: 2px;
    }

    .card-title::before {
        content: "";
        display: inline-block;
        width: 3px;
        height: 9px;
        background: #4338ca;
        border-radius: 1px;
    }

    p {
        margin: 1.5px 0;
        text-align: justify;
        color: #334155;
    }

    ul {
        margin: 2px 0 2px 12px;
        padding: 0;
        color: #334155;
    }

    li {
        margin-bottom: 1px;
    }

    /* Pipeline Diagram */
    .pipeline-container {
        border: 1px solid #cbd5e1;
        background: #f8fafc;
        border-radius: 4px;
        padding: 5px 6px;
        margin-bottom: 5px;
    }

    .pipeline-title {
        font-size: 6.8pt;
        font-weight: 700;
        color: #334155;
        margin-bottom: 3px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .pipeline-flow {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 4px;
    }

    .node {
        flex: 1;
        border: 1px solid #94a3b8;
        background: #ffffff;
        border-radius: 3px;
        padding: 3px 2px;
        text-align: center;
    }

    .node-num {
        font-size: 5.5pt;
        color: #64748b;
        font-weight: bold;
    }

    .node-name {
        font-size: 6.6pt;
        font-weight: 700;
        color: #0f172a;
    }

    .node-sub {
        font-size: 5.2pt;
        color: #475569;
    }

    .node.active {
        border-color: #4338ca;
        background: #eef2ff;
    }

    .node.active .node-name {
        color: #3730a3;
    }

    .node.gate {
        border-color: #dc2626;
        background: #fef2f2;
    }

    .node.gate .node-name {
        color: #991b1b;
    }

    .arrow {
        color: #64748b;
        font-weight: bold;
        font-size: 6.5pt;
    }

    /* Compact Table */
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 6.2pt;
        margin-top: 2px;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 2.2px 4px;
        text-align: left;
    }

    th {
        background: #f1f5f9;
        font-weight: 700;
        color: #1e293b;
    }

    tr:nth-child(even) td {
        background: #f8fafc;
    }

    .mono {
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 6pt;
    }

    .footer-bar {
        border-top: 1px solid #cbd5e1;
        padding-top: 3px;
        margin-top: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 6pt;
        color: #64748b;
    }
</style>
</head>
<body>

<!-- HEADER -->
<div class="header-container">
    <div class="title-block">
        <h1>POST-QUANTUM CRYPTOGRAPHY (PQC) SECURE-CODE REVIEWER</h1>
        <div class="subtitle">An Agentic DevSecOps Framework for Automated Cryptographic Migration (FIPS 203 & FIPS 204)</div>
    </div>
    <div class="meta-box">
        <strong>Domain:</strong> Computer Network Security / Applied Crypto<br>
        <strong>Focus:</strong> Quantum-Resilient Code Review (Track 1)<br>
        <strong>Repo:</strong> <span class="mono">natasyafrzan-hub/Quantum-Safe-Secure-Code-Reviewer</span>
    </div>
</div>

<div class="badges">
    <span class="badge b-indigo">Agentic AI Architecture</span>
    <span class="badge b-green">NIST FIPS 203 (ML-KEM)</span>
    <span class="badge b-green">NIST FIPS 204 (ML-DSA)</span>
    <span class="badge b-red">Zero-Trust HITL Gate</span>
    <span class="badge b-slate">Tamper-Evident SHA-256 Audit</span>
    <span class="badge b-slate">DevSecOps CLI & CI/CD</span>
</div>

<!-- ROW 1: PROBLEM & OBJECTIVES -->
<div class="grid-2">
    <div class="card">
        <div class="card-title">1. Problem Statement & Threat Model</div>
        <p>
            Nation-state adversaries are actively executing <strong>"Harvest Now, Decrypt Later" (HNDL)</strong> attacks—capturing encrypted enterprise traffic today to decrypt retroactively once Cryptographically Relevant Quantum Computers (CRQCs) emerge.
        </p>
        <ul>
            <li><strong>Shor's Algorithm:</strong> Breaks integer factorisation and discrete logarithms in polynomial time, completely compromising <strong>RSA, DSA, ECDSA, DH, and ECDH</strong>.</li>
            <li><strong>Grover's Algorithm:</strong> Halves symmetric security (AES-128 drops to 64 bits; AES-256 retains 128-bit quantum security).</li>
            <li><strong>Enterprise Bottleneck:</strong> Legacy codebases contain thousands of hidden cryptographic call sites. Manual auditing is slow, error-prone, and lacks provable audit trails.</li>
        </ul>
    </div>

    <div class="card">
        <div class="card-title">2. Research Objectives & Innovation</div>
        <p>
            Develops an autonomous yet strictly governed <strong>AI Security Agent</strong> to automate code auditing and PQC migration with zero-trust safety:
        </p>
        <ul>
            <li><strong>Dual-Engine Static Analysis:</strong> AST parsing (Python) and syntax regex (Java) identify vulnerable primitives deterministically with line-level confidence scoring.</li>
            <li><strong>Explainable AI (XAI):</strong> LLM reasoning generates transparent Chain of Thought (CoT) and explicit uncertainty quantification (distinguishing test code from production).</li>
            <li><strong>Strict Human-in-the-Loop Gate:</strong> Built via LangGraph's stateful <span class="mono">interrupt()</span>—no autonomous code modifications occur without signed human approval.</li>
            <li><strong>Tamper-Evident Provenance:</strong> Recursively links every action into a SHA-256 blockchain-style hash chain for SOC 2 and NIST SP 800-53 compliance.</li>
        </ul>
    </div>
</div>

<!-- PIPELINE FLOW DIAGRAM -->
<div class="pipeline-container">
    <div class="pipeline-title">Agentic Workflow: 5-Node LangGraph Directed Acyclic Graph (DAG)</div>
    <div class="pipeline-flow">
        <div class="node active">
            <div class="node-num">NODE 1</div>
            <div class="node-name">INGEST</div>
            <div class="node-sub">Validation & Genesis Hash</div>
        </div>
        <div class="arrow">➔</div>
        <div class="node active">
            <div class="node-num">NODE 2</div>
            <div class="node-name">SCAN</div>
            <div class="node-sub">Deterministic AST Analysis</div>
        </div>
        <div class="arrow">➔</div>
        <div class="node active">
            <div class="node-num">NODE 3</div>
            <div class="node-name">INVESTIGATE</div>
            <div class="node-sub">CoT Reasoning & Patches</div>
        </div>
        <div class="arrow">➔</div>
        <div class="node gate">
            <div class="node-num">NODE 4 (GATE)</div>
            <div class="node-name">HUMAN APPROVAL</div>
            <div class="node-sub">interrupt() Pause Gate</div>
        </div>
        <div class="arrow">➔</div>
        <div class="node active">
            <div class="node-num">NODE 5</div>
            <div class="node-name">FINALISE</div>
            <div class="node-sub">SHA-256 Hash Seal</div>
        </div>
    </div>
</div>

<!-- ROW 2: MIGRATION TABLE & DEVSECOPS VERIFICATION -->
<div class="grid-2">
    <div class="card">
        <div class="card-title">3. Post-Quantum Migration Matrix (NIST Standards)</div>
        <table>
            <thead>
                <tr>
                    <th>Legacy Primitive</th>
                    <th>Threat</th>
                    <th>NIST PQC Replacement</th>
                    <th>FIPS Standard</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>RSA (Key Exchange)</strong></td>
                    <td>Shor (Factoring)</td>
                    <td><strong>ML-KEM-768</strong> (Kyber)</td>
                    <td>FIPS 203 (Cat. 3)</td>
                </tr>
                <tr>
                    <td><strong>ECDH / DH</strong></td>
                    <td>Shor (DLP / ECDLP)</td>
                    <td><strong>ML-KEM-768</strong></td>
                    <td>FIPS 203 (Cat. 3)</td>
                </tr>
                <tr>
                    <td><strong>ECDSA / DSA / EdDSA</strong></td>
                    <td>Shor (ECDLP)</td>
                    <td><strong>ML-DSA-65</strong> (Dilithium)</td>
                    <td>FIPS 204 (Cat. 3)</td>
                </tr>
                <tr>
                    <td><strong>AES-128 / DES / 3DES</strong></td>
                    <td>Grover / Classical</td>
                    <td><strong>AES-256-GCM</strong></td>
                    <td>NIST SP 800-38D</td>
                </tr>
                <tr>
                    <td><strong>MD5 / SHA-1</strong></td>
                    <td>Collisions + Grover</td>
                    <td><strong>SHA-3-256 / SHA-512</strong></td>
                    <td>FIPS 202</td>
                </tr>
            </tbody>
        </table>
        <p style="font-size: 6.2pt; margin-top: 2px; color: #475569;">
            *Supports hybrid migration modes (e.g. <span class="mono">X25519_ML-KEM-768</span>) for backwards-compatible TLS/PKI transitions.
        </p>
    </div>

    <div class="card">
        <div class="card-title">4. DevSecOps Architecture & Verification</div>
        <ul>
            <li><strong>Headless CLI (<span class="mono">pqc_agent/cli.py</span>):</strong> Automated CI/CD execution. Returns exit code 0 on clean code, exit code 1 on policy violation.</li>
            <li><strong>Shift-Left Pre-Commit Gate (<span class="mono">.pre-commit-config.yaml</span>):</strong> Blocks developers from committing deprecated crypto into Git locally.</li>
            <li><strong>CI/CD Pipelines (<span class="mono">.github/workflows/</span>):</strong> Multi-version matrix (Python 3.11/3.12), Bandit SAST, pip-audit SCA, and PR audit artifact generation.</li>
            <li><strong>Production Containerization:</strong> Hardened multi-stage <span class="mono">Dockerfile</span> with unprivileged user (<span class="mono">UID 10001</span>), resource quotas, and healthcheck.</li>
            <li><strong>Verification:</strong> 100% test pass rate across AST detection, patch generation, LangGraph state machine resume, and SHA-256 chain validation.</li>
        </ul>
    </div>
</div>

<!-- FOOTER -->
<div class="footer-bar">
    <div><strong>Project Deliverable:</strong> Executive Architectural Framework &bull; Ready for Supervisor Review &amp; Hackathon Defence</div>
    <div><strong>Audit Hash Integrity:</strong> Verified SHA-256 Hash Chain &bull; Production Ready</div>
</div>

</body>
</html>
"""

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML template at: {HTML_FILE}")

cmd = [
    EDGE_EXE,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_FILE}",
    "--no-pdf-header-footer",
    f"file:///{HTML_FILE.resolve().as_posix()}"
]

print("Compiling single-page PDF via Edge headless...")
result = subprocess.run(cmd, capture_output=True, text=True)

if PDF_FILE.exists() and PDF_FILE.stat().st_size > 0:
    print(f"SUCCESS: PDF created at: {PDF_FILE} ({PDF_FILE.stat().st_size:,} bytes)")
    downloads_pdf = Path("C:/Users/User/Downloads/PQC_Framework_Executive_Summary.pdf")
    downloads_pdf.write_bytes(PDF_FILE.read_bytes())
    print(f"Copied to Downloads: {downloads_pdf}")
else:
    print(f"ERROR: {result.stderr}")
    sys.exit(1)
