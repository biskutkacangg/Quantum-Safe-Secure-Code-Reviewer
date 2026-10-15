# ============================================================
# pqc_agent/graph.py
# LangGraph State Machine — Core Workflow Engine
# ============================================================
"""
Defines the complete LangGraph state graph for the PQC Secure-Code
Reviewer Agent.  The graph implements a five-node pipeline:

    ┌─────────┐    ┌─────────────┐    ┌──────────────┐
    │  INGEST │───▶│   SCAN      │───▶│ INVESTIGATE  │
    └─────────┘    └─────────────┘    └──────┬───────┘
                                             │
                                             ▼
                                    ┌────────────────┐
                         ┌─────────│ HUMAN APPROVAL  │◀── interrupt()
                         │         │   (HITL Gate)    │
                         │         └────────────────┘
                         ▼
                   ┌───────────┐
                   │  FINALISE │───▶ END
                   └───────────┘

The workflow **pauses** at the HUMAN APPROVAL node using LangGraph's
``interrupt()`` primitive, requiring explicit human input via
``Command(resume=...)`` before proceeding to finalisation.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

from pqc_agent.prompts import (
    INVESTIGATION_PROMPT,
    PATCH_SUMMARY_PROMPT,
    SYSTEM_PROMPT,
)
from pqc_agent.state import AgentState, AuditEntry
from pqc_agent.tools import ALL_TOOLS, code_scanner_tool, pqc_patch_generator_tool

load_dotenv()

logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════
# ░░░ LLM PROVIDER FACTORY ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def _get_llm():
    """Instantiate the configured LLM with tool-calling support."""
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    model = os.getenv("LLM_MODEL", "gemini-1.5-pro")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.1"))

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(
            model=model,
            temperature=temperature,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    # Bind tools so the LLM can invoke them
    return llm.bind_tools(ALL_TOOLS)


# ════════════════════════════════════════════════════════════════
# ░░░ UTILITY HELPERS ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def _make_audit(actor: str, action: str, detail: str, **meta) -> dict:
    """Create an AuditEntry dict."""
    return AuditEntry(
        actor=actor, action=action, detail=detail, metadata=meta
    ).model_dump()


def _detect_language(file_name: str, source_code: str) -> str:
    """Heuristic language detection from filename and content."""
    name_lower = file_name.lower()
    if name_lower.endswith(".py"):
        return "python"
    elif name_lower.endswith(".java"):
        return "java"
    # Content-based fallback
    if "def " in source_code or "import " in source_code:
        return "python"
    if "public class" in source_code or "System.out" in source_code:
        return "java"
    return "unknown"


# ════════════════════════════════════════════════════════════════
# ░░░ NODE DEFINITIONS ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def node_ingest(state: AgentState) -> dict:
    """
    Node 1 — INGEST
    ────────────────
    Validates the uploaded source code, detects the programming language,
    and initialises the audit trail.
    """
    source_code = state.get("source_code", "")
    file_name = state.get("file_name", "uploaded_file")
    language = _detect_language(file_name, source_code)

    audit_trail = state.get("audit_trail", [])
    audit_trail.append(
        _make_audit(
            "system",
            "INGEST",
            f"Ingested file '{file_name}' ({len(source_code)} chars, "
            f"language={language})",
            file_name=file_name,
            language=language,
            code_length=len(source_code),
        )
    )

    return {
        "language": language,
        "current_phase": "ingest_complete",
        "audit_trail": audit_trail,
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"I have uploaded a {language} file named '{file_name}' "
                    f"({len(source_code)} characters). Please scan it for "
                    f"legacy cryptographic algorithms that are vulnerable to "
                    f"quantum computing attacks."
                )
            ),
        ],
    }


def node_scan(state: AgentState) -> dict:
    """
    Node 2 — SCAN
    ──────────────
    Directly invokes the code_scanner_tool (deterministic, no LLM needed)
    to perform AST/regex analysis, then stores findings in state.
    """
    source_code = state.get("source_code", "")
    file_name = state.get("file_name", "uploaded_file")
    language = state.get("language", "python")

    # Direct tool invocation (not LLM-mediated — deterministic)
    findings_json = code_scanner_tool.invoke(
        {
            "source_code": source_code,
            "file_name": file_name,
            "language": language,
        }
    )

    findings = json.loads(findings_json)

    # Build human-readable summary
    if findings:
        severity_counts: dict[str, int] = {}
        algo_set: set[str] = set()
        for f in findings:
            sev = f.get("severity", "UNKNOWN")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            algo_set.add(f.get("algorithm_detected", "UNKNOWN"))

        summary_parts = [
            f"Detected **{len(findings)} legacy cryptographic finding(s)** "
            f"in `{file_name}`.",
            f"Algorithms found: {', '.join(sorted(algo_set))}.",
            "Severity breakdown: "
            + ", ".join(f"{k}: {v}" for k, v in sorted(severity_counts.items())),
        ]
        scan_summary = " ".join(summary_parts)
    else:
        scan_summary = (
            f"No legacy cryptographic primitives detected in `{file_name}`. "
            f"The code appears to be quantum-safe or does not contain "
            f"cryptographic operations."
        )

    audit_trail = state.get("audit_trail", [])
    audit_trail.append(
        _make_audit(
            "agent",
            "SCAN_COMPLETE",
            f"Found {len(findings)} findings in {file_name}",
            finding_count=len(findings),
        )
    )

    return {
        "findings": findings,
        "scan_summary": scan_summary,
        "current_phase": "scan_complete",
        "audit_trail": audit_trail,
        "messages": [
            AIMessage(
                content=(
                    f"## Scan Results\n\n{scan_summary}\n\n"
                    f"I will now investigate each finding in depth and "
                    f"generate quantum-safe patches."
                )
            ),
        ],
    }


def node_investigate(state: AgentState) -> dict:
    """
    Node 3 — INVESTIGATE
    ─────────────────────
    Sends findings to the LLM for deep analysis with Chain of Thought
    reasoning.  The LLM may call the pqc_patch_generator_tool as part
    of its reasoning loop.
    """
    findings = state.get("findings", [])
    source_code = state.get("source_code", "")
    language = state.get("language", "python")

    if not findings:
        return {
            "chain_of_thought": "No findings to investigate.",
            "uncertainty_statement": "N/A — no vulnerabilities detected.",
            "risk_assessment": "The scanned code does not contain detectable legacy cryptographic primitives.",
            "patches": [],
            "current_phase": "investigation_complete",
            "messages": [
                AIMessage(
                    content="No legacy cryptographic findings to investigate. "
                    "The code appears quantum-safe."
                )
            ],
        }

    findings_json = json.dumps(findings, indent=2)

    # --- Generate patches deterministically ---
    patches_json_str = pqc_patch_generator_tool.invoke(
        {"findings_json": findings_json}
    )
    patches = json.loads(patches_json_str)

    # --- LLM deep analysis with CoT ---
    try:
        llm = _get_llm()
        investigation_msg = HumanMessage(
            content=INVESTIGATION_PROMPT.format(
                findings_json=findings_json,
                source_code=source_code,
                language=language,
            )
        )

        # Get the full message history and add investigation prompt
        messages = list(state.get("messages", []))
        messages.append(investigation_msg)

        response = llm.invoke(messages)
        raw_content = response.content
        if isinstance(raw_content, list):
            parts = []
            for item in raw_content:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                elif isinstance(item, str):
                    parts.append(item)
            chain_of_thought = "\n".join(parts) if parts else str(raw_content)
        else:
            chain_of_thought = str(raw_content)

        # Extract uncertainty statements
        uncertainty_keywords = [
            "uncertain", "cannot determine", "manual verification",
            "false positive", "may not", "unclear", "limited confidence",
            "requires human", "potential", "might be",
        ]
        uncertainty_lines = []
        for line in chain_of_thought.split("\n"):
            if any(kw in line.lower() for kw in uncertainty_keywords):
                uncertainty_lines.append(line.strip())

        uncertainty_statement = (
            "\n".join(uncertainty_lines)
            if uncertainty_lines
            else "No explicit uncertainties identified. All findings appear "
            "to be high-confidence true positives, but manual review is "
            "always recommended for security-critical code."
        )

    except Exception as e:
        logger.warning(f"LLM investigation fell back to static reasoning: {e}")
        # Build rich deterministic Chain of Thought
        cot_lines = [
            "### Chain of Thought Analysis (Static Rule Engine)",
            "",
            "1. **Detection & Triage**:",
            f"   - Scanned {len(findings)} cryptographic operations across the ingested code.",
            "   - Identified legacy public-key algorithms vulnerable to Shor's algorithm (polynomial time discrete log / integer factorisation).",
            "",
            "2. **Algorithm Threat Breakdown**:",
        ]
        seen_algos = set()
        for f in findings:
            algo = f.get("algorithm_detected", "UNKNOWN")
            if algo not in seen_algos:
                seen_algos.add(algo)
                threat = f.get("quantum_threat_level", "Quantum vulnerable")
                cot_lines.append(f"   - **{algo}**: {threat}")

        cot_lines.extend([
            "",
            "3. **Migration Strategy**:",
            "   - Key encapsulation mechanisms (RSA, DH, ECDH) mapped to **ML-KEM (FIPS 203)**.",
            "   - Digital signature schemes (ECDSA, DSA, EdDSA) mapped to **ML-DSA (FIPS 204)**.",
            "   - Legacy symmetric/hash primitives (DES, MD5, SHA-1) mapped to **AES-256-GCM** / **SHA-3-256**.",
            "",
            "4. **Human Review Directive**:",
            "   - All proposed patches require explicit human review and sign-off before application.",
        ])
        chain_of_thought = "\n".join(cot_lines)
        uncertainty_statement = (
            "Static analysis detected AST and pattern matches with high structural confidence, "
            "but runtime cryptographic dependencies and key exchange protocol contexts require "
            "manual human verification."
        )

    # --- Risk assessment ---
    critical_count = sum(
        1 for f in findings if f.get("severity") == "CRITICAL"
    )
    high_count = sum(1 for f in findings if f.get("severity") == "HIGH")
    risk_assessment = (
        f"Overall Risk: {'CRITICAL' if critical_count > 0 else 'HIGH' if high_count > 0 else 'MEDIUM'}. "
        f"{critical_count} critical and {high_count} high-severity findings. "
        f"This codebase requires immediate PQC migration planning to maintain "
        f"cryptographic agility against quantum threats."
    )

    audit_trail = state.get("audit_trail", [])
    audit_trail.append(
        _make_audit(
            "agent",
            "INVESTIGATION_COMPLETE",
            f"Generated {len(patches)} patches, performed LLM analysis",
            patch_count=len(patches),
            risk_level="CRITICAL" if critical_count > 0 else "HIGH",
        )
    )

    return {
        "chain_of_thought": chain_of_thought,
        "uncertainty_statement": uncertainty_statement,
        "risk_assessment": risk_assessment,
        "patches": patches,
        "current_phase": "investigation_complete",
        "audit_trail": audit_trail,
        "messages": [
            AIMessage(content=chain_of_thought),
        ],
    }


def node_human_approval(state: AgentState) -> dict:
    """
    Node 4 — HUMAN APPROVAL (HITL Gate)
    ────────────────────────────────────
    **This node PAUSES the graph** using ``interrupt()``.

    The interrupt surfaces the findings and patches to the Streamlit UI,
    which presents "Approve" / "Reject" buttons.  The graph resumes only
    when the human provides their decision via ``Command(resume=...)``.
    """
    findings = state.get("findings", [])
    patches = state.get("patches", [])
    risk_assessment = state.get("risk_assessment", "")

    # ── INTERRUPT — blocks here until human resumes ──
    human_response = interrupt(
        {
            "question": "Review the PQC migration patches and approve or reject.",
            "findings_count": len(findings),
            "patches_count": len(patches),
            "risk_assessment": risk_assessment,
            "requires_action": True,
        }
    )

    # Parse the human's response
    if isinstance(human_response, dict):
        decision = human_response.get("decision", "rejected")
        feedback = human_response.get("feedback", "")
    elif isinstance(human_response, str):
        decision = "approved" if "approv" in human_response.lower() else "rejected"
        feedback = human_response
    else:
        decision = "rejected"
        feedback = "Invalid response format — defaulting to rejection for safety."

    audit_trail = state.get("audit_trail", [])
    audit_trail.append(
        _make_audit(
            "human",
            f"HITL_DECISION_{decision.upper()}",
            f"Human reviewer {'approved' if decision == 'approved' else 'rejected'} "
            f"the proposed patches.",
            decision=decision,
            feedback=feedback,
        )
    )

    return {
        "human_decision": decision,
        "human_feedback": feedback,
        "current_phase": "approval_complete",
        "audit_trail": audit_trail,
        "messages": [
            HumanMessage(
                content=f"Human decision: {decision}. Feedback: {feedback}"
            ),
        ],
    }


def node_finalise(state: AgentState) -> dict:
    """
    Node 5 — FINALISE
    ──────────────────
    Generates the final audit trail and closes the workflow.  If the
    human approved, the patches are marked as "ready to apply".
    If rejected, they are archived with the rejection reason.
    """
    decision = state.get("human_decision", "rejected")
    feedback = state.get("human_feedback", "")

    if decision == "approved":
        final_message = (
            "## ✅ Patches Approved\n\n"
            "The proposed PQC migration patches have been **approved** by "
            "the human reviewer. The patches are ready for integration.\n\n"
            f"**Reviewer feedback:** {feedback or 'No additional comments.'}"
        )
        action = "PATCHES_APPROVED"
    else:
        final_message = (
            "## ❌ Patches Rejected\n\n"
            "The proposed patches have been **rejected** by the human "
            "reviewer. No changes will be applied.\n\n"
            f"**Rejection reason:** {feedback or 'No reason provided.'}"
        )
        action = "PATCHES_REJECTED"

    audit_trail = state.get("audit_trail", [])
    audit_trail.append(
        _make_audit(
            "system",
            action,
            final_message,
            decision=decision,
        )
    )

    # Final audit closure entry
    audit_trail.append(
        _make_audit(
            "system",
            "WORKFLOW_COMPLETE",
            f"PQC review workflow completed. Decision: {decision}. "
            f"Total audit entries: {len(audit_trail) + 1}.",
        )
    )

    return {
        "current_phase": "complete",
        "audit_trail": audit_trail,
        "messages": [AIMessage(content=final_message)],
    }


# ════════════════════════════════════════════════════════════════
# ░░░ ROUTING LOGIC ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def route_after_scan(state: AgentState) -> str:
    """Route after scan: if findings exist, investigate; else finalise."""
    findings = state.get("findings", [])
    if findings:
        return "investigate"
    return "finalise"


def route_after_approval(state: AgentState) -> str:
    """Always proceed to finalise after human decision."""
    return "finalise"


# ════════════════════════════════════════════════════════════════
# ░░░ GRAPH BUILDER ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

def build_graph(checkpointer=None):
    """
    Construct and compile the PQC Reviewer LangGraph.

    Args:
        checkpointer: A LangGraph checkpointer for state persistence.
                      If None, uses MemorySaver (in-process only).

    Returns:
        Compiled LangGraph application ready for .invoke() or .stream().
    """
    if checkpointer is None:
        checkpointer = MemorySaver()

    builder = StateGraph(AgentState)

    # ── Register nodes ──
    builder.add_node("ingest", node_ingest)
    builder.add_node("scan", node_scan)
    builder.add_node("investigate", node_investigate)
    builder.add_node("human_approval", node_human_approval)
    builder.add_node("finalise", node_finalise)

    # ── Define edges ──
    builder.add_edge(START, "ingest")
    builder.add_edge("ingest", "scan")
    builder.add_conditional_edges(
        "scan",
        route_after_scan,
        {"investigate": "investigate", "finalise": "finalise"},
    )
    builder.add_edge("investigate", "human_approval")
    builder.add_edge("human_approval", "finalise")
    builder.add_edge("finalise", END)

    # ── Compile with checkpointer (required for interrupt()) ──
    graph = builder.compile(checkpointer=checkpointer)

    return graph


# ── Module-level convenience: pre-built graph instance ──
_default_checkpointer = MemorySaver()
app = build_graph(checkpointer=_default_checkpointer)
