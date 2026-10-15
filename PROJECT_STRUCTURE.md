# 📁 Project Structure & Organization Guide
## Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool

This document provides a clean, comprehensive, file-by-file breakdown of the **Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool** repository. All files are organized into dedicated, logical directories for maximum clarity, maintainability, and ease of access.

---

## 🗺️ High-Level Directory Tree

```
Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool/
│
├── pqc_agent/                               # CORE AGENT PYTHON PACKAGE
│   ├── __init__.py                          # Package initialization & public API exports
│   ├── state.py                             # LangGraph state schema & Pydantic data models
│   ├── tools.py                             # AST & Regex scanners + NIST PQC patch generator
│   ├── prompts.py                           # LLM system prompts & investigation guidance
│   ├── graph.py                             # 5-node LangGraph state machine & HITL interrupt
│   ├── audit.py                             # Cryptographic tamper-evident SHA-256 audit logger
│   └── cli.py                               # DevSecOps headless CLI scanner for CI/CD pipelines
│
├── reports/                                 # ACTIVE RESEARCH DELIVERABLES & PDF REPORTS
│   ├── README.md                            # Official catalog of active deliverables
│   ├── PQC_Model_Parameters_and_Results_Paper_Comparison.pdf    # 4-page SOTA Literature Review (Google Scholar 2020–2025)
│   ├── PQC_Vulnerabilities_and_Replacements_Catalog.pdf         # Complete Inventory of Deprecated Algorithms & NIST Targets
│   └── html/                                # HTML SOURCE & PREVIEW TEMPLATES (Isolated to eliminate clutter)
│       ├── PQC_Model_Parameters_and_Results_Paper_Comparison.html
│       └── PQC_Vulnerabilities_and_Replacements_Catalog.html
│
├── scripts/                                 # REPORT BUILD & GENERATION AUTOMATION
│   ├── README.md                            # Documentation on running compiler scripts
│   ├── generate_all_reports.py              # Master script: 1-click rebuild of active deliverables
│   ├── generate_papers_comparison_pdf.py    # Headless Edge compiler for Literature Review PDF
│   └── generate_catalog_pdf.py              # Headless Edge compiler for Deprecated Algorithms Catalog PDF
│
├── tests/                                   # AUTOMATED TEST SUITES
│   ├── __init__.py                          # Test package initializer
│   ├── test_pqc_agent.py                    # Static AST/Regex scanner & patch generation tests
│   ├── test_graph_e2e.py                    # End-to-end LangGraph HITL interrupt & resume tests
│   └── test_cia_triad.py                    # CIA Triad impact classification tests
│
├── docs/                                    # ARCHITECTURAL DOCUMENTATION & BLUEPRINTS
│   └── devsecops_ai_architecture_blueprint.md# Enterprise DevSecOps & AI architecture specification
│
├── sample_files/                            # TEST BENCH / VULNERABLE CODE SAMPLES
│   ├── vulnerable_python.py                 # Intentionally vulnerable Python crypto sample (21 flaws)
│   └── VulnerableJava.java                  # Intentionally vulnerable Java crypto sample (12 flaws)
│
├── audit_outputs/                           # PERSISTED RUNTIME AUDIT TRAILS (JSON & TXT)
│
├── .github/                                 # CI/CD WORKFLOWS
│   └── workflows/
│       ├── ci.yml                           # GitHub Actions build & test matrix workflow
│       └── security-scan.yml                # SAST, SCA & cryptographic compliance pipeline
│
├── web/                                     # MODERN CYBER SOC WEB DASHBOARD
│   ├── index.html                           # Single-page application HTML5 interface
│   ├── styles.css                           # Obsidian dark theme, glassmorphism, glowing badges
│   └── app.js                               # Monaco diff viewer, LangGraph circuit & audio FX
│
├── server.py                                # FASTAPI HIGH-PERFORMANCE CYBER SOC SERVER (Port 8000)
├── run_app.bat                              # 1-CLICK LAUNCHER FOR CYBER SOC DASHBOARD (Port 8000)
├── run_streamlit.bat                        # LEGACY STREAMLIT LAUNCHER (Port 8501)
├── run_interactive_poster.bat               # INTERACTIVE POSTER BROWSER LAUNCHER
├── interactive_poster.html                  # Standalone interactive digital research poster
├── app.py                                   # Legacy Streamlit Dashboard implementation
├── requirements.txt                         # Production Python dependencies manifest
├── pqc_config.yaml                          # Cryptographic policy thresholds & PQC targets
├── .env / .env.example                      # LLM API keys & provider configuration
├── Dockerfile & docker-compose.yml          # Hardened production container definitions
├── README.md                                # Master repository documentation & quickstart guide
└── PROJECT_STRUCTURE.md                     # THIS FILE — Directory structure reference
```

---

## 📂 Detailed Directory & Component Breakdown

### 1. `pqc_agent/` — Core Engine Package
Contains the complete business logic of the tool:
* **`state.py`**: Pydantic data models for findings, patches, and the unified LangGraph state.
* **`tools.py`**: Deterministic Python AST scanner and Java regex scanner mapping against `LEGACY_CRYPTO_DB`, plus the `liboqs` / Bouncy Castle code generator.
* **`prompts.py`**: Cognitive prompts guiding the LLM in Chain-of-Thought investigation and risk explanation.
* **`graph.py`**: The LangGraph state machine orchestrating the 5 nodes with the mandatory Human-in-the-Loop `interrupt()`.
* **`audit.py`**: Cryptographic blockchain-style SHA-256 chained hash logger guaranteeing non-repudiation.
* **`cli.py`**: Headless CLI tool for CI/CD pipelines (returns exit code 1 on policy failure).

### 2. `reports/` — Research Deliverables & PDFs
Contains the active publication-grade deliverables ready for immediate review and academic submission:
* **`PQC_Model_Parameters_and_Results_Paper_Comparison.pdf`**: 4-page comparative literature review comparing our tool against 6 Google Scholar papers (2020–2025), anchored on **Masood & Vargas Martin (SECRYPT 2025)**. *(System Parameters, Empirical Benchmark Results & Literature Review)*.
* **`PQC_Vulnerabilities_and_Replacements_Catalog.pdf`**: Complete reference catalog of 14 vulnerable cryptographic primitives and their post-quantum replacements. *(Complete Inventory of Deprecated Algorithms • NIST FIPS 203 / 204 Migration Targets)*.

### 3. `scripts/` — Automation & PDF Compilers
Houses the automated headless Microsoft Edge generation scripts:
* **`generate_all_reports.py`**: 1-click builder that compiles both active reports and synchronizes them to `C:\Users\User\Downloads\`.
* **`generate_papers_comparison_pdf.py`**: Compiles the 4-page comparative literature review.
* **`generate_catalog_pdf.py`**: Compiles the complete inventory catalog.

### 4. `tests/` — Test Suites
Automated unit and integration verification:
* **`test_pqc_agent.py`**: Validates AST visitor, scanner rules, patch synthesis, and SHA-256 hash chains.
* **`test_graph_e2e.py`**: Exercises the full LangGraph state machine from ingestion, through HITL interruption, to resume and final audit closure.
* **`test_cia_triad.py`**: Validates Confidentiality (HNDL), Integrity, and Availability risk mapping.

### 5. Application Interfaces & Root Launchers
* **`server.py`**: The FastAPI high-performance backend serving the modern Cyber SOC interface and LangGraph REST endpoints.
* **`web/`**: Modern Cyber SOC Web UI featuring obsidian dark theme, Monaco side-by-side diff editor, and live state flow circuit.
* **`run_app.bat`**: 1-click Windows launcher for the modern Cyber SOC Dashboard (`http://localhost:8000`).
* **`run_streamlit.bat`**: Optional Windows launcher for the legacy Streamlit interface (`http://localhost:8501`).
* **`run_interactive_poster.bat`**: Direct launcher for the standalone interactive research poster.
* **`requirements.txt`**, **`pqc_config.yaml`**, **`Dockerfile`**, and **`README.md`**.
