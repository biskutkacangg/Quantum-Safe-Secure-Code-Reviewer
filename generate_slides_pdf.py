"""
generate_slides_pdf.py — Compiles a 16:9 landscape presentation slide deck
into a publication-quality PDF for presenting to peers, supervisors, and judges.
"""

import subprocess
import sys
from pathlib import Path

WORKSPACE = Path("c:/Users/User/hackathon-cybersecurity-agents")
HTML_FILE = WORKSPACE / "PQC_Presentation_Slides.html"
PDF_FILE = WORKSPACE / "PQC_Presentation_Slides.pdf"
DOWNLOADS_PDF = Path("C:/Users/User/Downloads/PQC_Presentation_Slides.pdf")
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PQC Secure-Code Reviewer — Presentation Slides</title>
<style>
    @page {
        size: 297mm 167.0625mm; /* Exact 16:9 widescreen presentation ratio */
        margin: 0;
    }

    * {
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        padding: 0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        background: #090d16;
        color: #f1f5f9;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }

    .slide {
        width: 297mm;
        height: 167mm;
        padding: 20mm 24mm;
        page-break-after: always;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        background: radial-gradient(circle at 80% 20%, #1e1b4b 0%, #0b0f19 55%, #05070d 100%);
        overflow: hidden;
    }

    /* Top slide header */
    .slide-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1.5px solid rgba(99, 102, 241, 0.35);
        padding-bottom: 8px;
        margin-bottom: 12px;
    }

    .slide-title-wrap h2 {
        font-size: 19pt;
        margin: 0;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .slide-title-wrap .slide-sub {
        font-size: 8.5pt;
        color: #a5b4fc;
        font-weight: 500;
        margin-top: 2px;
    }

    .slide-badge {
        font-size: 7.5pt;
        font-weight: 700;
        background: rgba(99, 102, 241, 0.2);
        color: #c7d2fe;
        border: 1px solid #6366f1;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Slide content area */
    .slide-body {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    /* Footer */
    .slide-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid rgba(148, 163, 184, 0.15);
        padding-top: 8px;
        font-size: 7.5pt;
        color: #64748b;
    }

    /* Grid Layouts */
    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }

    .grid-3 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 14px;
    }

    .grid-4 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        gap: 10px;
    }

    /* Cards */
    .card {
        background: rgba(19, 27, 46, 0.7);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 8px;
        padding: 12px 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
    }

    .card h3 {
        font-size: 10.5pt;
        margin: 0 0 6px 0;
        color: #38bdf8;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .card p, .card ul {
        margin: 0;
        font-size: 8.2pt;
        color: #cbd5e1;
        line-height: 1.45;
    }

    .card ul {
        padding-left: 16px;
    }

    .card li {
        margin-bottom: 4px;
    }

    /* Cover Slide */
    .cover-slide {
        text-align: center;
        justify-content: center;
        align-items: center;
        background: radial-gradient(circle at 50% 40%, #1e1b4b 0%, #0b0f19 70%, #030712 100%);
    }

    .cover-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.25);
        color: #a5b4fc;
        border: 1px solid #6366f1;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 9pt;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 16px;
        text-transform: uppercase;
    }

    .cover-title {
        font-size: 28pt;
        font-weight: 900;
        color: #ffffff;
        margin: 0 0 10px 0;
        letter-spacing: -0.6px;
        line-height: 1.15;
    }

    .cover-subtitle {
        font-size: 13pt;
        color: #94a3b8;
        max-width: 680px;
        margin: 0 auto 24px auto;
        line-height: 1.4;
    }

    .cover-meta {
        display: flex;
        gap: 16px;
        justify-content: center;
        font-size: 8.5pt;
        color: #64748b;
    }

    .meta-tag {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 12px;
        border-radius: 6px;
        color: #cbd5e1;
    }

    /* Highlight box */
    .highlight-stat {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin-bottom: 4px;
    }

    .stat-num {
        font-size: 20pt;
        font-weight: 800;
        color: #6366f1;
    }

    .stat-label {
        font-size: 9pt;
        font-weight: 600;
        color: #e2e8f0;
    }

    /* Tables */
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 7.8pt;
    }

    th, td {
        padding: 5.5px 8px;
        border: 1px solid rgba(148, 163, 184, 0.2);
        text-align: left;
    }

    th {
        background: rgba(30, 41, 59, 0.8);
        color: #93c5fd;
        font-weight: 700;
    }

    tr:nth-child(even) td {
        background: rgba(15, 23, 42, 0.4);
    }

    .mono {
        font-family: "Cascadia Code", "Consolas", monospace;
        color: #a5b4fc;
        font-size: 7.4pt;
    }

    .tag-vuln { color: #f87171; font-weight: bold; }
    .tag-safe { color: #4ade80; font-weight: bold; }

    /* Pipeline Flow in Slide */
    .flow-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
        margin: 12px 0;
    }

    .flow-step {
        flex: 1;
        background: #111827;
        border: 1.5px solid #4338ca;
        border-radius: 6px;
        padding: 10px 8px;
        text-align: center;
    }

    .flow-step.gate {
        border-color: #ef4444;
        background: rgba(239, 68, 68, 0.1);
    }

    .flow-step .num {
        font-size: 6.5pt;
        font-weight: 800;
        color: #818cf8;
        text-transform: uppercase;
    }

    .flow-step .name {
        font-size: 9.5pt;
        font-weight: 800;
        color: #ffffff;
        margin: 2px 0;
    }

    .flow-step .desc {
        font-size: 6.8pt;
        color: #94a3b8;
    }

    .flow-sep {
        color: #6366f1;
        font-size: 11pt;
        font-weight: 900;
    }
</style>
</head>
<body>

<!-- SLIDE 1: COVER -->
<div class="slide cover-slide">
    <div style="margin: auto;">
        <div class="cover-badge">Cybersecurity Hackathon • Track 1: Agentic Cyber Defence</div>
        <div class="cover-title">🛡️ Post-Quantum Cryptography (PQC)<br>Secure-Code Reviewer Agent</div>
        <div class="cover-subtitle">
            An Autonomous, State-Machine-Driven Security Agent for Detecting Quantum-Vulnerable Cryptography, Generating FIPS 203/204 Patches, and Enforcing Zero-Trust Human Governance.
        </div>
        <div class="cover-meta">
            <span class="meta-tag">👤 <strong>Role:</strong> DevSecOps & AI Systems Architect</span>
            <span class="meta-tag">🎯 <strong>Standards:</strong> NIST FIPS 203 (ML-KEM) & FIPS 204 (ML-DSA)</span>
            <span class="meta-tag">🔒 <strong>Safety:</strong> LangGraph interrupt() HITL Gate</span>
        </div>
    </div>
    <div class="slide-footer">
        <span>Repository: natasyafrzan-hub/Quantum-Safe-Secure-Code-Reviewer</span>
        <span>Slide 1 of 8</span>
    </div>
</div>

<!-- SLIDE 2: THE PROBLEM & THREAT MODEL -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>🚨 The Threat: "Harvest Now, Decrypt Later" (HNDL)</h2>
            <div class="slide-sub">Why classical encryption is already failing against nation-state adversaries</div>
        </div>
        <div class="slide-badge">Threat Modeling</div>
    </div>

    <div class="slide-body">
        <div class="grid-3">
            <div class="card" style="border-top: 3px solid #ef4444;">
                <h3>💥 Shor's Algorithm</h3>
                <p>
                    Runs on Cryptographically Relevant Quantum Computers (CRQCs) to factor large integers and compute discrete logs in <strong>polynomial time $\mathcal{O}(n^3)$</strong>.
                </p>
                <ul style="margin-top: 8px;">
                    <li><span class="tag-vuln">RSA (2048/4096)</span> ➔ Broken</li>
                    <li><span class="tag-vuln">ECDSA / ECDH</span> ➔ Broken</li>
                    <li><span class="tag-vuln">DSA / Diffie-Hellman</span> ➔ Broken</li>
                </ul>
            </div>

            <div class="card" style="border-top: 3px solid #f59e0b;">
                <h3>⚡ Grover's Algorithm</h3>
                <p>
                    Provides a quadratic speedup $\mathcal{O}(\sqrt{N})$ for searching unstructured spaces, <strong>halving effective symmetric key lengths</strong>.
                </p>
                <ul style="margin-top: 8px;">
                    <li><span class="tag-vuln">AES-128</span> drops to 64-bit security (Unsafe)</li>
                    <li><span class="tag-safe">AES-256</span> retains 128-bit quantum security</li>
                    <li><span class="tag-vuln">MD5 / SHA-1</span> broken classically & quantum</li>
                </ul>
            </div>

            <div class="card" style="border-top: 3px solid #6366f1;">
                <h3>🏢 Enterprise Reality</h3>
                <p>
                    Organizations have millions of lines of legacy code with hardcoded cryptographic calls.
                </p>
                <ul style="margin-top: 8px;">
                    <li>Adversaries are <strong>stockpiling encrypted data today</strong> to decrypt retroactively.</li>
                    <li>Manual code auditing takes months and lacks provable audit trails.</li>
                    <li>NIST released FIPS 203/204 in August 2024—codebases must migrate now.</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework</span>
        <span>Slide 2 of 8</span>
    </div>
</div>

<!-- SLIDE 3: COMPLETE REPO & FILE MAP -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>🗺️ Complete Repository Anatomy & File Guide</h2>
            <div class="slide-sub">Modular structure: Presentation, Agent Core, Testbench, and DevSecOps</div>
        </div>
        <div class="slide-badge">File Structure</div>
    </div>

    <div class="slide-body">
        <div class="grid-4">
            <div class="card">
                <h3>🖥️ Presentation</h3>
                <ul>
                    <li><span class="mono">app.py</span>: Streamlit dark dashboard (Port 8501) with side-by-side diffs.</li>
                    <li><span class="mono">.streamlit/config.toml</span>: Theme styling & server config.</li>
                </ul>
            </div>

            <div class="card">
                <h3>🧠 Agent Engine</h3>
                <ul>
                    <li><span class="mono">pqc_agent/state.py</span>: AgentState TypedDict & Pydantic models.</li>
                    <li><span class="mono">pqc_agent/tools.py</span>: AST scanner & FIPS patch generator.</li>
                    <li><span class="mono">pqc_agent/graph.py</span>: 5-node LangGraph state machine.</li>
                    <li><span class="mono">pqc_agent/audit.py</span>: SHA-256 recursive hash logger.</li>
                </ul>
            </div>

            <div class="card">
                <h3>⚙️ DevSecOps & CI</h3>
                <ul>
                    <li><span class="mono">pqc_agent/cli.py</span>: Headless CLI scanner for CI/CD.</li>
                    <li><span class="mono">pqc_config.yaml</span>: Policy rules & target algorithms.</li>
                    <li><span class="mono">.github/workflows/</span>: CI tests & Bandit SAST scans.</li>
                    <li><span class="mono">Dockerfile</span>: Hardened non-root container.</li>
                </ul>
            </div>

            <div class="card">
                <h3>🧪 Testbench</h3>
                <ul>
                    <li><span class="mono">sample_files/</span>: Vulnerable Python & Java crypto samples.</li>
                    <li><span class="mono">test_pqc_agent.py</span>: Unit tests for all scanner tools.</li>
                    <li><span class="mono">test_graph_e2e.py</span>: E2E HITL interrupt & resume test.</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework</span>
        <span>Slide 3 of 8</span>
    </div>
</div>

<!-- SLIDE 4: THE 5-NODE STATE MACHINE & HITL GATE -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>🧠 The LangGraph 5-Node State Machine & HITL Gate</h2>
            <div class="slide-sub">Zero-Trust Safety: AI can propose code, but cannot touch production without human sign-off</div>
        </div>
        <div class="slide-badge">Agentic AI Architecture</div>
    </div>

    <div class="slide-body">
        <div class="flow-bar">
            <div class="flow-step">
                <div class="num">Node 1</div>
                <div class="name">INGEST</div>
                <div class="desc">Validation & Genesis SHA-256</div>
            </div>
            <div class="flow-sep">➔</div>
            <div class="flow-step">
                <div class="num">Node 2</div>
                <div class="name">SCAN</div>
                <div class="desc">AST Parser & Confidence Metric</div>
            </div>
            <div class="flow-sep">➔</div>
            <div class="flow-step">
                <div class="num">Node 3</div>
                <div class="name">INVESTIGATE</div>
                <div class="desc">LLM CoT & FIPS 203/204 Patches</div>
            </div>
            <div class="flow-sep">➔</div>
            <div class="flow-step gate">
                <div class="num" style="color:#ef4444;">Node 4 (Pause)</div>
                <div class="name" style="color:#f87171;">HITL GATE</div>
                <div class="desc">interrupt() Approval Barrier</div>
            </div>
            <div class="flow-sep">➔</div>
            <div class="flow-step">
                <div class="num">Node 5</div>
                <div class="name">FINALISE</div>
                <div class="desc">Sealed Tamper-Evident Log</div>
            </div>
        </div>

        <div class="grid-2" style="margin-top: 10px;">
            <div class="card">
                <h3>🔍 Explainable AI & Uncertainty (XAI)</h3>
                <p>
                    Rather than opaque black-box responses, the agent produces step-by-step Chain-of-Thought (CoT) reasoning. It explicitly isolates test fixtures from security-critical paths and states confidence metrics (0.95 for direct imports, 0.85 for call sites).
                </p>
            </div>
            <div class="card">
                <h3>🛑 Non-Negotiable Human-in-the-Loop Barrier</h3>
                <p>
                    Built with LangGraph's native <span class="mono">interrupt()</span> primitive. Execution freezes completely at Node 4 until a human reviewer reviews the side-by-side diff and clicks <strong>Approve</strong> or <strong>Reject</strong> via <span class="mono">Command(resume=...)</span>.
                </p>
            </div>
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework</span>
        <span>Slide 4 of 8</span>
    </div>
</div>

<!-- SLIDE 5: NIST PQC MIGRATION MATRIX -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>🔄 NIST Post-Quantum Cryptography Migration Matrix</h2>
            <div class="slide-sub">Mapping legacy algorithms to the new NIST FIPS standards finalized in August 2024</div>
        </div>
        <div class="slide-badge">Cryptographic Standards</div>
    </div>

    <div class="slide-body">
        <table>
            <thead>
                <tr>
                    <th>Legacy Algorithm</th>
                    <th>Category</th>
                    <th>Vulnerability Reason</th>
                    <th>Target NIST Replacement</th>
                    <th>Standard Reference</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="tag-vuln">RSA-2048 / 4096</span></td>
                    <td>Key Encapsulation / Signing</td>
                    <td>Shor's Algorithm (Integer Factorization)</td>
                    <td><span class="tag-safe">ML-KEM-768</span> / <span class="tag-safe">ML-DSA-65</span></td>
                    <td>FIPS 203 / FIPS 204</td>
                </tr>
                <tr>
                    <td><span class="tag-vuln">ECDH / DH</span></td>
                    <td>Key Exchange</td>
                    <td>Shor's Algorithm (Discrete Logarithm / ECDLP)</td>
                    <td><span class="tag-safe">ML-KEM-768</span> (Module Lattice KEM)</td>
                    <td>FIPS 203</td>
                </tr>
                <tr>
                    <td><span class="tag-vuln">ECDSA / DSA / EdDSA</span></td>
                    <td>Digital Signature</td>
                    <td>Shor's Algorithm (Elliptic Curve Discrete Log)</td>
                    <td><span class="tag-safe">ML-DSA-65</span> (Module Lattice Signature)</td>
                    <td>FIPS 204</td>
                </tr>
                <tr>
                    <td><span class="tag-vuln">DES / 3DES / Blowfish</span></td>
                    <td>Symmetric Cipher</td>
                    <td>Broken Classically & Grover's Speedup</td>
                    <td><span class="tag-safe">AES-256-GCM</span> (Authenticated Encryption)</td>
                    <td>NIST SP 800-38D</td>
                </tr>
                <tr>
                    <td><span class="tag-vuln">AES-128 (CBC/ECB)</span></td>
                    <td>Symmetric Cipher</td>
                    <td>Grover's reduces key strength to 64 bits</td>
                    <td><span class="tag-safe">AES-256-GCM</span> (Maintains 128-bit quantum security)</td>
                    <td>NIST SP 800-38D</td>
                </tr>
                <tr>
                    <td><span class="tag-vuln">MD5 / SHA-1</span></td>
                    <td>Hashing Function</td>
                    <td>Known Classical Collisions + Grover</td>
                    <td><span class="tag-safe">SHA-3-256 / SHA-512</span> (Keccak sponge)</td>
                    <td>FIPS 202</td>
                </tr>
            </tbody>
        </table>
        <div style="font-size: 7.5pt; color: #94a3b8; margin-top: 6px;">
            *Also supports hybrid classical/quantum pairings (e.g., <span class="mono">X25519_ML-KEM-768</span>) for phased backwards-compatible infrastructure transitions.
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework</span>
        <span>Slide 5 of 8</span>
    </div>
</div>

<!-- SLIDE 6: DUAL EXECUTION MODES -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>⚡ Dual Operation Modes: Web Dashboard &amp; DevSecOps CLI</h2>
            <div class="slide-sub">Built for both human security architects and automated continuous integration pipelines</div>
        </div>
        <div class="slide-badge">System Implementation</div>
    </div>

    <div class="slide-body">
        <div class="grid-2">
            <div class="card" style="border-top: 3px solid #6366f1;">
                <h3>🖥️ Mode A: Interactive Web UI (`app.py`)</h3>
                <p style="margin-bottom: 8px;">Designed for cryptographers and security auditors exploring repositories:</p>
                <ul>
                    <li>Live file upload or sample selector with line-numbered preview.</li>
                    <li>Visual cards detailing line numbers, severity, and Shor/Grover risk.</li>
                    <li>Side-by-side syntax diff viewer highlighting legacy code vs PQC patch.</li>
                    <li>Approve / Reject decision buttons unblocking the state machine.</li>
                    <li>One-click download of JSON &amp; TXT audit trails with SHA-256 hashes.</li>
                </ul>
            </div>

            <div class="card" style="border-top: 3px solid #10b981;">
                <h3>⚡ Mode B: Headless CLI Engine (`pqc_agent/cli.py`)</h3>
                <p style="margin-bottom: 8px;">Designed for automated CI/CD runners and pre-commit hooks:</p>
                <ul>
                    <li>Reads policy thresholds from <span class="mono">pqc_config.yaml</span>.</li>
                    <li>Scans repositories recursively without requiring UI or LLM tokens.</li>
                    <li>Enforces build gates via standardized exit codes:
                        <br>&bull; <span class="mono">Exit 0</span>: Clean code (Build passes).
                        <br>&bull; <span class="mono">Exit 1</span>: Policy violation &ge; threshold (Build fails).
                    </li>
                    <li>Auto-generates FIPS 203/204 patches via <span class="mono">--generate-patches</span>.</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework</span>
        <span>Slide 6 of 8</span>
    </div>
</div>

<!-- SLIDE 7: TAMPER-EVIDENT AUDIT & COMPLIANCE -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>🔒 Cryptographic Tamper-Evident Auditing (SHA-256)</h2>
            <div class="slide-sub">Blockchain-style hash chaining guarantees non-repudiation for SOC 2 and NIST SP 800-53</div>
        </div>
        <div class="slide-badge">Governance & Compliance</div>
    </div>

    <div class="slide-body">
        <div class="grid-2">
            <div class="card">
                <h3>⛓️ Recursive Hash Chaining Formula</h3>
                <p style="margin-bottom: 8px;">Every audit entry cryptographically seals the previous state:</p>
                <div style="background: #0b0f19; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 7.6pt; color: #38bdf8; margin-bottom: 8px;">
                    Hash_0 = SHA256("0" * 64) [Genesis]<br>
                    Hash_i = SHA256(CanonicalJSON(Entry_i) + Hash_{i-1})
                </div>
                <p>
                    If an insider or adversary tampers with any past finding, severity rating, or approval timestamp, the computed terminal hash immediately breaks.
                </p>
            </div>

            <div class="card">
                <h3>📜 Regulatory Compliance Mapping</h3>
                <ul>
                    <li><strong>NIST SP 800-53 Rev. 5 (SC-13):</strong> Cryptographic protection against quantum attacks via migration to FIPS 203/204.</li>
                    <li><strong>NIST SP 800-53 Rev. 5 (AU-10):</strong> Non-repudiation enforced via the SHA-256 chain hash.</li>
                    <li><strong>SOC 2 Type II (CC6.1 / CC6.6):</strong> Strict Human-in-the-Loop authorization before code modification.</li>
                    <li><strong>NSA CNSA 2.0:</strong> Prepares enterprise software for national post-quantum mandates.</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework</span>
        <span>Slide 7 of 8</span>
    </div>
</div>

<!-- SLIDE 8: QUICK COMMANDS & SUMMARY -->
<div class="slide">
    <div class="slide-header">
        <div class="slide-title-wrap">
            <h2>🚀 Live Demonstration Cheatsheet & Summary</h2>
            <div class="slide-sub">Everything you need to run, test, and explain the project to friends and judges</div>
        </div>
        <div class="slide-badge">Demo Guide</div>
    </div>

    <div class="slide-body">
        <div class="grid-2">
            <div class="card">
                <h3>⚡ Essential Commands</h3>
                <table>
                    <tr>
                        <td><strong>Web UI</strong></td>
                        <td><span class="mono">streamlit run app.py</span></td>
                    </tr>
                    <tr>
                        <td><strong>CLI Scan</strong></td>
                        <td><span class="mono">python -m pqc_agent.cli --target sample_files/</span></td>
                    </tr>
                    <tr>
                        <td><strong>Unit Tests</strong></td>
                        <td><span class="mono">python test_pqc_agent.py</span></td>
                    </tr>
                    <tr>
                        <td><strong>E2E HITL Test</strong></td>
                        <td><span class="mono">python test_graph_e2e.py</span></td>
                    </tr>
                    <tr>
                        <td><strong>Docker Compose</strong></td>
                        <td><span class="mono">docker compose up -d --build</span></td>
                    </tr>
                </table>
            </div>

            <div class="card">
                <h3>🏆 Key Pitch Takeaways for Friends</h3>
                <ul>
                    <li><strong>Not just a linter:</strong> It reasons with an LLM, explains Shor vs Grover, and writes FIPS 203/204 code.</li>
                    <li><strong>Zero-Trust safety:</strong> The AI is mathematically blocked from auto-committing via LangGraph's <span class="mono">interrupt()</span>.</li>
                    <li><strong>Full Production DevSecOps:</strong> Shipped with Docker, GitHub Actions CI/CD, pre-commit hooks, and tamper-evident SHA-256 auditing.</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="slide-footer">
        <span>Post-Quantum Cryptography Migration Framework • Production Ready</span>
        <span>Slide 8 of 8</span>
    </div>
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

print("Compiling 16:9 widescreen presentation slide deck PDF via Edge headless...")
result = subprocess.run(cmd, capture_output=True, text=True)

if PDF_FILE.exists() and PDF_FILE.stat().st_size > 0:
    print(f"SUCCESS: Slide deck PDF created at: {PDF_FILE} ({PDF_FILE.stat().st_size:,} bytes)")
    DOWNLOADS_PDF.write_bytes(PDF_FILE.read_bytes())
    print(f"Copied to Downloads: {DOWNLOADS_PDF}")
    sys.exit(0)
else:
    print(f"ERROR: {result.stderr}")
    sys.exit(1)
