"""
generate_pdf.py — Generates a publication-quality PDF of the
PQC Secure-Code Reviewer Production DevSecOps & AI Systems Blueprint.
Uses Microsoft Edge headless to render HTML/CSS into vector PDF.
"""

import os
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("c:/Users/User/hackathon-cybersecurity-agents")
HTML_FILE = WORKSPACE / "PQC_Secure_Code_Reviewer_Blueprint.html"
PDF_FILE = WORKSPACE / "PQC_Secure_Code_Reviewer_Blueprint.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PQC Secure-Code Reviewer — DevSecOps & AI Systems Architectural Blueprint</title>
<style>
    @page {
        size: A4;
        margin: 18mm 16mm 20mm 16mm;
        @bottom-right {
            content: "Page " counter(page);
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
        background-color: #ffffff;
        line-height: 1.55;
        font-size: 10pt;
        margin: 0;
        padding: 0;
    }

    h1, h2, h3, h4 {
        color: #091e42;
        font-weight: 700;
        margin-top: 1.3em;
        margin-bottom: 0.4em;
        page-break-after: avoid;
    }

    h1 {
        font-size: 20pt;
        line-height: 1.2;
        border-bottom: 2.5px solid #4f46e5;
        padding-bottom: 8px;
        margin-top: 0;
    }

    h2 {
        font-size: 13.5pt;
        border-left: 4px solid #4f46e5;
        padding-left: 8px;
        margin-top: 1.6em;
    }

    h3 {
        font-size: 11pt;
        color: #1e293b;
    }

    p {
        margin: 0.5em 0;
        text-align: justify;
    }

    .badge-bar {
        margin: 10px 0 18px 0;
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }

    .badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 8pt;
        font-weight: 600;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-primary { background-color: #e0e7ff; color: #3730a3; }
    .badge-secure  { background-color: #dcfce7; color: #166534; }
    .badge-threat  { background-color: #fee2e2; color: #991b1b; }
    .badge-info    { background-color: #f1f5f9; color: #334155; }

    .callout {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #4f46e5;
        padding: 10px 14px;
        border-radius: 4px;
        margin: 12px 0;
        font-size: 9.5pt;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 8.5pt;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 9px;
        text-align: left;
    }

    th {
        background-color: #f1f5f9;
        font-weight: 600;
        color: #1e293b;
    }

    tr:nth-child(even) td {
        background-color: #f8fafc;
    }

    pre, code {
        font-family: "Cascadia Code", "Consolas", "Courier New", monospace;
    }

    code {
        background-color: #f1f5f9;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 8.5pt;
        color: #4338ca;
    }

    pre {
        background-color: #0f172a;
        color: #e2e8f0;
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 8pt;
        line-height: 1.4;
        overflow-x: auto;
        page-break-inside: avoid;
        margin: 10px 0;
    }

    .diagram-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 12px;
        margin: 14px 0;
        text-align: center;
        page-break-inside: avoid;
    }

    .diagram-flow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 6px;
        font-size: 8pt;
        font-weight: 600;
        margin: 8px 0;
    }

    .flow-node {
        flex: 1;
        padding: 8px 6px;
        border-radius: 5px;
        border: 1.5px solid #cbd5e1;
        background: #ffffff;
        color: #0f172a;
        text-align: center;
    }

    .flow-node.active {
        border-color: #4f46e5;
        background-color: #eef2ff;
        color: #3730a3;
    }

    .flow-node.gate {
        border-color: #b91c1c;
        background-color: #fef2f2;
        color: #991b1b;
    }

    .flow-arrow {
        color: #64748b;
        font-weight: bold;
    }

    .page-break {
        page-break-before: always;
    }

    .footer-note {
        font-size: 7.5pt;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        padding-top: 6px;
        margin-top: 20px;
    }
</style>
</head>
<body>

<!-- HEADER SECTION -->
<div>
    <h1>🛡️ Post-Quantum Cryptography (PQC) Secure-Code Reviewer Agent</h1>
    <div style="font-size: 11pt; color: #4338ca; font-weight: 600; margin-top: -4px;">
        Production DevSecOps & AI Systems Architectural Blueprint
    </div>
    
    <div class="badge-bar">
        <span class="badge badge-primary">Track 1: Agentic Cyber Defence</span>
        <span class="badge badge-secure">NIST FIPS 203 (ML-KEM)</span>
        <span class="badge badge-secure">NIST FIPS 204 (ML-DSA)</span>
        <span class="badge badge-threat">Zero Trust Gating</span>
        <span class="badge badge-info">SHA-256 Chained Auditing</span>
    </div>
</div>

<div class="callout">
    <strong>Executive Architectural Summary:</strong> The PQC Secure-Code Reviewer is an agentic cybersecurity static analysis platform designed to remediate the existential threat of <em>"Harvest Now, Decrypt Later" (HNDL)</em> attacks. It couples deterministic Abstract Syntax Tree (AST) scanning with transparent Chain-of-Thought (CoT) reasoning, enforces non-negotiable Human-in-the-Loop (HITL) approval gates, and guarantees cryptographic non-repudiation using recursive SHA-256 hash chaining.
</div>

<!-- SECTION 1 -->
<h2>1. Threat Modeling & Cryptographic Risk Analysis</h2>
<p>
Modern enterprise architectures rely fundamentally on public-key cryptography for digital signatures and key agreement. On a Cryptographically Relevant Quantum Computer (CRQC), Shor's algorithm solves discrete logarithms and integer factorizations in polynomial time $\mathcal{O}((\log N)^3)$, rendering classical asymmetric cryptography completely insecure.
</p>

<table>
    <thead>
        <tr>
            <th>Algorithm</th>
            <th>Category</th>
            <th>Quantum Attack Vector</th>
            <th>Impact</th>
            <th>NIST PQC Replacement</th>
            <th>Target Standard</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>RSA (2048/4096)</strong></td>
            <td>Key Exchange / Signature</td>
            <td>Shor's Algorithm</td>
            <td>Total Compromise (Polynomial Time)</td>
            <td>ML-KEM-768 / ML-DSA-65</td>
            <td>FIPS 203 / 204</td>
        </tr>
        <tr>
            <td><strong>ECDSA / ECDH</strong></td>
            <td>Signatures / Key Exchange</td>
            <td>Shor's Algorithm (ECDLP)</td>
            <td>Total Compromise (Forged Signatures)</td>
            <td>ML-DSA-65 / ML-KEM-768</td>
            <td>FIPS 204 / 203</td>
        </tr>
        <tr>
            <td><strong>DSA / DH</strong></td>
            <td>Key Exchange / Signature</td>
            <td>Shor's Algorithm</td>
            <td>Total Compromise</td>
            <td>ML-KEM-768 / ML-DSA-65</td>
            <td>FIPS 203 / 204</td>
        </tr>
        <tr>
            <td><strong>AES-128 / CBC</strong></td>
            <td>Symmetric Encryption</td>
            <td>Grover's Algorithm</td>
            <td>Effective security halved to 64-bit</td>
            <td>AES-256-GCM</td>
            <td>NIST SP 800-38D</td>
        </tr>
        <tr>
            <td><strong>MD5 / SHA-1</strong></td>
            <td>Hashing</td>
            <td>Classical Collisions + Grover</td>
            <td>Critically Broken</td>
            <td>SHA-3-256 / SHA-512</td>
            <td>FIPS 202</td>
        </tr>
    </tbody>
</table>

<!-- SECTION 2 -->
<h2>2. Four-Tier Production System Architecture</h2>
<p>The system is organized into four distinct architectural tiers ensuring strict separation of concerns, least privilege, and deterministic reproducibility:</p>

<div class="diagram-box">
    <div style="font-weight: 700; color: #1e293b; margin-bottom: 8px; font-size: 9pt;">ENTERPRISE ARCHITECTURE TIERS</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; text-align: left; font-size: 8pt;">
        <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px; border-radius: 4px;">
            <strong style="color: #4f46e5;">Tier 1: Shift-Left & Ingestion</strong>
            <ul style="margin: 4px 0 0 16px; padding: 0;">
                <li>Streamlit Web Dashboard (Port 8501)</li>
                <li>Headless DevSecOps CLI (<code>pqc_agent/cli.py</code>)</li>
                <li>Git Pre-Commit Hook (<code>.pre-commit-config.yaml</code>)</li>
            </ul>
        </div>
        <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px; border-radius: 4px;">
            <strong style="color: #4f46e5;">Tier 2: Agentic State Engine</strong>
            <ul style="margin: 4px 0 0 16px; padding: 0;">
                <li>LangGraph 5-Node State Machine</li>
                <li>State Checkpointer (<code>MemorySaver</code> / DB)</li>
                <li>Zero-Trust HITL Gate (<code>interrupt()</code>)</li>
            </ul>
        </div>
        <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px; border-radius: 4px;">
            <strong style="color: #4f46e5;">Tier 3: Analysis & Synthesis</strong>
            <ul style="margin: 4px 0 0 16px; padding: 0;">
                <li>Python AST Scanner & Java Syntax Trees</li>
                <li>AI Reasoning Core (Gemini 1.5 Pro + CoT)</li>
                <li>FIPS 203/204 Patch Synthesizer</li>
            </ul>
        </div>
        <div style="background: #ffffff; border: 1px solid #cbd5e1; padding: 8px; border-radius: 4px;">
            <strong style="color: #4f46e5;">Tier 4: Provenance & Governance</strong>
            <ul style="margin: 4px 0 0 16px; padding: 0;">
                <li>Enterprise Policy Engine (<code>pqc_config.yaml</code>)</li>
                <li>SHA-256 Recursive Tamper-Evident Hash Chain</li>
                <li>JSON & TXT Audit Outputs (<code>audit_outputs/</code>)</li>
            </ul>
        </div>
    </div>
</div>

<div class="page-break"></div>

<!-- SECTION 3 -->
<h2>3. LangGraph Five-Node Execution Pipeline</h2>
<p>
The core workflow is governed by a stateful LangGraph Directed Acyclic Graph (DAG) with explicit Human-in-the-Loop gating:
</p>

<div class="diagram-box">
    <div class="diagram-flow">
        <div class="flow-node active">
            <div>NODE 1</div>
            <div><strong>INGEST</strong></div>
            <div style="font-size: 7pt; color: #64748b;">File Validation & Genesis Hash</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node active">
            <div>NODE 2</div>
            <div><strong>SCAN</strong></div>
            <div style="font-size: 7pt; color: #64748b;">Deterministic AST Code Analysis</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node active">
            <div>NODE 3</div>
            <div><strong>INVESTIGATE</strong></div>
            <div style="font-size: 7pt; color: #64748b;">LLM CoT & Patch Synthesis</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node gate">
            <div>NODE 4</div>
            <div><strong>HITL GATE</strong></div>
            <div style="font-size: 7pt; color: #991b1b;">interrupt() Approval</div>
        </div>
        <div class="flow-arrow">➔</div>
        <div class="flow-node active">
            <div>NODE 5</div>
            <div><strong>FINALISE</strong></div>
            <div style="font-size: 7pt; color: #64748b;">Audit Sealing & Export</div>
        </div>
    </div>
</div>

<ol>
    <li><strong>INGEST</strong>: Evaluates source payloads, auto-detects dialect (Python/Java), logs file characteristics, and initializes state.</li>
    <li><strong>SCAN</strong>: Executes deterministic static analysis. Uses Python's native <code>ast.parse</code> to traverse import nodes and call sites, and regex pattern engines for Java source. Generates confidence ratings (0.95 for direct imports, 0.85 for call sites).</li>
    <li><strong>INVESTIGATE</strong>: Synthesizes NIST-standard migration patches. Generates Chain-of-Thought (CoT) reasoning outlining Shor's vs. Grover's threats, surfaces explicit uncertainty metrics, and includes fallback rule engines when offline.</li>
    <li><strong>HUMAN APPROVAL (HITL Gate)</strong>: Halts execution completely using LangGraph's <code>interrupt()</code> primitive. Resumes exclusively via <code>Command(resume={"decision": "approved", "feedback": "..."})</code>. The agent is mathematically incapable of committing code autonomously.</li>
    <li><strong>FINALISE</strong>: Seals approved patches, records reviewer authorization, calculates the terminal SHA-256 chain hash, and writes persistent audit logs.</li>
</ol>

<!-- SECTION 4 -->
<h2>4. DevSecOps CI/CD Integration & Shift-Left Gates</h2>
<p>
Security must shift left directly into developer workflows. The project provides multiple enforcement mechanisms:
</p>

<h3>4.1 Automated CLI Scanner Engine (<code>pqc_agent/cli.py</code>)</h3>
<p>Enables headless execution inside CI/CD runners, container builds, and pre-commit hooks:</p>
<pre>python -m pqc_agent.cli --target src/ --config pqc_config.yaml --fail-on CRITICAL --generate-patches --output-json audit_outputs/ci_audit.json</pre>
<ul>
    <li><strong>Exit Code 0</strong>: Compliance verification passed. Clean codebase.</li>
    <li><strong>Exit Code 1</strong>: Policy violation. Flagged cryptographic primitives $\ge$ threshold (e.g. CRITICAL RSA). <em>Fails the CI build</em>.</li>
    <li><strong>Exit Code 2</strong>: Invocation or syntax error.</li>
</ul>

<h3>4.2 Continuous Security Workflows (<code>.github/workflows/</code>)</h3>
<ul>
    <li><strong><code>ci.yml</code></strong>: Validates syntax, executes unit test suites (<code>test_pqc_agent.py</code>), and proves LangGraph interrupt & resume cycles (<code>test_graph_e2e.py</code>).</li>
    <li><strong><code>security-scan.yml</code></strong>: Executes SAST (Bandit), dependency audit (pip-audit), and the automated PQC security gate. Uploads the tamper-evident JSON audit trail as a workflow artifact.</li>
    <li><strong><code>.pre-commit-config.yaml</code></strong>: Local git hook preventing developers from committing deprecated crypto locally.</li>
</ul>

<!-- SECTION 5 -->
<h2>5. Cryptographic Tamper-Evident Hash Chaining</h2>
<p>
To satisfy strict compliance regimes (SOC 2 Type II, NIST SP 800-53), audit records are cryptographically linked using SHA-256:
</p>

<div class="callout" style="font-family: monospace; font-size: 8.5pt;">
    ChainHash<sub>0</sub> = SHA256("0" &times; 64)<br>
    ChainHash<sub>i</sub> = SHA256(CanonicalJSON(Entry<sub>i</sub>) || ChainHash<sub>i-1</sub>)
</div>

<p>
Every historical log entry forms a link in the chain. Any alteration to a finding, confidence score, reviewer feedback, or timestamp immediately breaks the terminal hash, exposing unauthorized tampering.
</p>

<!-- SECTION 6 -->
<h2>6. Regulatory Compliance & Standards Alignment</h2>
<table>
    <thead>
        <tr>
            <th>Regulatory Standard</th>
            <th>Control ID</th>
            <th>Requirement</th>
            <th>PQC Reviewer Implementation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>NIST SP 800-53 Rev. 5</strong></td>
            <td>SC-13</td>
            <td>Cryptographic Protection</td>
            <td>Detects sub-128-bit quantum primitives; migrates to FIPS 203/204.</td>
        </tr>
        <tr>
            <td><strong>NIST SP 800-53 Rev. 5</strong></td>
            <td>AU-10</td>
            <td>Non-Repudiation</td>
            <td>SHA-256 chained hashing proves provenance of all human approvals.</td>
        </tr>
        <tr>
            <td><strong>SOC 2 Type II</strong></td>
            <td>CC6.1 / CC6.6</td>
            <td>Logical Access & Boundary Defense</td>
            <td>Zero-Trust Human-in-the-Loop approval gate prior to code commit.</td>
        </tr>
        <tr>
            <td><strong>NSA CNSA 2.0</strong></td>
            <td>Timeline</td>
            <td>PQC Migration Mandates</td>
            <td>Facilitates transition to ML-KEM/ML-DSA ahead of 2030 deadlines.</td>
        </tr>
    </tbody>
</table>

<div class="footer-note">
    Document Reference: PQC-SEC-ARCH-2026-V1 &bull; Repository: https://github.com/natasyafrzan-hub/Quantum-Safe-Secure-Code-Reviewer &bull; Generated for Cybersecurity Hackathon Track 1
</div>

</body>
</html>
"""

# Write HTML file
with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML template at: {HTML_FILE}")

# Execute Edge headless print to PDF
cmd = [
    EDGE_EXE,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_FILE}",
    "--no-pdf-header-footer",
    f"file:///{HTML_FILE.resolve().as_posix()}"
]

print("Executing Microsoft Edge headless PDF engine...")
result = subprocess.run(cmd, capture_output=True, text=True)

if PDF_FILE.exists() and PDF_FILE.stat().st_size > 0:
    print(f"SUCCESS: PDF successfully generated at: {PDF_FILE} ({PDF_FILE.stat().st_size:,} bytes)")
    sys.exit(0)
else:
    print(f"ERROR: PDF generation failed. Stderr: {result.stderr}")
    sys.exit(1)
