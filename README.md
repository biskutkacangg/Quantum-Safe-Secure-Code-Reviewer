# 🛡️ PQC Secure-Code Reviewer Agent

> **Track 1: Agentic Cyber Defence** — An AI-powered static analysis agent that detects quantum-vulnerable cryptographic primitives in Python/Java source code, generates NIST-standardised ML-KEM & ML-DSA migration patches, and enforces Human-in-the-Loop approval with a complete audit trail.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-red?style=flat-square&logo=streamlit)
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
│                    STREAMLIT DASHBOARD                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │  Upload   │  │ Findings │  │   Diff   │  │   Audit    │ │
│  │  Panel    │  │  Cards   │  │   View   │  │  Download  │ │
│  └─────┬────┘  └──────────┘  └──────────┘  └────────────┘ │
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
| **Frontend**   | Streamlit 1.38+                   | Interactive dashboard with real-time updates  |
| **Agent Core** | LangGraph 0.2+                    | Deterministic state machine with HITL support |
| **LLM**        | Gemini 1.5 Pro / Claude 3.5       | Chain of Thought reasoning & analysis         |
| **Tools**      | Python `ast` + Regex              | Static code analysis (Python AST, Java regex) |
| **PQC**        | liboqs-python / Bouncy Castle     | ML-KEM (FIPS 203) & ML-DSA (FIPS 204) patches|
| **Persistence**| LangGraph MemorySaver             | Checkpoint state for interrupt/resume         |
| **Audit**      | SHA-256 chain hash                | Tamper-evident audit trail (JSON + TXT)       |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- A Gemini API key (or Anthropic/OpenAI key)

### Installation

```bash
# 1. Clone the repository
cd hackathon-cybersecurity-agents

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Run the dashboard
streamlit run app.py
```

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
   - The Streamlit UI renders an interactive review dashboard
   - The human reviewer sees: findings, CoT, side-by-side diffs, limitations
   - The graph **resumes only** when the human clicks Approve or Reject
   - This is enforced by LangGraph's `Command(resume=...)` mechanism

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
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .gitignore
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
├── pqc_agent/                      # Core agent package
│   ├── __init__.py
│   ├── state.py                    # AgentState TypedDict + Pydantic models
│   ├── tools.py                    # code_scanner_tool + pqc_patch_generator_tool
│   ├── prompts.py                  # LLM prompt templates
│   ├── graph.py                    # LangGraph state machine (5 nodes)
│   └── audit.py                    # Audit trail generator (SHA-256 chain hash)
├── sample_files/                   # Test files with intentional vulnerabilities
│   ├── vulnerable_python.py        # Python: RSA, ECDSA, DES, MD5, SHA-1, etc.
│   └── VulnerableJava.java         # Java: RSA, ECDSA, DSA, DES, MD5, etc.
└── README.md
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
