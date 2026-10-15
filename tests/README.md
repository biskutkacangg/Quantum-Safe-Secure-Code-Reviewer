# Automated Test Suites
**Project:** *Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool*

This directory contains the automated test suites verifying the AST scanner, LangGraph state machine, HITL approval gates, and CIA Triad risk scoring.

---

## 🧪 Running the Tests

To run all unit and integration tests across the repository:

```bash
# From workspace root:
python -m unittest discover tests -v
```

Or run individual test modules:

```bash
python -m unittest tests/test_pqc_agent.py -v
python -m unittest tests/test_graph_e2e.py -v
python -m unittest tests/test_cia_triad.py -v
```

---

## 📂 Test Suites Overview

| File | Purpose | Key Test Cases |
| :--- | :--- | :--- |
| **`test_pqc_agent.py`** | Unit tests for AST & Regex detection engine | Verifies detection of RSA, ECC, DH, MD5, SHA-1; validates AST line identification and NIST PQC migration targets. |
| **`test_graph_e2e.py`** | E2E LangGraph workflow & HITL gating | Tests graph execution, interrupt state at human approval node, and resumption upon user consent. |
| **`test_cia_triad.py`** | Security impact classification | Verifies CIA Triad severity weighting, cryptographic risk scores, and compliance flag accuracy. |
