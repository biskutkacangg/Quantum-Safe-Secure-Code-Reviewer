# 📁 Project Structure & File Guide
## Post-Quantum Cryptography (PQC) Secure-Code Reviewer Agent

This document provides a comprehensive, file-by-file breakdown of the **PQC Secure-Code Reviewer** repository. It explains the exact role of every file, its internal components, and how data flows across the system.

---

## 🗺️ High-Level Directory Tree

```
hackathon-cybersecurity-agents/
│
├── .github/
│   └── workflows/
│       ├── ci.yml                           # GitHub Actions CI matrix test runner
│       └── security-scan.yml                # DevSecOps SAST, SCA & PQC compliance workflow
│
├── .streamlit/
│   └── config.toml                          # Streamlit UI theme & server configuration
│
├── pqc_agent/                               # Core Agent Python Package
│   ├── __init__.py                          # Package initialization & public API exports
│   ├── state.py                             # LangGraph state schema & Pydantic data models
│   ├── tools.py                             # AST/Regex scanner & NIST PQC patch generator tools
│   ├── prompts.py                           # LLM system prompts & investigation templates
│   ├── graph.py                             # 5-node LangGraph state machine & HITL interrupt
│   ├── audit.py                             # Cryptographic tamper-evident SHA-256 audit logger
│   └── cli.py                               # DevSecOps headless CLI scanner for CI/CD pipelines
│
├── sample_files/                            # Test Bench / Vulnerable Code Samples
│   ├── vulnerable_python.py                 # Intentionally vulnerable Python crypto sample
│   └── VulnerableJava.java                  # Intentionally vulnerable Java crypto sample
│
├── audit_outputs/                           # Directory storing generated audit logs (JSON/TXT)
│
├── app.py                                   # Streamlit Interactive Web Application Dashboard
├── pqc_config.yaml                          # Enterprise cryptographic policy & scanner config
├── requirements.txt                         # Python dependencies manifest
├── .env.example                             # Environment variable template for LLM API keys
├── .gitignore                               # Git file ignore specifications
├── .pre-commit-config.yaml                  # Pre-commit hook for local cryptographic policy gate
│
├── Dockerfile                               # Hardened multi-stage container build definition
├── docker-compose.yml                       # Container orchestration & healthcheck service
├── .dockerignore                            # Docker build context exclusion rules
│
├── test_pqc_agent.py                        # Automated unit & integration verification test suite
├── test_graph_e2e.py                        # End-to-end LangGraph HITL state machine verification
├── generate_pdf.py                          # Multi-page architecture blueprint PDF compiler
├── generate_one_page_pdf.py                 # Executive 1-page summary PDF compiler for supervisors
│
├── PQC_Secure_Code_Reviewer_Blueprint.pdf   # Multi-page rendered architecture blueprint
├── PQC_Framework_Executive_Summary.pdf      # Single-page executive summary PDF for supervisors
├── devsecops_ai_architecture_blueprint.md   # Markdown blueprint with threat models & compliance
├── README.md                                # Repository overview, installation & demo guide
└── PROJECT_STRUCTURE.md                     # THIS FILE — Complete directory & file breakdown
```

---

## 📄 Detailed File-by-File Breakdown

### 1. Root Application & Configuration Files

| File Name | Exact Role & Description |
| :--- | :--- |
| [`app.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/app.py) | **The Streamlit Web Application Dashboard (Presentation Layer).**<br>• Renders the dark glassmorphic cybersecurity dashboard (Port 8501).<br>• Manages user sessions, file uploads (`.py`, `.java`), and sample selection.<br>• Drives the visual 5-phase workflow tracker (`Upload` ➔ `Scanning` ➔ `Review` ➔ `Approved/Rejected`).<br>• Renders interactive findings cards, quantum threat explanations, and Chain-of-Thought reasoning.<br>• Displays side-by-side code diffs comparing legacy code with proposed post-quantum patches.<br>• Houses the Human-in-the-Loop (HITL) gate buttons (**Approve** / **Reject**) that resume the paused LangGraph workflow.<br>• Enables one-click download of timestamped audit logs (JSON and TXT) with SHA-256 hash chains. |
| [`pqc_config.yaml`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_config.yaml) | **Enterprise Cryptographic Policy & Scanner Configuration.**<br>• Defines policy thresholds (e.g. `fail_on_severity: CRITICAL`).<br>• Configures target post-quantum algorithms: `ML-KEM-768` (FIPS 203), `ML-DSA-65` (FIPS 204), `AES-256-GCM` (NIST SP 800-38D), `SHA-3-256` (FIPS 202).<br>• Configures hybrid classical + PQC pairings (`X25519_ML-KEM-768`, `Ed25519_ML-DSA-65`).<br>• Specifies file inclusion globs (`**/*.py`, `**/*.java`) and exclusion filters (`.venv`, `node_modules`, `tests`). |
| [`requirements.txt`](file:///c:/Users/User/hackathon-cybersecurity-agents/requirements.txt) | **Python Dependencies Manifest.**<br>• Lists required production libraries: `streamlit`, `langgraph`, `langchain-core`, `langchain-google-genai`, `cryptography`, `pydantic`, `pygments`, `python-dotenv`, and `pyyaml`. |
| [`.env.example`](file:///c:/Users/User/hackathon-cybersecurity-agents/.env.example) | **Environment Variables Template.**<br>• Provides a template for configuring the LLM provider (`gemini`, `anthropic`, or `openai`), model name (`gemini-1.5-pro`), temperature (`0.1`), and API keys (`GOOGLE_API_KEY`). |
| [`.gitignore`](file:///c:/Users/User/hackathon-cybersecurity-agents/.gitignore) | **Git Exclusion Rules.**<br>• Prevents virtual environments (`.venv/`), caches (`__pycache__/`), OS temp files, IDE configs, local secrets, and raw audit outputs from being tracked in version control. |
| [`.pre-commit-config.yaml`](file:///c:/Users/User/hackathon-cybersecurity-agents/.pre-commit-config.yaml) | **DevSecOps Shift-Left Pre-Commit Hook.**<br>• Executes automated formatting checks before commits.<br>• Runs `pqc_agent.cli` against staged Python and Java files to block commits introducing deprecated algorithms locally. |
| [`README.md`](file:///c:/Users/User/hackathon-cybersecurity-agents/README.md) | **Primary Repository Documentation.**<br>• Overview of the system, problem statement (Harvest Now, Decrypt Later), NIST PQC standards, quickstart commands, and hackathon rubric alignment. |

---

### 2. Core Agent Package (`pqc_agent/`)

This package houses the business logic, detection tools, state definitions, LangGraph workflow, and audit generation.

| File Name | Exact Role & Description |
| :--- | :--- |
| [`pqc_agent/__init__.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/__init__.py) | **Package Initializer & Public Symbol Exporter.**<br>• Exports key classes and functions (`AgentState`, `AuditEntry`, `CryptoFinding`, `PQCPatch`, `code_scanner_tool`, `pqc_patch_generator_tool`, `build_graph`, `LEGACY_CRYPTO_DB`) for clean imports across the workspace. |
| [`pqc_agent/state.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/state.py) | **Canonical State Schema & Pydantic Data Models.**<br>• `AgentState` (TypedDict): The single source of truth that flows through every node in the LangGraph graph. Contains messages, source code, detected findings, LLM reasoning, patches, human decision, and audit trail.<br>• `CryptoFinding` (Pydantic BaseModel): Represents a detected legacy cryptographic vulnerability with fields for line number, code snippet, algorithm, severity, confidence, and quantum threat explanation.<br>• `PQCPatch` (Pydantic BaseModel): Represents a synthesized post-quantum patch linking to a finding ID, with original code, patched code, target PQC algorithm, and migration notes.<br>• `AuditEntry` (Pydantic BaseModel): Immutable timestamped log entry with actor (`agent`, `human`, `system`), action name, detail narrative, and metadata dictionary. |
| [`pqc_agent/tools.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/tools.py) | **Static Scanner & NIST PQC Patch Generator (The Tool Layer).**<br>• `LEGACY_CRYPTO_DB`: Knowledge base mapping deprecated algorithms (RSA, ECDSA, DSA, DH, DES, 3DES, MD5, SHA-1, AES-128) to Shor's/Grover's threat impacts and replacement standards.<br>• `PythonCryptoVisitor` (ast.NodeVisitor): Traverses Python Abstract Syntax Trees to detect deprecated module imports (`Crypto.Cipher`, `cryptography.hazmat`) and dangerous function calls (`rsa.generate_private_key`, `ec.generate_private_key`, `hashlib.md5`). Assigns confidence scores (0.95 for imports, 0.85 for calls).<br>• Java Regex Scanner: Inspects Java source files for calls like `KeyPairGenerator.getInstance("RSA")` and `Cipher.getInstance("DES")` (0.75 confidence).<br>• `code_scanner_tool`: Decorated `@tool` wrapping the dual-engine scanner for LangGraph integration.<br>• `pqc_patch_generator_tool`: Decorated `@tool` synthesizing concrete Python (using `oqs` / `liboqs-python`) and Java (using Bouncy Castle PQC `bcprov-jdk18on`) replacement code for ML-KEM-768 and ML-DSA-65. |
| [`pqc_agent/prompts.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/prompts.py) | **LLM Prompts & Cognitive Guidance.**<br>• `SYSTEM_PROMPT`: Establishes the agent persona as an expert Post-Quantum Cryptography Secure-Code Reviewer, defining guiding principles (evidence-based, explicit uncertainty, human supremacy).<br>• `INVESTIGATION_PROMPT`: Instructs the LLM to inspect scanner findings, reason step-by-step using Chain of Thought, distinguish true positives from test fixtures, and explicitly state confidence boundaries.<br>• `PATCH_SUMMARY_PROMPT`: Guides the LLM in summarizing proposed patches, detailing FIPS compliance and deployment considerations (key sizes, latency). |
| [`pqc_agent/graph.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/graph.py) | **LangGraph State Machine Engine (The Brain).**<br>• Implements the 5-node pipeline: `node_ingest` ➔ `node_scan` ➔ `node_investigate` ➔ `node_human_approval` ➔ `node_finalise`.<br>• `node_ingest`: Validates file size, determines language, creates genesis audit block.<br>• `node_scan`: Deterministically executes `code_scanner_tool` without requiring LLM tokens.<br>• `node_investigate`: Calls `pqc_patch_generator_tool` and runs LLM reasoning with a rich deterministic static fallback if the LLM API is unreachable.<br>• `node_human_approval`: **Halts execution** using LangGraph's native `interrupt()` primitive. Surfaces findings to the human reviewer and blocks until resumed via `Command(resume=...)`.<br>• `node_finalise`: Finalizes state, marks patches as approved or rejected, and writes final audit closure entries.<br>• `build_graph()`: Compiles the `StateGraph` with a checkpointer (`MemorySaver`) for state persistence. |
| [`pqc_agent/audit.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/audit.py) | **Cryptographic Tamper-Evident Audit Generator.**<br>• `_compute_chain_hash()`: Computes a recursive SHA-256 hash chain over all audit entries: $\text{Hash}_i = \text{SHA256}(\text{JSON}(\text{Entry}_i) \mathbin{\Vert} \text{Hash}_{i-1})$.<br>• `generate_audit_json()`: Generates structured, machine-readable JSON reports containing the 64-character SHA-256 chain hash.<br>• `generate_audit_txt()`: Formats human-readable audit summaries with visual separators.<br>• `save_audit_file()`: Persists audit reports to disk with ISO-8601 UTC timestamps. |
| [`pqc_agent/cli.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/pqc_agent/cli.py) | **DevSecOps Command-Line Interface (Headless CI/CD Scanner).**<br>• Enables running the scanner in automated headless environments (Docker, GitHub Actions, Jenkins).<br>• Evaluates codebases against `pqc_config.yaml` policy thresholds.<br>• Formats CLI tables of detected vulnerabilities with severity and confidence metrics.<br>• Returns exit codes: `0` (clean), `1` (policy threshold violation), `2` (syntax/file error).<br>• Saves JSON/TXT audit trails to `--output-json` and `--output-txt`. |

---

### 3. Test Bench & Sample Files (`sample_files/`)

| File Name | Exact Role & Description |
| :--- | :--- |
| [`sample_files/vulnerable_python.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/sample_files/vulnerable_python.py) | **Intentionally Vulnerable Python Cryptography Benchmark.**<br>• Contains intentional legacy cryptographic calls for validation: RSA-2048 keypair generation, ECDSA P-256 signing, DSA key generation, DES encryption, 3DES encryption, MD5 hashing, SHA-1 hashing, and AES-128 CBC. |
| [`sample_files/VulnerableJava.java`](file:///c:/Users/User/hackathon-cybersecurity-agents/sample_files/VulnerableJava.java) | **Intentionally Vulnerable Java Cryptography Benchmark.**<br>• Contains intentional legacy Java JCA/JCE implementations: `KeyPairGenerator.getInstance("RSA")`, `Cipher.getInstance("RSA/ECB/PKCS1Padding")`, `Signature.getInstance("SHA256withECDSA")`, DSA, DES, MD5, SHA-1, and Diffie-Hellman (`DH`). |

---

### 4. Automated Testing & Verification

| File Name | Exact Role & Description |
| :--- | :--- |
| [`test_pqc_agent.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/test_pqc_agent.py) | **Unit & Tool Integration Verification Suite.**<br>• Tests module imports, Python AST scanner detection (finds 21 vulnerabilities in sample), Java regex scanner (finds 12 vulnerabilities in sample), NIST PQC patch generation, SHA-256 chain hash integrity, and LangGraph compilation. |
| [`test_graph_e2e.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/test_graph_e2e.py) | **End-to-End LangGraph HITL State Machine Verification.**<br>• Simulates the complete runtime lifecycle: streams state up to the `human_approval` node, asserts that execution pauses at `interrupt()`, and resumes execution using `Command(resume=...)`, verifying the final sealed audit trail. |

---

### 5. DevSecOps, Containerization & CI/CD

| File Name | Exact Role & Description |
| :--- | :--- |
| [`.github/workflows/ci.yml`](file:///c:/Users/User/hackathon-cybersecurity-agents/.github/workflows/ci.yml) | **Continuous Integration Matrix Workflow.**<br>• Triggers on push and pull requests to `main`.<br>• Tests across Python 3.11 and 3.12.<br>• Executes syntax linting with `flake8`, unit tests (`test_pqc_agent.py`), and E2E state machine verification (`test_graph_e2e.py`). |
| [`.github/workflows/security-scan.yml`](file:///c:/Users/User/hackathon-cybersecurity-agents/.github/workflows/security-scan.yml) | **DevSecOps Security Gate Workflow.**<br>• Runs static application security testing (SAST) with `bandit`.<br>• Audits dependencies for known CVEs using `pip-audit`.<br>• Runs `pqc_agent.cli` against sample files and uploads the resulting SHA-256 audit log as a GitHub Actions pipeline artifact. |
| [`Dockerfile`](file:///c:/Users/User/hackathon-cybersecurity-agents/Dockerfile) | **Hardened Production Multi-Stage Container Definition.**<br>• Stage 1 (Builder): Installs build tools and compiles Python wheels.<br>• Stage 2 (Runtime): Minimal Debian-slim base, creates an unprivileged user (`pqcuser`, UID `10001`), drops root privileges, configures healthcheck (`/_stcore/health`), and serves Streamlit on port 8501. |
| [`docker-compose.yml`](file:///c:/Users/User/hackathon-cybersecurity-agents/docker-compose.yml) | **Docker Compose Service Orchestration.**<br>• Configures port mapping (`8501:8501`), environment variables, persistent volumes for `audit_outputs/`, resource quotas (2.0 CPUs, 2GB RAM), and security option `no-new-privileges:true`. |
| [`.dockerignore`](file:///c:/Users/User/hackathon-cybersecurity-agents/.dockerignore) | **Docker Context Exclusion.**<br>• Excludes Git history, test files, virtual environments, and secrets from being copied into the container image during build. |

---

### 6. Architectural Blueprints & PDF Generation

| File Name | Exact Role & Description |
| :--- | :--- |
| [`devsecops_ai_architecture_blueprint.md`](file:///c:/Users/User/hackathon-cybersecurity-agents/devsecops_ai_architecture_blueprint.md) | **Production Technical Blueprint (Markdown).**<br>• Complete technical architectural reference covering the 4-tier architecture, Shor/Grover threat model, LangGraph pipeline, DevSecOps gates, SHA-256 hash chaining, and regulatory compliance mapping (NIST SP 800-53, SOC 2, CNSA 2.0). |
| [`generate_pdf.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/generate_pdf.py) | **Multi-Page Architecture Blueprint PDF Compiler.**<br>• Uses Microsoft Edge in headless mode to convert the complete architectural blueprint into a vector-rendered PDF document ([`PQC_Secure_Code_Reviewer_Blueprint.pdf`](file:///c:/Users/User/hackathon-cybersecurity-agents/PQC_Secure_Code_Reviewer_Blueprint.pdf)). |
| [`generate_one_page_pdf.py`](file:///c:/Users/User/hackathon-cybersecurity-agents/generate_one_page_pdf.py) | **Executive 1-Page Summary PDF Compiler.**<br>• Generates an executive, high-density single-page A4 summary PDF ([`PQC_Framework_Executive_Summary.pdf`](file:///c:/Users/User/hackathon-cybersecurity-agents/PQC_Framework_Executive_Summary.pdf)) designed specifically for academic supervisor review. |
| [`PQC_Secure_Code_Reviewer_Blueprint.pdf`](file:///c:/Users/User/hackathon-cybersecurity-agents/PQC_Secure_Code_Reviewer_Blueprint.pdf) | **Multi-Page Architectural Blueprint Document.**<br>• Rendered PDF document detailing system architecture, mathematical threat models, and compliance mappings. |
| [`PQC_Framework_Executive_Summary.pdf`](file:///c:/Users/User/hackathon-cybersecurity-agents/PQC_Framework_Executive_Summary.pdf) | **Executive 1-Page Summary PDF.**<br>• Single-page executive summary PDF with problem statement, workflow diagram, NIST migration matrix, and DevSecOps verification. |
| [`PQC_Secure_Code_Reviewer_Blueprint.html`](file:///c:/Users/User/hackathon-cybersecurity-agents/PQC_Secure_Code_Reviewer_Blueprint.html) | **HTML Template for Multi-Page Blueprint.**<br>• Source HTML/CSS used by `generate_pdf.py` to compile the multi-page PDF. |
| [`PQC_Framework_Executive_Summary.html`](file:///c:/Users/User/hackathon-cybersecurity-agents/PQC_Framework_Executive_Summary.html) | **HTML Template for Single-Page Summary.**<br>• Source HTML/CSS used by `generate_one_page_pdf.py` to compile the single-page PDF. |

---

### 7. Generated Outputs & Runtime Directories

| Directory Name | Exact Role & Description |
| :--- | :--- |
| [`audit_outputs/`](file:///c:/Users/User/hackathon-cybersecurity-agents/audit_outputs) | **Persistent Audit Trail Output Store.**<br>• Stores machine-readable (`.json`) and human-readable (`.txt`) audit trail logs generated by the Streamlit dashboard or CLI scans, sealed with SHA-256 chain hashes. |
| [`.streamlit/`](file:///c:/Users/User/hackathon-cybersecurity-agents/.streamlit) | **Streamlit App Configuration Directory.**<br>• Contains `config.toml` configuring dark theme colors (`#0a0e17`, `#6366f1`), server port `8501`, headless mode, and disabling telemetry. |

---

## 🔄 How the Files Interact (Runtime Execution Flow)

### Workflow A: Interactive Web Review (`app.py`)
```
1. User uploads file or selects sample in app.py
2. app.py passes source code to pqc_agent.graph.build_graph()
3. graph.py runs node_ingest (validates file, logs genesis hash via audit.py)
4. graph.py runs node_scan (invokes code_scanner_tool in tools.py using AST/Regex)
5. graph.py runs node_investigate:
     ├── Calls pqc_patch_generator_tool in tools.py (generates ML-KEM/ML-DSA diffs)
     └── Invokes LLM using prompts.py (generates Chain-of-Thought reasoning)
6. graph.py reaches node_human_approval and PAUSES at interrupt()
7. app.py displays findings, CoT reasoning, and diffs to user
8. Human clicks "Approve Patches" or "Reject Patches" in app.py
9. app.py calls graph.stream(Command(resume=...))
10. graph.py unpauses, runs node_finalise, and updates audit.py
11. app.py exports final SHA-256 chain-hashed audit trail to audit_outputs/
```

### Workflow B: DevSecOps Headless CI/CD Pipeline (`pqc_agent/cli.py`)
```
1. CI pipeline or Git pre-commit hook runs: python -m pqc_agent.cli --target src/
2. cli.py reads enterprise policy thresholds from pqc_config.yaml
3. cli.py invokes code_scanner_tool in tools.py across all target files
4. If --generate-patches is set, cli.py invokes pqc_patch_generator_tool in tools.py
5. cli.py calls audit.py to generate a tamper-evident SHA-256 audit log
6. cli.py checks findings against policy threshold:
     ├── Violations found: Returns exit code 1 (Fails CI build)
     └── No violations: Returns exit code 0 (Passes CI build)
```

---

## ⚡ Quick Command Reference

| Action | Command |
| :--- | :--- |
| **Launch Web Dashboard** | `streamlit run app.py` |
| **Run DevSecOps CLI Scan** | `python -m pqc_agent.cli --target sample_files/ --generate-patches` |
| **Run Unit & Integration Tests** | `python test_pqc_agent.py` |
| **Run E2E LangGraph HITL Test** | `python test_graph_e2e.py` |
| **Build & Run with Docker** | `docker compose up -d --build` |
| **Compile Architecture PDF** | `python generate_pdf.py` |
| **Compile 1-Page Summary PDF** | `python generate_one_page_pdf.py` |
