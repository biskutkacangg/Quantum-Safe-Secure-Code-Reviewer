"""
generate_structure_pdf.py — Compiles a high-impact, visual presentation PDF
of the complete Project Structure and File Breakdown for team/friend walkthroughs.
Uses headless Microsoft Edge to render pixel-perfect vector PDF.
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("c:/Users/User/hackathon-cybersecurity-agents")
HTML_FILE = WORKSPACE / "PQC_Project_Structure_Presentation.html"
PDF_FILE = WORKSPACE / "PQC_Project_Structure_Presentation.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PQC Secure-Code Reviewer — Project Structure & File Guide</title>
<style>
    @page {
        size: A4;
        margin: 14mm 14mm 16mm 14mm;
        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-size: 8pt;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #64748b;
        }
    }

    * {
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #0f172a;
        background: #ffffff;
        line-height: 1.45;
        font-size: 9pt;
        margin: 0;
        padding: 0;
    }

    /* Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #312e81 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 14px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }

    .hero-banner h1 {
        font-size: 17pt;
        margin: 0 0 4px 0;
        font-weight: 800;
        letter-spacing: -0.3px;
        color: #f8fafc;
    }

    .hero-banner .subtitle {
        font-size: 9.5pt;
        color: #c7d2fe;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .badges {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }

    .badge {
        font-size: 7pt;
        font-weight: 700;
        padding: 2.5px 7px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .b-indigo { background: rgba(99, 102, 241, 0.25); color: #e0e7ff; border: 1px solid #818cf8; }
    .b-green  { background: rgba(34, 197, 94, 0.25); color: #bbf7d0; border: 1px solid #4ade80; }
    .b-cyan   { background: rgba(6, 182, 212, 0.25); color: #cffafe; border: 1px solid #22d3ee; }
    .b-amber  { background: rgba(245, 158, 11, 0.25); color: #fef3c7; border: 1px solid #fbbf24; }

    /* Section Headings */
    h2 {
        font-size: 12pt;
        color: #1e1b4b;
        font-weight: 800;
        border-left: 4px solid #4f46e5;
        padding-left: 8px;
        margin: 16px 0 8px 0;
        page-break-after: avoid;
    }

    h3 {
        font-size: 9.8pt;
        color: #334155;
        font-weight: 700;
        margin: 10px 0 4px 0;
        page-break-after: avoid;
    }

    p {
        margin: 4px 0;
        text-align: justify;
    }

    .callout {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #6366f1;
        padding: 8px 12px;
        border-radius: 5px;
        font-size: 8.8pt;
        margin: 10px 0;
    }

    /* Directory Tree Block */
    .tree-box {
        background: #0f172a;
        color: #e2e8f0;
        padding: 12px 14px;
        border-radius: 6px;
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 7.6pt;
        line-height: 1.35;
        margin: 8px 0 14px 0;
        page-break-inside: avoid;
    }

    .tree-box .folder { color: #38bdf8; font-weight: bold; }
    .tree-box .file   { color: #f1f5f9; }
    .tree-box .comm   { color: #94a3b8; font-style: italic; }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0 12px 0;
        font-size: 8pt;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 5px 8px;
        text-align: left;
        vertical-align: top;
    }

    th {
        background: #f1f5f9;
        color: #1e293b;
        font-weight: 700;
    }

    tr:nth-child(even) td {
        background: #f8fafc;
    }

    .mono {
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 7.5pt;
        color: #4338ca;
        font-weight: 600;
    }

    /* Workflow Cards */
    .workflow-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px 0;
        page-break-inside: avoid;
    }

    .workflow-card {
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 10px 12px;
        background: #ffffff;
    }

    .workflow-card.web {
        border-top: 3px solid #6366f1;
    }

    .workflow-card.cli {
        border-top: 3px solid #059669;
    }

    .workflow-card h4 {
        margin: 0 0 6px 0;
        font-size: 9pt;
        color: #0f172a;
    }

    .step-list {
        margin: 0;
        padding-left: 14px;
        font-size: 7.8pt;
        color: #334155;
    }

    .step-list li {
        margin-bottom: 3.5px;
    }

    .page-break {
        page-break-before: always;
    }

    .cheatsheet {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px 12px;
        margin-top: 10px;
        page-break-inside: avoid;
    }
</style>
</head>
<body>

<!-- HERO BANNER -->
<div class="hero-banner">
    <h1>🛡️ PQC Secure-Code Reviewer Agent</h1>
    <div class="subtitle">Complete Architectural Anatomy &amp; File-by-File Technical Guide</div>
    <div class="badges">
        <span class="badge b-indigo">Agentic Cyber Defence</span>
        <span class="badge b-green">NIST FIPS 203 (ML-KEM)</span>
        <span class="badge b-cyan">NIST FIPS 204 (ML-DSA)</span>
        <span class="badge b-amber">Zero-Trust HITL Gate</span>
        <span class="badge b-indigo">SHA-256 Hash Chaining</span>
    </div>
</div>

<div class="callout">
    <strong>Project Summary for Collaborators:</strong> An autonomous yet strictly governed AI security tool designed to find and remediate quantum-vulnerable cryptographic algorithms (RSA, ECC, DES) in source code. It uses deterministic AST parsing, LLM Chain-of-Thought (CoT) reasoning, non-negotiable Human-in-the-Loop (HITL) approval, and produces a tamper-evident SHA-256 audit log.
</div>

<!-- SECTION 1: VISUAL TREE -->
<h2>1. Project Directory Anatomy</h2>
<p>The codebase is organized into modular layers ensuring clear separation between the presentation tier, agent logic, detection tools, testbench, and DevSecOps pipelines:</p>

<div class="tree-box">
<span class="folder">hackathon-cybersecurity-agents/</span>
├── <span class="file">app.py</span>                              <span class="comm"># Streamlit interactive Web Dashboard (Port 8501)</span>
├── <span class="file">pqc_config.yaml</span>                     <span class="comm"># Enterprise policy & target NIST algorithms</span>
├── <span class="file">requirements.txt</span>                    <span class="comm"># Production Python dependency manifest</span>
├── <span class="file">Dockerfile</span> &amp; <span class="file">docker-compose.yml</span>       <span class="comm"># Hardened multi-stage container deployment</span>
│
├── <span class="folder">pqc_agent/</span>                          <span class="comm"># Core Agent Python Package</span>
│   ├── <span class="file">__init__.py</span>                     <span class="comm"># Public exports &amp; package initializer</span>
│   ├── <span class="file">state.py</span>                        <span class="comm"># LangGraph AgentState TypedDict &amp; Pydantic models</span>
│   ├── <span class="file">tools.py</span>                        <span class="comm"># AST/Regex scanner &amp; FIPS 203/204 patch generator</span>
│   ├── <span class="file">prompts.py</span>                      <span class="comm"># System prompts &amp; Chain-of-Thought templates</span>
│   ├── <span class="file">graph.py</span>                        <span class="comm"># 5-node LangGraph pipeline &amp; interrupt() HITL gate</span>
│   ├── <span class="file">audit.py</span>                        <span class="comm"># Cryptographic SHA-256 recursive hash chain logger</span>
│   └── <span class="file">cli.py</span>                          <span class="comm"># Headless DevSecOps CLI engine for CI/CD runs</span>
│
├── <span class="folder">sample_files/</span>                       <span class="comm"># Testbench: intentionally vulnerable code samples</span>
│   ├── <span class="file">vulnerable_python.py</span>            <span class="comm"># Python sample (RSA, ECDSA, DES, MD5, AES-128)</span>
│   └── <span class="file">VulnerableJava.java</span>             <span class="comm"># Java sample (RSA, ECDSA, DSA, DES, MD5, DH)</span>
│
├── <span class="folder">.github/workflows/</span>                  <span class="comm"># Automated DevSecOps CI/CD Pipelines</span>
│   ├── <span class="file">ci.yml</span>                          <span class="comm"># Unit tests &amp; LangGraph E2E verification</span>
│   └── <span class="file">security-scan.yml</span>               <span class="comm"># SAST (Bandit), SCA (pip-audit), PQC audit gate</span>
│
├── <span class="file">test_pqc_agent.py</span>                   <span class="comm"># Automated unit &amp; tool integration test suite</span>
├── <span class="file">test_graph_e2e.py</span>                   <span class="comm"># End-to-end LangGraph HITL interrupt &amp; resume test</span>
└── <span class="folder">audit_outputs/</span>                      <span class="comm"># Generated tamper-evident audit logs (JSON &amp; TXT)</span>
</div>

<!-- SECTION 2: CORE PACKAGE -->
<h2>2. The Core Agent Engine (`pqc_agent/`)</h2>
<p>The primary intelligence and execution mechanisms reside within the <span class="mono">pqc_agent/</span> package:</p>

<table>
    <thead>
        <tr>
            <th style="width: 26%;">File</th>
            <th>Role &amp; Responsibilities</th>
            <th style="width: 32%;">Key Components Inside</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="mono">pqc_agent/state.py</span></td>
            <td><strong>State Schema &amp; Data Contract</strong><br>Defines the canonical TypedDict and Pydantic models flowing through every LangGraph node.</td>
            <td>• <span class="mono">AgentState</span> (TypedDict)<br>• <span class="mono">CryptoFinding</span> (Line, severity, conf)<br>• <span class="mono">PQCPatch</span> (Diff, FIPS standard)<br>• <span class="mono">AuditEntry</span> (Actor, action, timestamp)</td>
        </tr>
        <tr>
            <td><span class="mono">pqc_agent/tools.py</span></td>
            <td><strong>Scanning &amp; Patch Synthesis Engine</strong><br>Performs AST-based (Python) and regex (Java) detection; rewrites legacy calls to NIST ML-KEM/ML-DSA.</td>
            <td>• <span class="mono">code_scanner_tool</span> (AST Visitor)<br>• <span class="mono">pqc_patch_generator_tool</span><br>• <span class="mono">LEGACY_CRYPTO_DB</span> (Knowledge base)<br>• Template synthesizers (liboqs / Bouncy Castle)</td>
        </tr>
        <tr>
            <td><span class="mono">pqc_agent/graph.py</span></td>
            <td><strong>LangGraph State Machine (The Brain)</strong><br>Orchestrates the 5-node workflow. Pauses at human approval using native <span class="mono">interrupt()</span>.</td>
            <td>• <span class="mono">node_ingest</span> (Validation &amp; genesis hash)<br>• <span class="mono">node_scan</span> (Deterministic scan)<br>• <span class="mono">node_investigate</span> (LLM CoT reasoning)<br>• <span class="mono">node_human_approval</span> (HITL Gate)<br>• <span class="mono">node_finalise</span> (Seals audit trail)</td>
        </tr>
        <tr>
            <td><span class="mono">pqc_agent/prompts.py</span></td>
            <td><strong>LLM Cognitive Guidance</strong><br>Prompts defining the agent's persona, rules, and structured investigation questions.</td>
            <td>• <span class="mono">SYSTEM_PROMPT</span> (Persona &amp; NIST rules)<br>• <span class="mono">INVESTIGATION_PROMPT</span> (CoT &amp; uncertainty)<br>• <span class="mono">PATCH_SUMMARY_PROMPT</span> (FIPS notes)</td>
        </tr>
        <tr>
            <td><span class="mono">pqc_agent/audit.py</span></td>
            <td><strong>Cryptographic Provenance Engine</strong><br>Creates tamper-evident logs using a recursive SHA-256 hash chain for non-repudiation.</td>
            <td>• <span class="mono">_compute_chain_hash()</span><br>• <span class="mono">generate_audit_json()</span><br>• <span class="mono">generate_audit_txt()</span></td>
        </tr>
        <tr>
            <td><span class="mono">pqc_agent/cli.py</span></td>
            <td><strong>Headless DevSecOps Scanner</strong><br>CLI tool for CI/CD runners. Reads policy, scans files, generates patches, and returns exit codes.</td>
            <td>• <span class="mono">scan_target()</span> recursive walker<br>• Policy violation gate (Exit 0, 1, 2)<br>• Automated JSON/TXT report export</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<!-- SECTION 3: APP & DEVSECOPS -->
<h2>3. Presentation, Testbench &amp; DevSecOps Layer</h2>

<table>
    <thead>
        <tr>
            <th style="width: 26%;">File / Directory</th>
            <th>Role &amp; Responsibilities</th>
            <th style="width: 32%;">Key Features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="mono">app.py</span></td>
            <td><strong>Interactive Web Dashboard</strong><br>The user-facing Streamlit application offering a clean cybersecurity control center.</td>
            <td>• Dark glassmorphic theme (Port 8501)<br>• Visual 5-phase execution tracker<br>• Side-by-side code diff comparison<br>• Approve/Reject HITL resume buttons<br>• Instant JSON/TXT audit trail download</td>
        </tr>
        <tr>
            <td><span class="mono">pqc_config.yaml</span></td>
            <td><strong>Enterprise Policy Configuration</strong><br>Defines policy failure thresholds, target NIST algorithms, and hybrid pairings.</td>
            <td>• <span class="mono">fail_on_severity: CRITICAL</span><br>• <span class="mono">targets: ML-KEM-768, ML-DSA-65</span><br>• File inclusion/exclusion globs</td>
        </tr>
        <tr>
            <td><span class="mono">sample_files/</span></td>
            <td><strong>Vulnerable Code Testbench</strong><br>Intentionally vulnerable Python and Java files used to validate detection and patching.</td>
            <td>• <span class="mono">vulnerable_python.py</span> (21 findings)<br>• <span class="mono">VulnerableJava.java</span> (12 findings)<br>• Covers RSA, ECDSA, DSA, DES, MD5, DH</td>
        </tr>
        <tr>
            <td><span class="mono">test_pqc_agent.py</span></td>
            <td><strong>Unit &amp; Integration Test Suite</strong><br>Validates scanner detection, patch generation, hash chaining, and graph compilation.</td>
            <td>• Automated assertion of 33+ findings<br>• Verifies SHA-256 chain length &amp; integrity<br>• Verifies AST vs regex accuracy</td>
        </tr>
        <tr>
            <td><span class="mono">test_graph_e2e.py</span></td>
            <td><strong>E2E LangGraph State Machine Test</strong><br>Proves the <span class="mono">interrupt()</span> pause and <span class="mono">Command(resume=...)</span> unblocking lifecycle.</td>
            <td>• Verifies graph halts at node 4<br>• Tests resume with human decision<br>• Verifies final sealed audit trail</td>
        </tr>
        <tr>
            <td><span class="mono">.github/workflows/</span></td>
            <td><strong>Continuous Integration &amp; Security</strong><br>Automated GitHub Actions running quality and cryptographic gates on every commit.</td>
            <td>• <span class="mono">ci.yml</span>: Matrix tests (Python 3.11, 3.12)<br>• <span class="mono">security-scan.yml</span>: Bandit + pip-audit + PQC audit artifact upload</td>
        </tr>
        <tr>
            <td><span class="mono">Dockerfile</span> &amp; <br><span class="mono">docker-compose.yml</span></td>
            <td><strong>Production Containerization</strong><br>Hardened multi-stage container build adhering to CIS security benchmarks.</td>
            <td>• Unprivileged user (<span class="mono">pqcuser</span>, UID 10001)<br>• Dropped root capabilities<br>• Native healthcheck (<span class="mono">/_stcore/health</span>)<br>• Persistent volume for audit outputs</td>
        </tr>
    </tbody>
</table>

<!-- SECTION 4: HOW FILES INTERACT -->
<h2>4. How the Files Interact (Runtime Workflow Sequences)</h2>
<p>To explain the architecture to your team, walk them through the two primary execution workflows:</p>

<div class="workflow-grid">
    <div class="workflow-card web">
        <h4>🌐 Workflow A: Interactive Web Review (`app.py`)</h4>
        <ol class="step-list">
            <li>User uploads code or selects a sample in <strong><span class="mono">app.py</span></strong>.</li>
            <li><strong><span class="mono">app.py</span></strong> initiates the LangGraph state machine in <strong><span class="mono">pqc_agent/graph.py</span></strong>.</li>
            <li><strong>Node 1 (Ingest):</strong> Ingests file, generates genesis hash via <strong><span class="mono">audit.py</span></strong>.</li>
            <li><strong>Node 2 (Scan):</strong> Deterministically calls <strong><span class="mono">tools.py</span></strong> (AST visitor) to detect vulnerabilities.</li>
            <li><strong>Node 3 (Investigate):</strong> Calls <strong><span class="mono">tools.py</span></strong> for patches and queries LLM via <strong><span class="mono">prompts.py</span></strong>.</li>
            <li><strong>Node 4 (HITL Gate):</strong> LangGraph <strong>pauses</strong> via <span class="mono">interrupt()</span>.</li>
            <li><strong><span class="mono">app.py</span></strong> renders findings, CoT reasoning, and diffs.</li>
            <li>Human clicks <em>Approve</em>; <strong><span class="mono">app.py</span></strong> calls <span class="mono">Command(resume=...)</span>.</li>
            <li><strong>Node 5 (Finalise):</strong> Seals decision and writes SHA-256 audit log.</li>
        </ol>
    </div>

    <div class="workflow-card cli">
        <h4>⚡ Workflow B: Headless CI/CD Pipeline (`cli.py`)</h4>
        <ol class="step-list">
            <li>CI/CD runner executes: <br><span class="mono">python -m pqc_agent.cli --target src/</span></li>
            <li><strong><span class="mono">cli.py</span></strong> loads policy rules from <strong><span class="mono">pqc_config.yaml</span></strong>.</li>
            <li><strong><span class="mono">cli.py</span></strong> recursively scans files using <strong><span class="mono">tools.py</span></strong> without needing web UI or LLM tokens.</li>
            <li>If <span class="mono">--generate-patches</span> is passed, it generates NIST FIPS 203/204 replacement snippets.</li>
            <li><strong><span class="mono">cli.py</span></strong> invokes <strong><span class="mono">audit.py</span></strong> to save tamper-evident JSON/TXT logs.</li>
            <li><strong><span class="mono">cli.py</span></strong> checks violations against policy:
                <br>• If findings &ge; CRITICAL: <strong>Exit Code 1</strong> (Build fails).
                <br>• If clean: <strong>Exit Code 0</strong> (Build passes).</li>
        </ol>
    </div>
</div>

<!-- SECTION 5: COMMAND CHEATSHEET -->
<h2>5. Quick Commands Cheatsheet for Team Demos</h2>
<div class="cheatsheet">
    <table style="margin: 0; font-size: 7.8pt;">
        <tr>
            <td style="width: 32%;"><strong>Launch Web Dashboard</strong></td>
            <td><span class="mono">streamlit run app.py</span></td>
            <td>Opens interactive dark UI at http://localhost:8501</td>
        </tr>
        <tr>
            <td><strong>Run Headless CLI Scan</strong></td>
            <td><span class="mono">python -m pqc_agent.cli --target sample_files/ --generate-patches</span></td>
            <td>Prints vulnerability table &amp; generates PQC patches</td>
        </tr>
        <tr>
            <td><strong>Run Unit &amp; Tool Tests</strong></td>
            <td><span class="mono">python test_pqc_agent.py</span></td>
            <td>Tests AST scanner, patch generator &amp; hash chaining</td>
        </tr>
        <tr>
            <td><strong>Run LangGraph E2E Test</strong></td>
            <td><span class="mono">python test_graph_e2e.py</span></td>
            <td>Proves the interrupt pause &amp; resume cycle</td>
        </tr>
        <tr>
            <td><strong>Launch with Docker</strong></td>
            <td><span class="mono">docker compose up -d --build</span></td>
            <td>Starts containerized app on port 8501</td>
        </tr>
    </table>
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

print("Compiling project structure presentation PDF via Edge headless...")
result = subprocess.run(cmd, capture_output=True, text=True)

if PDF_FILE.exists() and PDF_FILE.stat().st_size > 0:
    print(f"SUCCESS: PDF created at: {PDF_FILE} ({PDF_FILE.stat().st_size:,} bytes)")
    downloads_pdf = Path("C:/Users/User/Downloads/PQC_Project_Structure_Presentation.pdf")
    downloads_pdf.write_bytes(PDF_FILE.read_bytes())
    print(f"Copied to Downloads: {downloads_pdf}")
    sys.exit(0)
else:
    print(f"ERROR: {result.stderr}")
    sys.exit(1)
