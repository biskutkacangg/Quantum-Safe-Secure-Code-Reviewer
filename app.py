# ============================================================
# app.py — Streamlit Dashboard for PQC Secure-Code Reviewer Agent
# ============================================================
"""
Premium Streamlit frontend that provides:
  - Source code file upload (Python / Java)
  - Real-time agent workflow execution with phase tracking
  - Chain of Thought transparency panel
  - Side-by-side code diff (Legacy vs PQC)
  - Interactive Approve / Reject HITL gate
  - Downloadable audit trail (JSON + TXT)
  - Explicit limitations & false-positive disclosures

Run:  streamlit run app.py
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

try:
    from pqc_agent.audit import compute_cia_summary, generate_audit_json, generate_audit_txt
except ImportError:
    from pqc_agent.audit import generate_audit_json, generate_audit_txt

    def compute_cia_summary(findings: list[dict]) -> dict[str, int]:
        """Fallback CIA summary calculator."""
        summary = {"Confidentiality": 0, "Integrity": 0, "Availability": 0}
        for f in findings:
            for p in f.get("cia_triad", []):
                if p in summary:
                    summary[p] += 1
        return summary

from pqc_agent.graph import build_graph
from pqc_agent.state import AgentState
from pqc_agent.tools import LEGACY_CRYPTO_DB


# ════════════════════════════════════════════════════════════════
# ░░░ PAGE CONFIG ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="PQC Secure-Code Reviewer Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════
# ░░░ CUSTOM CSS — Premium Dark Theme ░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* ── Import Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a1f2e;
        --bg-card-hover: #232940;
        --bg-glass: rgba(26, 31, 46, 0.85);
        --border-subtle: rgba(99, 102, 241, 0.15);
        --border-glow: rgba(99, 102, 241, 0.4);
        --text-primary: #e2e8f0;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-indigo: #6366f1;
        --accent-violet: #8b5cf6;
        --accent-cyan: #22d3ee;
        --accent-emerald: #10b981;
        --accent-amber: #f59e0b;
        --accent-rose: #f43f5e;
        --gradient-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        --gradient-danger: linear-gradient(135deg, #f43f5e 0%, #e11d48 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --shadow-glow: 0 0 30px rgba(99, 102, 241, 0.15);
        --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.3);
    }

    /* ── Global ── */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── Header Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 40%, #312e81 100%);
        border: 1px solid var(--border-subtle);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-glow);
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-banner h1 {
        font-size: 2rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .hero-banner p {
        color: var(--text-secondary);
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.6;
        max-width: 700px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--accent-indigo);
        margin-bottom: 1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── Phase Tracker ── */
    .phase-tracker {
        display: flex;
        gap: 0;
        margin: 1.5rem 0;
        padding: 0;
    }
    .phase-step {
        flex: 1;
        text-align: center;
        padding: 12px 8px;
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        font-size: 0.78rem;
        font-weight: 500;
        color: var(--text-muted);
        position: relative;
        transition: all 0.3s ease;
    }
    .phase-step:first-child { border-radius: 10px 0 0 10px; }
    .phase-step:last-child { border-radius: 0 10px 10px 0; }
    .phase-step.active {
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.15));
        border-color: var(--accent-indigo);
        color: var(--accent-indigo);
        font-weight: 700;
        box-shadow: 0 0 20px rgba(99,102,241,0.15);
    }
    .phase-step.completed {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
        color: var(--accent-emerald);
    }

    /* ── Cards ── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-card);
    }
    .metric-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow);
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    .metric-card .metric-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }
    .card-critical .metric-value { color: var(--accent-rose); }
    .card-high .metric-value { color: var(--accent-amber); }
    .card-findings .metric-value { color: var(--accent-cyan); }
    .card-patches .metric-value { color: var(--accent-emerald); }

    /* ── Finding Card ── */
    .finding-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-left: 4px solid var(--accent-rose);
        border-radius: 0 12px 12px 0;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .finding-card:hover {
        border-left-color: var(--accent-indigo);
        background: var(--bg-card-hover);
    }
    .finding-card.sev-critical { border-left-color: var(--accent-rose); }
    .finding-card.sev-high { border-left-color: var(--accent-amber); }
    .finding-card.sev-medium { border-left-color: #3b82f6; }
    .finding-card.sev-low { border-left-color: var(--accent-emerald); }

    .severity-badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .severity-badge.critical {
        background: rgba(244, 63, 94, 0.15);
        color: var(--accent-rose);
        border: 1px solid rgba(244, 63, 94, 0.3);
    }
    .severity-badge.high {
        background: rgba(245, 158, 11, 0.15);
        color: var(--accent-amber);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .severity-badge.medium {
        background: rgba(59, 130, 246, 0.15);
        color: #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    /* ── CIA Triad Badges & Cards ── */
    .cia-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .cia-badge.confidentiality {
        background: rgba(139, 92, 246, 0.18);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }
    .cia-badge.integrity {
        background: rgba(34, 211, 238, 0.18);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
    }
    .cia-badge.availability {
        background: rgba(245, 158, 11, 0.18);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    .cia-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-card);
    }
    .cia-card:hover {
        border-color: var(--border-glow);
        transform: translateY(-2px);
    }
    .cia-card.pillar-c { border-top: 3px solid #c084fc; }
    .cia-card.pillar-i { border-top: 3px solid #38bdf8; }
    .cia-card.pillar-a { border-top: 3px solid #fbbf24; }
    .cia-stat-num {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1;
        margin-top: 0.5rem;
        margin-bottom: 0.4rem;
    }

    /* ── Code Diff ── */
    .diff-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    .diff-panel {
        background: var(--bg-secondary);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        overflow: hidden;
    }
    .diff-header {
        padding: 10px 16px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .diff-header.legacy {
        background: rgba(244, 63, 94, 0.1);
        color: var(--accent-rose);
        border-bottom: 1px solid rgba(244, 63, 94, 0.2);
    }
    .diff-header.pqc {
        background: rgba(16, 185, 129, 0.1);
        color: var(--accent-emerald);
        border-bottom: 1px solid rgba(16, 185, 129, 0.2);
    }
    .diff-content {
        padding: 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        line-height: 1.7;
        overflow-x: auto;
        white-space: pre-wrap;
        color: var(--text-primary);
    }

    /* ── Approval Buttons ── */
    .approval-container {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }

    /* ── Limitations Box ── */
    .limitations-box {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
    }
    .limitations-box h4 {
        color: var(--accent-amber);
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .limitations-box li {
        color: var(--text-secondary);
        font-size: 0.85rem;
        line-height: 1.7;
        margin-bottom: 0.3rem;
    }

    /* ── Audit Timeline ── */
    .audit-entry {
        display: flex;
        gap: 1rem;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(99,102,241,0.08);
    }
    .audit-timestamp {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--text-muted);
        white-space: nowrap;
        min-width: 180px;
    }
    .audit-action {
        font-weight: 600;
        font-size: 0.82rem;
        color: var(--accent-indigo);
        min-width: 180px;
    }
    .audit-detail {
        font-size: 0.82rem;
        color: var(--text-secondary);
        flex: 1;
    }

    /* ── Animations ── */
    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 10px rgba(99,102,241,0.2); }
        50% { box-shadow: 0 0 25px rgba(99,102,241,0.4); }
    }
    .pulse-active { animation: pulse-glow 2s ease-in-out infinite; }

    @keyframes slide-in {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in { animation: slide-in 0.4s ease-out; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%);
    }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# ░░░ SESSION STATE INIT ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def _init_session():
    """Initialise Streamlit session state variables."""
    defaults = {
        "thread_id": str(uuid.uuid4()),
        "checkpointer": MemorySaver(),
        "graph": None,
        "phase": "upload",        # upload → scanning → review → approved/rejected
        "findings": [],
        "patches": [],
        "chain_of_thought": "",
        "uncertainty_statement": "",
        "risk_assessment": "",
        "scan_summary": "",
        "audit_trail": [],
        "source_code": "",
        "file_name": "",
        "language": "",
        "human_feedback": "",
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

    if st.session_state["graph"] is None:
        st.session_state["graph"] = build_graph(
            checkpointer=st.session_state["checkpointer"]
        )


_init_session()


# ════════════════════════════════════════════════════════════════
# ░░░ HELPER RENDERERS ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def render_phase_tracker(current_phase: str):
    """Render the workflow phase tracker bar."""
    phases = [
        ("📤 Upload", "upload"),
        ("🔍 Scanning", "scanning"),
        ("🧠 Investigation", "investigating"),
        ("👤 Review", "review"),
        ("✅ Complete", "complete"),
    ]
    phase_order = [p[1] for p in phases]
    current_idx = phase_order.index(current_phase) if current_phase in phase_order else 0

    html_parts = []
    for i, (label, phase_id) in enumerate(phases):
        if i < current_idx:
            css_class = "completed"
        elif i == current_idx:
            css_class = "active pulse-active"
        else:
            css_class = ""
        html_parts.append(
            f'<div class="phase-step {css_class}">{label}</div>'
        )

    st.markdown(
        f'<div class="phase-tracker">{"".join(html_parts)}</div>',
        unsafe_allow_html=True,
    )


def render_metrics(findings: list[dict], patches: list[dict]):
    """Render the dashboard metric cards and CIA summary."""
    critical = sum(1 for f in findings if f.get("severity") == "CRITICAL")
    high = sum(1 for f in findings if f.get("severity") == "HIGH")

    cols = st.columns(4)
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card card-findings animate-in">
            <div class="metric-value">{len(findings)}</div>
            <div class="metric-label">Total Findings</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card card-critical animate-in">
            <div class="metric-value">{critical}</div>
            <div class="metric-label">Critical</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="metric-card card-high animate-in">
            <div class="metric-value">{high}</div>
            <div class="metric-label">High</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[3]:
        st.markdown(f"""
        <div class="metric-card card-patches animate-in">
            <div class="metric-value">{len(patches)}</div>
            <div class="metric-label">Patches Generated</div>
        </div>
        """, unsafe_allow_html=True)

    # CIA Impact Quick Bar
    if findings:
        cia_summary = compute_cia_summary(findings)
        c_num = cia_summary.get("Confidentiality", 0)
        i_num = cia_summary.get("Integrity", 0)
        a_num = cia_summary.get("Availability", 0)
        st.markdown(f"""
        <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; background:rgba(26,31,46,0.7); border:1px solid var(--border-subtle); border-radius:10px; padding:10px 16px; margin-top:12px;">
            <span style="font-size:0.78rem; font-weight:700; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.05em;">🛡️ CIA Triad Impact:</span>
            <span class="cia-badge confidentiality">Confidentiality: {c_num}</span>
            <span class="cia-badge integrity">Integrity: {i_num}</span>
            <span class="cia-badge availability">Availability: {a_num}</span>
            <span style="font-size:0.75rem; color:var(--text-muted); margin-left:auto;">Target: NIST FIPS 203 / 204 Zero-Trust</span>
        </div>
        """, unsafe_allow_html=True)


def render_finding_card(finding: dict, index: int):
    """Render a single finding card with CIA Triad badges."""
    sev = finding.get("severity", "INFO").lower()
    algo = finding.get("algorithm_detected", "Unknown")
    line = finding.get("line_number", "?")
    snippet = finding.get("code_snippet", "")
    confidence = finding.get("confidence", 0)
    rationale = finding.get("rationale", "")
    quantum = finding.get("quantum_threat_level", "")
    cia_triad = finding.get("cia_triad", ["Confidentiality"])

    cia_badges = " ".join([
        f'<span class="cia-badge {p.lower()}">{p}</span>'
        for p in cia_triad
    ])

    st.markdown(f"""
    <div class="finding-card sev-{sev} animate-in">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-weight:700; font-size:1rem; color:var(--text-primary);">
                #{index+1} — {algo}
            </span>
            <div style="display:flex; align-items:center; gap:8px;">
                {cia_badges}
                <span class="severity-badge {sev}">{sev.upper()}</span>
            </div>
        </div>
        <div style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:6px;">
            📍 Line {line} &nbsp;|&nbsp; Confidence: {confidence:.0%}
        </div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.78rem; background:rgba(0,0,0,0.3); padding:8px 12px; border-radius:6px; margin:8px 0; color:#e2e8f0;">
            {snippet}
        </div>
        <div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.6;">
            <strong style="color:var(--accent-indigo);">Rationale:</strong> {rationale}
        </div>
        <div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.6; margin-top:4px;">
            <strong style="color:var(--accent-cyan);">⚛️ Quantum Threat:</strong> {quantum}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_cia_analysis(findings: list[dict], patches: list[dict]):
    """Render the comprehensive CIA Triad Impact Analysis panel."""
    c_findings = [f for f in findings if "Confidentiality" in f.get("cia_triad", [])]
    i_findings = [f for f in findings if "Integrity" in f.get("cia_triad", [])]
    a_findings = [f for f in findings if "Availability" in f.get("cia_triad", [])]

    pqc_algos = [p.get("pqc_algorithm", "") for p in patches]
    has_pqc_bloat = any("ML-KEM" in a or "ML-DSA" in a or "Dilithium" in a or "Kyber" in a for a in pqc_algos)

    st.markdown("""
    <div style="background:linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05)); border:1px solid var(--border-subtle); border-radius:12px; padding:1.25rem 1.5rem; margin-bottom:1.5rem;">
        <h4 style="margin:0 0 8px 0; color:var(--accent-indigo);">🛡️ The CIA Triad in Post-Quantum Cryptography</h4>
        <p style="font-size:0.86rem; color:var(--text-secondary); margin:0; line-height:1.6;">
            Evaluating post-quantum cryptographic resilience across all three foundational pillars of cybersecurity:
            <strong>Confidentiality</strong> (countering Harvest Now, Decrypt Later attacks), 
            <strong>Integrity</strong> (preventing quantum signature forgery and hash collision attacks), and 
            <strong>Availability</strong> (mitigating PQC network bloat, MTU packet fragmentation, and handshake latency spikes).
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_c, col_i, col_a = st.columns(3)

    with col_c:
        st.markdown(f"""
        <div class="cia-card pillar-c animate-in">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cia-badge confidentiality">Confidentiality</span>
                <span style="font-size:0.8rem; color:var(--text-muted);">Shor's & Grover's</span>
            </div>
            <div class="cia-stat-num" style="color:#c084fc;">{len(c_findings)}</div>
            <div style="font-size:0.85rem; font-weight:700; color:var(--text-primary); margin-bottom:6px;">
                Harvest Now, Decrypt Later (HNDL)
            </div>
            <div style="font-size:0.8rem; color:var(--text-secondary); line-height:1.5; margin-bottom:12px;">
                Adversaries passively record encrypted ciphertext today to decrypt once cryptographically relevant quantum computers (CRQC) emerge.
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.06); padding-top:10px; font-size:0.78rem;">
                <strong style="color:var(--accent-emerald);">🎯 NIST Migration:</strong><br/>
                FIPS 203 ML-KEM-768/1024, Hybrid X25519_ML-KEM-768, AES-256
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_i:
        st.markdown(f"""
        <div class="cia-card pillar-i animate-in">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cia-badge integrity">Integrity</span>
                <span style="font-size:0.8rem; color:var(--text-muted);">Discrete Log & Hashes</span>
            </div>
            <div class="cia-stat-num" style="color:#38bdf8;">{len(i_findings)}</div>
            <div style="font-size:0.85rem; font-weight:700; color:var(--text-primary); margin-bottom:6px;">
                Digital Signature Forgery
            </div>
            <div style="font-size:0.8rem; color:var(--text-secondary); line-height:1.5; margin-bottom:12px;">
                Shor's algorithm breaks discrete logarithms in ECDSA, Ed25519, and RSA signing, allowing identity theft, authentication bypass, and malicious firmware injection.
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.06); padding-top:10px; font-size:0.78rem;">
                <strong style="color:var(--accent-emerald);">🎯 NIST Migration:</strong><br/>
                FIPS 204 ML-DSA-65/87, FIPS 205 SLH-DSA, SHA-384 / SHA-512
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_a:
        avail_count = len(a_findings) if a_findings else (len(patches) if has_pqc_bloat else 0)
        st.markdown(f"""
        <div class="cia-card pillar-a animate-in">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="cia-badge availability">Availability</span>
                <span style="font-size:0.8rem; color:var(--text-muted);">Packet Bloat & MTU</span>
            </div>
            <div class="cia-stat-num" style="color:#fbbf24;">{avail_count}</div>
            <div style="font-size:0.85rem; font-weight:700; color:var(--text-primary); margin-bottom:6px;">
                PQC MTU & Latency Overhead
            </div>
            <div style="font-size:0.8rem; color:var(--text-secondary); line-height:1.5; margin-bottom:12px;">
                ML-KEM keys (~1.2 KB) and ML-DSA signatures (~3.3 KB) exceed standard Ethernet 1500-byte MTUs, causing TCP fragmentation and handshake timeouts.
            </div>
            <div style="border-top:1px solid rgba(255,255,255,0.06); padding-top:10px; font-size:0.78rem;">
                <strong style="color:var(--accent-emerald);">🎯 Resilience Plan:</strong><br/>
                DigiCert TLS 1.3 PQC hybrid negotiation, TCP Jumbo Frames, crypto agility
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📊 CIA Impact Matrix")
    if findings:
        matrix_rows = []
        for f in findings:
            pillars = f.get("cia_triad", ["Confidentiality"])
            algo_key = f.get("algorithm_detected", "")
            db_info = LEGACY_CRYPTO_DB.get(algo_key, {})
            c_flag = "🟣 Vulnerable (HNDL)" if "Confidentiality" in pillars else "—"
            i_flag = "🔵 Vulnerable (Forgery)" if "Integrity" in pillars else "—"
            a_flag = "🟡 Key Bloat / MTU" if "Availability" in pillars or db_info.get("category") in ("kem", "signature", "asymmetric") else "—"
            matrix_rows.append({
                "Algorithm": algo_key,
                "Line": f.get("line_number", "?"),
                "Severity": f.get("severity", "HIGH"),
                "Confidentiality": c_flag,
                "Integrity": i_flag,
                "Availability Risk": a_flag,
                "NIST Recommendation": db_info.get("recommended_pqc", "NIST PQC Standard"),
                "FIPS Standard": db_info.get("fips_standard", "FIPS 203/204")
            })
        st.dataframe(matrix_rows, use_container_width=True)
    else:
        st.info("No findings detected to populate the CIA matrix.")


def render_diff(patch: dict, index: int):
    """Render a side-by-side code diff for a patch."""
    original = patch.get("original_code", "").replace("<", "&lt;").replace(">", "&gt;")
    patched = patch.get("patched_code", "").replace("<", "&lt;").replace(">", "&gt;")
    pqc_algo = patch.get("pqc_algorithm", "")
    notes = patch.get("migration_notes", "")

    st.markdown(f"""
    <div class="animate-in" style="margin-bottom:1.5rem;">
        <div style="font-weight:700; font-size:0.95rem; color:var(--text-primary); margin-bottom:8px;">
            Patch #{index+1} → {pqc_algo}
        </div>
        <div class="diff-container">
            <div class="diff-panel">
                <div class="diff-header legacy">❌ Legacy Code (Vulnerable)</div>
                <div class="diff-content">{original}</div>
            </div>
            <div class="diff-panel">
                <div class="diff-header pqc">✅ PQC Replacement (Quantum-Safe)</div>
                <div class="diff-content">{patched}</div>
            </div>
        </div>
        <div style="font-size:0.82rem; color:var(--text-secondary); padding:8px 0; line-height:1.6;">
            <strong style="color:var(--accent-amber);">📝 Migration Notes:</strong> {notes}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_limitations():
    """Render the Responsible Design — Limitations panel."""
    st.markdown("""
    <div class="limitations-box">
        <h4>⚠️ Responsible Design — Known Limitations & Potential False Positives</h4>
        <ul>
            <li><strong>Static Analysis Only:</strong> This agent performs static code analysis (AST + regex).
                It cannot trace data flow, resolve dynamic imports, or detect cryptographic usage loaded
                at runtime via reflection or dependency injection.</li>
            <li><strong>Context Blindness:</strong> The scanner cannot distinguish between production code
                and test fixtures / documentation examples. A finding in a unit test may be a false positive.</li>
            <li><strong>AES-128 Heuristic:</strong> AES key-size detection relies on byte-length heuristics.
                If the key is loaded from an external source, the scanner may misclassify AES-256 as AES-128.</li>
            <li><strong>Alias Tracking Limitation:</strong> If a developer aliases an import
                (e.g., <code>import hashlib as h</code>), the regex fallback may miss subsequent usage
                via the alias.  The AST visitor tracks aliases but only for Python.</li>
            <li><strong>Java Analysis Depth:</strong> Java analysis uses regex only (no AST parsing) and
                may produce false positives on string literals in comments or documentation.</li>
            <li><strong>Hybrid Recommendations:</strong> The agent recommends pure PQC replacements.
                For production environments, hybrid schemes (e.g., X25519 + ML-KEM) may be preferred
                during the transition period per NIST SP 800-227.  Consult your organisation's
                cryptographic agility roadmap.</li>
            <li><strong>Library Availability:</strong> Generated patches assume <code>liboqs-python</code>
                (Python) or Bouncy Castle PQC (Java) are available.  These must be installed separately.</li>
            <li><strong>LLM Hallucination Risk:</strong> The Chain of Thought analysis is generated by an LLM
                and may contain inaccuracies.  Always verify the reasoning against authoritative NIST publications.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


def render_audit_timeline(audit_trail: list[dict]):
    """Render the audit trail as a visual timeline."""
    for entry in audit_trail:
        ts = entry.get("timestamp", "")
        if len(ts) > 19:
            ts = ts[:19] + "Z"
        actor = entry.get("actor", "system")
        action = entry.get("action", "")
        detail = entry.get("detail", "")
        actor_emoji = {"agent": "🤖", "human": "👤", "system": "⚙️"}.get(actor, "⚙️")

        st.markdown(f"""
        <div class="audit-entry">
            <span class="audit-timestamp">{ts}</span>
            <span class="audit-action">{actor_emoji} {action}</span>
            <span class="audit-detail">{detail}</span>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# ░░░ DECISION HANDLER ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def _handle_decision(decision: str, feedback: str):
    """
    Resume the LangGraph after the HITL interrupt.

    Sends the human's decision back to the graph via ``Command(resume=...)``,
    which unblocks the ``interrupt()`` in ``node_human_approval``.
    """
    graph = st.session_state["graph"]
    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    try:
        # Resume the graph from the interrupt point
        resume_payload = {"decision": decision, "feedback": feedback}

        for event in graph.stream(
            Command(resume=resume_payload), config, stream_mode="values"
        ):
            phase = event.get("current_phase", "")
            if phase == "complete":
                st.session_state["audit_trail"] = event.get("audit_trail", [])

        st.session_state["phase"] = decision
        st.rerun()

    except Exception as e:
        st.error(f"Error resuming workflow: {e}")
        st.exception(e)


# ════════════════════════════════════════════════════════════════
# ░░░ MAIN DASHBOARD ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

# ── Hero Banner ──
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🔬 Agentic Cyber Defence — Track 1</div>
    <h1>🛡️ PQC Secure-Code Reviewer Agent</h1>
    <p>
        AI-powered static analysis for detecting quantum-vulnerable cryptographic
        primitives.  Automatically generates NIST-standardised ML-KEM (FIPS 203)
        and ML-DSA (FIPS 204) migration patches with full human-in-the-loop
        approval and audit trail.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Phase Tracker ──
render_phase_tracker(st.session_state["phase"])


# ── Sidebar ──
with st.sidebar:
    st.markdown("### ⚙️ Agent Configuration")
    st.markdown(f"**Thread ID:** `{st.session_state['thread_id'][:8]}…`")
    st.markdown(f"**Phase:** `{st.session_state['phase']}`")

    st.markdown("---")
    st.markdown("### 📁 Upload Source Code")

    uploaded_file = st.file_uploader(
        "Upload a Python (.py) or Java (.java) file",
        type=["py", "java", "txt"],
        key="file_uploader",
        help="Upload source code to scan for legacy cryptographic algorithms.",
    )

    use_sample = st.selectbox(
        "Or use a sample file:",
        ["— Select —", "vulnerable_python.py", "VulnerableJava.java"],
        key="sample_selector",
    )

    st.markdown("---")

    if st.button("🔄 Reset Agent", key="reset_btn", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Architecture")
    st.markdown("""
    ```
    ┌─────────┐
    │ INGEST  │
    └────┬────┘
         ▼
    ┌─────────┐
    │  SCAN   │ ← code_scanner_tool
    └────┬────┘
         ▼
    ┌───────────┐
    │INVESTIGATE│ ← LLM + pqc_patch_generator
    └────┬──────┘
         ▼
    ┌───────────┐
    │  APPROVE  │ ← interrupt() HITL Gate
    └────┬──────┘
         ▼
    ┌───────────┐
    │ FINALISE  │ → Audit Trail
    └───────────┘
    ```
    """)


# ════════════════════════════════════════════════════════════════
# ░░░ WORKFLOW EXECUTION ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def load_source_code() -> tuple[str, str] | None:
    """Load source code from upload or sample selection."""
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8", errors="replace")
        return content, uploaded_file.name
    elif use_sample and use_sample != "— Select —":
        import os
        sample_path = os.path.join("sample_files", use_sample)
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                return f.read(), use_sample
    return None


source_data = load_source_code()

# ── PHASE: Upload ──
if st.session_state["phase"] == "upload":
    if source_data:
        source_code, file_name = source_data
        st.session_state["source_code"] = source_code
        st.session_state["file_name"] = file_name

        st.markdown("### 📄 Source Code Preview")
        lang_hint = "python" if file_name.endswith(".py") else "java"
        st.code(source_code, language=lang_hint, line_numbers=True)

        if st.button(
            "🚀 Start PQC Analysis",
            key="start_analysis",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["phase"] = "scanning"
            st.rerun()
    else:
        st.info(
            "👈 Upload a source code file or select a sample from the sidebar to begin.",
            icon="📁",
        )


# ── PHASE: Scanning + Investigation (runs graph up to interrupt) ──
elif st.session_state["phase"] == "scanning":
    render_phase_tracker("scanning")

    with st.status("🔍 Analysing code for quantum-vulnerable cryptography…", expanded=True) as status:
        st.write("📥 Ingesting source file…")

        graph = st.session_state["graph"]
        config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

        initial_state = {
            "source_code": st.session_state["source_code"],
            "file_name": st.session_state["file_name"],
            "messages": [],
            "findings": [],
            "patches": [],
            "audit_trail": [],
            "chain_of_thought": "",
            "uncertainty_statement": "",
            "risk_assessment": "",
            "scan_summary": "",
            "human_decision": "pending",
            "human_feedback": "",
            "current_phase": "",
            "error": "",
        }

        try:
            # Stream until the graph hits the interrupt at human_approval
            events = []
            for event in graph.stream(initial_state, config, stream_mode="values"):
                events.append(event)
                phase = event.get("current_phase", "")
                if phase == "ingest_complete":
                    st.write("✅ File ingested successfully")
                    st.write(f"📋 Language detected: **{event.get('language', 'unknown')}**")
                elif phase == "scan_complete":
                    st.write(f"🔎 Scan complete — {len(event.get('findings', []))} findings")
                    st.write("🧠 Starting deep investigation with LLM…")
                elif phase == "investigation_complete":
                    st.write(f"✅ Investigation complete — {len(event.get('patches', []))} patches generated")

            # Get final state from checkpointer
            final_state = graph.get_state(config)
            state_values = final_state.values

            # Store results in session
            st.session_state["findings"] = state_values.get("findings", [])
            st.session_state["patches"] = state_values.get("patches", [])
            st.session_state["chain_of_thought"] = state_values.get("chain_of_thought", "")
            st.session_state["uncertainty_statement"] = state_values.get("uncertainty_statement", "")
            st.session_state["risk_assessment"] = state_values.get("risk_assessment", "")
            st.session_state["scan_summary"] = state_values.get("scan_summary", "")
            st.session_state["audit_trail"] = state_values.get("audit_trail", [])
            st.session_state["language"] = state_values.get("language", "unknown")

            status.update(label="✅ Analysis complete — Awaiting human review", state="complete")
            st.session_state["phase"] = "review"
            st.rerun()

        except Exception as e:
            status.update(label=f"❌ Error: {e}", state="error")
            st.error(f"An error occurred during analysis: {e}")
            st.exception(e)


# ── PHASE: Human Review (HITL Gate) ──
elif st.session_state["phase"] == "review":
    render_phase_tracker("review")

    findings = st.session_state["findings"]
    patches = st.session_state["patches"]

    # ── Metrics ──
    render_metrics(findings, patches)
    st.markdown("")

    # ── Tabs ──
    tab_findings, tab_cia, tab_cot, tab_patches, tab_limitations, tab_audit = st.tabs([
        "🔍 Findings",
        "🛡️ CIA Triad Analysis",
        "🧠 Chain of Thought",
        "🔧 PQC Patches (Diff View)",
        "⚠️ Limitations",
        "📋 Audit Trail",
    ])

    with tab_findings:
        st.markdown("### 🔍 Detailed Vulnerability Findings")
        if st.session_state["scan_summary"]:
            st.info(st.session_state["scan_summary"], icon="📊")
        if st.session_state["risk_assessment"]:
            st.warning(st.session_state["risk_assessment"], icon="⚡")
        for i, finding in enumerate(findings):
            render_finding_card(finding, i)

    with tab_cia:
        render_cia_analysis(findings, patches)

    with tab_cot:
        st.markdown("### 🧠 Agent Chain of Thought — Explainable AI")
        st.markdown(
            "The agent's complete reasoning process is shown below for "
            "transparency and auditability."
        )
        if st.session_state["chain_of_thought"]:
            st.markdown(st.session_state["chain_of_thought"])
        else:
            st.info("Chain of Thought was not generated (LLM may be unavailable).")

        st.markdown("---")
        st.markdown("#### 🔮 Explicit Uncertainty Statement")
        if st.session_state["uncertainty_statement"]:
            st.warning(st.session_state["uncertainty_statement"], icon="⚠️")

    with tab_patches:
        st.markdown("### 🔧 Proposed PQC Migration Patches")
        st.markdown(
            "Compare the legacy (quantum-vulnerable) code with the proposed "
            "quantum-safe replacement side by side."
        )
        for i, patch in enumerate(patches):
            render_diff(patch, i)

    with tab_limitations:
        st.markdown("### ⚠️ Responsible Design — Limitations & Caveats")
        render_limitations()

    with tab_audit:
        st.markdown("### 📋 Audit Trail (Live)")
        render_audit_timeline(st.session_state["audit_trail"])

    # ══════════════════════════════════════════════════════════
    # ░░░ APPROVAL GATE ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    # ══════════════════════════════════════════════════════════

    st.markdown("---")
    st.markdown("### 👤 Human-in-the-Loop Decision")
    st.markdown(
        "As the human reviewer, you have **final authority** over whether "
        "these patches should be applied.  Review the findings, patches, "
        "and chain of thought above before making your decision."
    )

    feedback = st.text_area(
        "Reviewer comments (optional):",
        key="reviewer_feedback",
        placeholder="Add any notes, concerns, or additional context…",
    )

    col_approve, col_reject = st.columns(2)

    with col_approve:
        if st.button(
            "✅ Approve Patches",
            key="approve_btn",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["human_feedback"] = feedback
            _handle_decision("approved", feedback)

    with col_reject:
        if st.button(
            "❌ Reject Patches",
            key="reject_btn",
            use_container_width=True,
        ):
            st.session_state["human_feedback"] = feedback
            _handle_decision("rejected", feedback)


# ── PHASE: Complete ──
elif st.session_state["phase"] in ("approved", "rejected", "complete"):
    render_phase_tracker("complete")

    decision = st.session_state["phase"]
    findings = st.session_state["findings"]
    patches = st.session_state["patches"]

    render_metrics(findings, patches)

    if decision == "approved":
        st.success(
            "## ✅ Patches Approved\n\n"
            "The PQC migration patches have been approved and are ready "
            "for integration into the codebase.",
            icon="✅",
        )
    else:
        st.error(
            "## ❌ Patches Rejected\n\n"
            "The proposed patches were rejected by the human reviewer. "
            "No changes will be applied.",
            icon="❌",
        )

    if st.session_state["human_feedback"]:
        st.info(
            f"**Reviewer Feedback:** {st.session_state['human_feedback']}",
            icon="💬",
        )

    # ── Audit Trail Download ──
    st.markdown("---")
    st.markdown("### 📥 Download Audit Trail")

    audit_trail = st.session_state["audit_trail"]
    metadata = {
        "file_name": st.session_state["file_name"],
        "language": st.session_state["language"],
        "decision": decision,
        "findings_count": len(findings),
        "patches_count": len(patches),
        "findings": findings,
    }

    col_json, col_txt = st.columns(2)
    with col_json:
        json_content = generate_audit_json(audit_trail, metadata)
        st.download_button(
            "📄 Download JSON Audit (with CIA Summary)",
            data=json_content,
            file_name=f"pqc_audit_{st.session_state['thread_id'][:8]}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col_txt:
        txt_content = generate_audit_txt(audit_trail, metadata)
        st.download_button(
            "📝 Download TXT Audit (with CIA Summary)",
            data=txt_content,
            file_name=f"pqc_audit_{st.session_state['thread_id'][:8]}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.markdown("---")
    tab_c_findings, tab_c_cia, tab_c_patches, tab_c_audit = st.tabs([
        "🔍 Findings",
        "🛡️ CIA Triad Analysis",
        "🔧 Patches & Diffs",
        "📋 Complete Audit Trail",
    ])

    with tab_c_findings:
        st.markdown("### 🔍 Verified Findings")
        for i, finding in enumerate(findings):
            render_finding_card(finding, i)

    with tab_c_cia:
        render_cia_analysis(findings, patches)

    with tab_c_patches:
        st.markdown("### 🔧 Proposed / Approved Patches")
        for i, patch in enumerate(patches):
            render_diff(patch, i)

    with tab_c_audit:
        st.markdown("### 📋 Complete Audit Trail")
        render_audit_timeline(audit_trail)

