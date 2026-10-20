# 🛡️ Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool
## Production DevSecOps & AI Systems Architectural Blueprint

> **System Classification**: Agentic Cyber Defence System (Track 1)  
> **Target Standard Alignment**: NIST FIPS 203 (ML-KEM), NIST FIPS 204 (ML-DSA), NIST FIPS 202 (SHA-3), NSA CNSA 2.0  
> **Security Baseline**: Non-repudiation, Zero Trust Code Modification, Tamper-Evident SHA-256 Chained Auditing

---

## 1. Executive Architectural Summary

The **Post-Quantum Cryptography (PQC) Secure-Code Reviewer** is an enterprise-grade agentic DevSecOps system designed to address the systemic threat of **"Harvest Now, Decrypt Later" (HNDL)** attacks. 

Traditional static application security testing (SAST) tools lack mathematical contextual awareness: they cannot differentiate between Shor-vulnerable asymmetric schemes and Grover-affected symmetric ciphers, cannot generate validated quantum-resistant replacement code, and offer no cryptographic provenance for automated changes. 

This platform integrates:
1. **Deterministic Multi-Language Static Analysis**: AST (Python) and regex syntax trees (Java).
2. **Autonomous Chain-of-Thought (CoT) Reasoning**: Powered by an LLM with explicit uncertainty quantification.
3. **Hard Human-in-the-Loop (HITL) Gate**: Enforced via LangGraph's native stateful `interrupt()` and `Command(resume=...)` primitives.
4. **Cryptographic Tamper-Evident Auditing**: A blockchain-style SHA-256 hash chain providing non-repudiation across all decisions.
5. **Multi-Modal Operation Interfaces**: A high-performance **Cyber SOC Web Dashboard** powered by FastAPI (Port 8000) with Monaco side-by-side patch diffing and dual-portal RBAC (Reviewer Portal & Admin SOC Console), a headless CLI engine for automated CI/CD pipeline gates, and an optional legacy Streamlit interface (Port 8501).

---

## 2. Threat Modeling & Cryptographic Risk Matrix

### 2.1 Quantum Adversary Threat Model
* **Harvest Now, Decrypt Later (HNDL)**: Adversaries passively record encrypted network traffic and code repositories today. Once a Cryptographically Relevant Quantum Computer (CRQC) becomes viable, all data protected by classical public key cryptography will be retroactively decrypted.
* **Shor's Algorithm Impact**: Solves integer factorization and discrete logarithms in polynomial time $\mathcal{O}((\log N)^3)$. It completely collapses RSA, DSA, ECDSA, DH, and ECDH.
* **Grover's Algorithm Impact**: Provides a quadratic speedup for unstructured database search $\mathcal{O}(\sqrt{N})$. Symmetric encryption (AES) and hashing (SHA-256) effectively lose half their key length. AES-128 drops to 64-bit security (insufficient); AES-256 retains 128-bit quantum security (fully secure).

```mermaid
graph TD
    subgraph "Legacy Cryptography"
        RSA["RSA (2048/4096-bit)"]
        ECC["ECC (ECDSA / ECDH)"]
        DSA["DSA / Diffie-Hellman"]
        AES128["AES-128 / DES / 3DES"]
        MD5["MD5 / SHA-1"]
    end

    subgraph "Quantum Attack Vector"
        SHOR["Shor's Algorithm<br/>(Polynomial Time $\mathcal{O}(n^3)$)"]
        GROVER["Grover's Algorithm<br/>(Quadratic Speedup $\mathcal{O}(\sqrt{N})$)"]
    end

    subgraph "NIST Post-Quantum Replacement"
        MLKEM["ML-KEM-768 / 1024<br/>(FIPS 203 — Module Lattice KEM)"]
        MLDSA["ML-DSA-65 / 87<br/>(FIPS 204 — Module Lattice DSA)"]
        AES256["AES-256-GCM<br/>(NIST SP 800-38D)"]
        SHA3["SHA-3-256 / SHA-512<br/>(FIPS 202)"]
    end

    RSA -->|Broken| SHOR
    ECC -->|Broken| SHOR
    DSA -->|Broken| SHOR
    AES128 -->|Halved Security| GROVER
    MD5 -->|Classical Collisions + Grover| GROVER

    SHOR -->|Migrate to| MLKEM
    SHOR -->|Migrate to| MLDSA
    GROVER -->|Harden with| AES256
    GROVER -->|Harden with| SHA3
```

---

## 3. Four-Tier Production System Architecture

```mermaid
graph TB
    subgraph "Tier 1: Ingestion & Presentation"
        SOC["Cyber SOC Web UI (Port 8000)<br/>FastAPI + Monaco Diff Editor"]
        RBAC["Dual RBAC Portals<br/>Reviewer & Admin SOC Console"]
        CLI["Headless DevSecOps CLI<br/>(pqc_agent.cli)"]
        HOOK["Git Pre-Commit Hook<br/>(.pre-commit-config.yaml)"]
        LEGACY["Legacy Streamlit UI<br/>(Port 8501)"]
    end

    subgraph "Tier 2: Orchestration & State Machine"
        LG["LangGraph State Engine"]
        MEM["Stateful Checkpointer<br/>(MemorySaver / SQLite / Postgres)"]
        HITL["Human-in-the-Loop Gate<br/>(interrupt() / Command(resume=...))"]
    end

    subgraph "Tier 3: Analysis & Patch Synthesis"
        SCAN["AST & Regex Static Scanner<br/>(code_scanner_tool)"]
        LLM["AI Reasoning Engine<br/>(Gemini 1.5 Pro with CoT Fallback)"]
        PATCH["PQC Patch Synthesizer<br/>(pqc_patch_generator_tool)"]
    end

    subgraph "Tier 4: Provenance & Governance"
        AUDIT["Tamper-Evident Audit Generator<br/>(audit.py)"]
        CHAIN["SHA-256 Recursive Hash Chain<br/>(Prev_Hash + Current_Entry)"]
        OUT["JSON & TXT Audit Reports<br/>(audit_outputs/)"]
    end

    SOC --> LG
    RBAC --> LG
    LEGACY --> LG
    CLI --> LG
    HOOK --> CLI

    LG <--> MEM
    LG --> SCAN
    LG --> LLM
    LG --> PATCH
    LG --> HITL
    HITL --> AUDIT
    AUDIT --> CHAIN
    CHAIN --> OUT
```

---

## 4. LangGraph Five-Node State Pipeline

The core execution engine is a strictly bounded Directed Acyclic Graph (DAG) with five states:

```
  ┌──────────┐      ┌──────────┐      ┌───────────────┐
  │  INGEST  │ ───▶ │   SCAN   │ ───▶ │  INVESTIGATE  │
  └──────────┘      └──────────┘      └───────┬───────┘
                                              │
                                              ▼
                                    ┌───────────────────┐
                                    │  HUMAN APPROVAL   │ ◀── [interrupt()]
                                    │    (HITL Gate)    │
                                    └─────────┬─────────┘
                                              │ [Command(resume=...)]
                                              ▼
                                    ┌───────────────────┐
                                    │     FINALISE      │ ───▶ [END]
                                    └───────────────────┘
```

1. **INGEST**: Validates file integrity, detects programming language (`.py`, `.java`), initializes state payload, and computes the genesis audit hash block.
2. **SCAN**: Pure deterministic static code scan using Abstract Syntax Tree inspection for Python (`ast.parse`) and regex pattern sets for Java. Assigns line numbers, code snippets, and confidence metrics ($0.95$ for explicit imports, $0.85$ for call sites, $0.75$ for regex).
3. **INVESTIVATE**: Analyzes flagged primitives using Chain of Thought. Generates NIST-standardized replacement patches. Evaluates whether findings are in test fixtures or security-critical paths. If the LLM provider is unavailable, falls back gracefully to a deterministic rule engine without throwing uncaught exceptions.
4. **HUMAN APPROVAL (HITL Gate)**: Halts execution via LangGraph's `interrupt()` primitive. Surfaces the code diff, CoT explanation, and uncertainty notes to the reviewer. Resumes **only** when a signed decision (`approved` or `rejected`) is provided via `Command(resume=...)`.
5. **FINALISE**: Seals the proposed patches as "ready to apply" or "rejected", generates the final SHA-256 chain hash block, and writes immutable JSON/TXT audit reports.

---

## 5. DevSecOps CI/CD Integration & Shift-Left Gates

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant Git as Git Pre-Commit Hook
    participant CI as GitHub Actions CI
    participant PQC as PQC Agent CLI
    participant Reviewer as Security Architect
    participant Repo as Remote Repository

    Dev->>Git: git commit (code with RSA-2048)
    Git->>PQC: Execute pqc-review --fail-on CRITICAL
    alt Policy Violated
        PQC-->>Git: Exit Code 1 (Policy Violation)
        Git-->>Dev: Commit Blocked: Deprecated RSA detected
    else Policy Allowed
        Git-->>Dev: Commit Accepted
    end

    Dev->>Repo: git push origin feature-branch
    Repo->>CI: Trigger Security Workflow
    CI->>PQC: Run headless scan on all changed files
    PQC->>CI: Generate audit_outputs/ci_pqc_audit.json
    CI->>Reviewer: Surface PQC Security Gate in PR checks
    Reviewer->>Repo: Approve or Reject migration diff
```

### DevSecOps CLI Exit Code Standards:
* `0`: **Clean** — No policy violations found. Code complies with PQC standard.
* `1`: **Policy Violation** — Deprecated cryptographic algorithm detected at or above configured severity threshold (`fail_on_severity: CRITICAL`). Blocks pipeline build.
* `2`: **Execution Error** — Malformed configuration, invalid target directory, or unparseable source file.

---

## 6. Cryptographic Tamper-Evident Hash Chaining

To guarantee compliance with SOC 2 Type II (Trust Services Criteria) and NIST SP 800-53 (AU-10 Non-repudiation), each audit record is cryptographically linked to its predecessor using SHA-256:

$$\text{ChainHash}_0 = \text{SHA256}(\text{"0"} \times 64)$$
$$\text{ChainHash}_i = \text{SHA256}(\text{CanonicalJSON}(\text{Entry}_i) \mathbin{\Vert} \text{ChainHash}_{i-1})$$

```python
def _compute_chain_hash(entries: list[dict]) -> str:
    prev_hash = "0" * 64  # Genesis
    for entry in entries:
        payload = json.dumps(entry, sort_keys=True) + prev_hash
        prev_hash = hashlib.sha256(payload.encode()).hexdigest()
    return prev_hash
```

If an adversary alters any historical finding, severity level, or human decision timestamp, the calculated chain hash completely diverges, proving tampering immediately during third-party audit verification.

---

## 7. Compliance & Regulatory Standards Mapping

| Standard | Control ID | Control Name | PQC Reviewer Implementation |
| :--- | :--- | :--- | :--- |
| **NIST SP 800-53 Rev. 5** | `SC-13` | Cryptographic Protection | Detects sub-128-bit quantum primitives and guides migration to FIPS 203/204. |
| **NIST SP 800-53 Rev. 5** | `AU-2` | Event Logging | Automatically logs scan start, findings, LLM reasoning, and decisions. |
| **NIST SP 800-53 Rev. 5** | `AU-10` | Non-Repudiation | SHA-256 chain hashing guarantees that human approval events cannot be altered or denied. |
| **SOC 2 Type II** | `CC6.1` | Logical Access Security | Enforces strict Human-in-the-Loop review before cryptographic changes are authorized. |
| **SOC 2 Type II** | `CC7.1` | Vulnerability Management | Continuous scanning of code repositories via pre-commit hooks and CI/CD pipelines. |
| **NSA CNSA 2.0** | Timeline | PQC Migration Mandate | Supports transition planning to ML-KEM and ML-DSA before the 2030–2033 national deadlines. |
