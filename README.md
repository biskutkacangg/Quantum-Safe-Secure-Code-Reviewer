# 🛡️ Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool

> **Track 1: Agentic Cyber Defence** — An AI-powered static analysis agent that detects quantum-vulnerable cryptographic primitives in Python/Java source code, generates NIST-standardised ML-KEM & ML-DSA migration patches, and enforces Human-in-the-Loop approval with a complete audit trail.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Hackathon Rubric Alignment](#hackathon-rubric-alignment)
- [Limitations & Responsible Design](#limitations--responsible-design)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 CYBER SOC WEB DASHBOARD (Port 8000)         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │  Upload   │  │ Findings │  │  Monaco  │  │   Audit    │ │
│  │  Panel    │  │  Cards   │  │ Diff(VS) │  │  Download  │ │
│  └─────┬────┘  └──────────┘  └──────────┘  └────────────┘ │
│        │   [Reviewer Portal & Admin SOC Console (RBAC)]     │
│        │              ▲             ▲             ▲         │
│        │              │             │             │         │
│  ┌─────▼──────────────┴─────────────┴─────────────┴───┐    │
│  │              LangGraph State Machine                │    │
│  │                                                     │    │
│  │   ┌────────┐   ┌───────┐   ┌─────────────┐        │    │
│  │   │ INGEST ├──▶│ SCAN  ├──▶│ INVESTIGATE │        │    │
│  │   └────────┘   └───┬───┘   └──────┬──────┘        │    │
│  │                    │              │                 │    │
│  │                    │    ┌─────────▼────────┐       │    │
│  │                    │    │ HUMAN APPROVAL   │       │    │
│  │                    │    │ (interrupt() HITL)│       │    │
│  │                    │    └─────────┬────────┘       │    │
│  │                    │              │                 │    │
│  │                    │    ┌─────────▼────────┐       │    │
│  │                    └───▶│    FINALISE      │       │    │
│  │                         └─────────────────┘       │    │
│  └────────────────────────────────────────────────────┘    │
│                        │                                    │
│              ┌─────────┴─────────┐                         │
│              ▼                   ▼                          │
│  ┌──────────────────┐  ┌───────────────────┐              │
│  │ code_scanner_tool │  │ pqc_patch_gen_tool│              │
│  │ (AST + Regex)     │  │ (ML-KEM / ML-DSA) │              │
│  └──────────────────┘  └───────────────────┘              │
└─────────────────────────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
     ┌─────────────────┐  ┌─────────────────┐
     │  Gemini 1.5 Pro │  │  MemorySaver    │
     │  (LLM Reasoning)│  │  (Checkpointer) │
     └─────────────────┘  └─────────────────┘
```

---

## 🔧 Tech Stack

| Layer          | Technology                        | Purpose                                      |
|----------------|-----------------------------------|----------------------------------------------|
| **Web UI**     | Cyber SOC (FastAPI + Monaco + Tailwind) | High-performance dashboard with side-by-side VS Code diffs |
| **Agent Core** | LangGraph 0.2+                    | Deterministic state machine with HITL support |
| **LLM Engine** | Gemini 2.5 Flash / 1.5 Pro        | Chain of Thought reasoning & analysis         |
| **Tools**      | Python `ast` + Regex              | Static code analysis (Python AST, Java regex) |
| **PQC Standards** | NIST FIPS 203 / 204 / 205      | ML-KEM-768 & ML-DSA-65 migration patches      |
| **Persistence**| LangGraph MemorySaver             | Checkpoint state for interrupt/resume         |
| **Audit**      | SHA-256 chain hash                | Tamper-evident audit trail (JSON + TXT)       |
| **Legacy UI**  | Streamlit 1.38+                   | Optional secondary dashboard (`run_streamlit.bat`) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A Gemini API key (or Anthropic/OpenAI key)

### Running the Application (1-Click Launch)

On Windows, double-click:
```cmd
run_app.bat
```
This automatically launches the high-performance **Cyber SOC Web Dashboard** at `http://localhost:8000`.

Or run manually via terminal:
```bash
# 1. Activate virtual environment
.\.venv\Scripts\activate

# 2. Start the Cyber SOC server
python server.py
# Opens at: http://localhost:8000
```

*(Note: If you wish to use the legacy Streamlit interface, run `run_streamlit.bat` or `streamlit run app.py`).*

### Using the Agent

1. **Upload** a `.py` or `.java` file (or select a sample)
2. **Click** "Start PQC Analysis"
3. **Review** the findings, Chain of Thought, and proposed patches
4. **Approve** or **Reject** the migration patches
5. **Download** the audit trail (JSON/TXT)

---

## ⚙️ How It Works

### The Five-Node Pipeline

1. **INGEST** — Validates the uploaded file, detects the programming language, initialises the audit trail.

2. **SCAN** — The `code_scanner_tool` performs deterministic static analysis:
   - **Python**: Full AST walk (import tracking, call-site detection, alias resolution) + regex fallback
   - **Java**: Comprehensive regex pattern matching
   - Detects: RSA, ECDSA, DSA, DH, ECDH, DES, 3DES, Blowfish, RC4, MD5, SHA-1, AES-128

3. **INVESTIGATE** — The LLM (Gemini 1.5 Pro) analyses findings with:
   - Deep Chain of Thought reasoning
   - True positive / false positive assessment
   - Quantum threat analysis (Shor's vs Grover's algorithm impact)
   - Explicit uncertainty statements
   - Triggers `pqc_patch_generator_tool` to create migration code

4. **HUMAN APPROVAL** — The graph **pauses** using `interrupt()`:
   - The Cyber SOC Web UI renders an interactive review modal with side-by-side Monaco code diffs
   - The human reviewer sees: findings, CoT, side-by-side diffs, limitations, and CIA Triad impacts
   - The graph **resumes only** when the authenticated human clicks Approve or Reject
   - Enforced by LangGraph's stateful `Command(resume=...)` mechanism

5. **FINALISE** — Generates the final audit trail, marks patches as approved/rejected, closes the workflow.

### Tool Specifications

#### `code_scanner_tool`
- **Input**: Source code string, filename, language
- **Output**: JSON array of `CryptoFinding` objects
- **Detection methods**: AST import/call visitors (Python), regex patterns (both)
- **Coverage**: 14+ algorithm families across 40+ detection patterns
- **Confidence scoring**: 0.95 (AST import), 0.85 (AST call), 0.70-0.75 (regex)

#### `pqc_patch_generator_tool`
- **Input**: JSON array of findings from the scanner
- **Output**: JSON array of `PQCPatch` objects
- **Templates**: ML-KEM-768 (key encapsulation), ML-DSA-65 (signatures), AES-256-GCM (symmetric), SHA-3-256 (hashing)
- **Languages**: Python (liboqs-python) and Java (Bouncy Castle PQC)

---

## 📁 Project Structure

```
hackathon-cybersecurity-agents/
├── app.py                          # Streamlit dashboard (main entry point)
├── run_app.bat                     # Windows 1-click launcher
├── requirements.txt                # Python dependencies
├── pqc_config.yaml                 # Cryptographic policy & PQC configuration
├── .env.example                    # Environment variable template
├── pqc_agent/                      # Core agent package (tools, state, graph, audit, cli)
├── reports/                        # Publication-grade PDFs & HTML research deliverables
│   ├── PQC_Model_Parameters_and_Results_Paper_Comparison.pdf   # Literature Review (Google Scholar 2020–2025)
│   └── PQC_Vulnerabilities_and_Replacements_Catalog.pdf        # Deprecated Algorithms & NIST Targets Catalog
├── scripts/                        # PDF & report build scripts (generate_all_reports.py)
├── tests/                          # Automated unit & E2E verification test suites
├── docs/                           # Architectural blueprints & engineering specifications
├── sample_files/                   # Intentionally vulnerable test code (Python / Java)
├── audit_outputs/                  # Persisted runtime SHA-256 audit logs
└── README.md                       # Master documentation & guide
```

---

## 🏆 Hackathon Rubric Alignment

### Technical Implementation (25%)

| Criterion | Evidence |
|-----------|----------|
| Code quality | Fully typed Python with Pydantic models, comprehensive docstrings, separation of concerns |
| Architecture | Five-node LangGraph state machine with conditional edges, checkpointer persistence, and modular tool system |
| Correctness | AST-based detection (not just regex) with deduplication, confidence scoring, and severity classification |
| PQC knowledge | Direct mapping to NIST FIPS 203/204/205/202 standards with correct algorithm parameters |

### Effective Use of Agentic AI (20%)

| Criterion | Evidence |
|-----------|----------|
| Tool calling | Two custom `@tool` functions integrated via LangGraph `ToolNode` pattern |
| State management | Typed `AgentState` with `add_messages` reducer, persistent checkpointing |
| HITL gate | `interrupt()` / `Command(resume=...)` — graph *physically pauses* until human input |
| Explainability | Full Chain of Thought rendered in dedicated tab, explicit uncertainty statements |
| Autonomy + Control | Agent scans and reasons autonomously, but *never* applies patches without human approval |

### Cybersecurity Value (20%)

| Criterion | Evidence |
|-----------|----------|
| Real threat model | Addresses the "Harvest Now, Decrypt Later" quantum threat with concrete NIST mitigations |
| Actionable output | Not just findings — generates production-ready ML-KEM/ML-DSA replacement code |
| Audit compliance | SHA-256 chain-hashed audit trail for regulatory compliance (SOC 2, NIST SP 800-53) |
| Responsible disclosure | Explicit limitations panel documenting false positive risks, static analysis blind spots |
| Academic rigour | Correctly distinguishes Shor's (breaks asymmetric) vs Grover's (weakens symmetric/hash) impact |

### Three Mandatory Pillars

| Pillar | Implementation |
|--------|----------------|
| **Take in evidence** | File upload → AST/regex scan → structured `CryptoFinding` objects with confidence scores |
| **Investigate and decide** | LLM Chain of Thought → explicit uncertainty → risk assessment → patch generation |
| **Act safely** | Hard `interrupt()` HITL gate → Approve/Reject buttons → audit trail → no auto-apply |

---

## ⚠️ Limitations & Responsible Design

This agent **explicitly discloses** the following limitations on the dashboard:

1. **Static Analysis Only** — Cannot trace data flow, resolve dynamic imports, or detect runtime-loaded cryptography
2. **Context Blindness** — Cannot distinguish production code from test fixtures
3. **AES-128 Heuristic** — Key size detection relies on byte-length heuristics
4. **Alias Tracking** — Regex fallback may miss aliased imports (`import hashlib as h`)
5. **Java Analysis Depth** — Regex-only (no Java AST parser), may false-positive on comments
6. **Hybrid Recommendations** — Recommends pure PQC; production may prefer hybrid schemes (NIST SP 800-227)
7. **Library Availability** — Patches assume liboqs-python / Bouncy Castle are installed
8. **LLM Hallucination Risk** — CoT analysis may contain inaccuracies; verify against NIST publications

---

## 📜 License

MIT License — Built for the Agentic Cyber Defence Hackathon.
