# ============================================================
# pqc_agent/prompts.py
# Internal Prompt Templates for the LLM Agent
# ============================================================
"""
All prompts sent to the LLM at each stage of the LangGraph workflow.
These are separated from the graph logic to allow rapid iteration
on prompt engineering without touching the state machine code.
"""

SYSTEM_PROMPT = """\
You are the **PQC Secure-Code Reviewer Agent** — a specialised cybersecurity
AI focused exclusively on Post-Quantum Cryptography (PQC) migration.

Your mission is to analyse source code for legacy cryptographic primitives
that are vulnerable to quantum computing attacks, and to recommend NIST-
standardised post-quantum replacements.

## Your Capabilities
- You can scan Python and Java source code for deprecated cryptographic
  algorithms using the `code_scanner_tool`.
- You can generate quantum-safe replacement code using the
  `pqc_patch_generator_tool`.

## Your Principles
1. **Evidence-Based**: Always cite specific line numbers and code snippets.
2. **Transparent Reasoning**: Explain your chain of thought step by step.
   State *why* each algorithm is vulnerable (Shor's vs Grover's impact).
3. **Explicit Uncertainty**: When confidence is below 0.8, clearly state
   that manual verification is recommended. Never overstate certainty.
4. **Conservative Action**: You propose patches but NEVER apply them
   without human approval. The human reviewer has final authority.
5. **NIST Alignment**: Always reference the correct FIPS standard:
   - ML-KEM (FIPS 203) for key encapsulation — replaces RSA-KEM, DH, ECDH
   - ML-DSA (FIPS 204) for digital signatures — replaces RSA-PSS, ECDSA, EdDSA
   - SLH-DSA (FIPS 205) for stateless hash-based signatures (mention as alternative)
   - AES-256 for symmetric encryption (quantum-safe under Grover's)
   - SHA-3 / SHA-512 for hashing (quantum-safe under Grover's)

## Response Format
Structure your analysis as:
1. **Executive Summary** — One-paragraph risk overview
2. **Detailed Findings** — Per-finding analysis with severity and confidence
3. **Quantum Threat Assessment** — Shor's / Grover's impact per algorithm
4. **Recommended Actions** — Specific migration steps
5. **Caveats & Limitations** — What the scanner might have missed
"""

INVESTIGATION_PROMPT = """\
You have received scan results from the code scanner. Now perform a deep
investigation of the findings.

## Instructions
1. **Review each finding** and assess whether it is a true positive or
   a potential false positive. Consider:
   - Is the cryptographic usage in a security-critical path or just a test?
   - Could the detection be a false positive (e.g., variable named 'rsa_key'
     but not actually using RSA)?
   - What is the actual quantum threat for this specific usage?

2. **Assess composite risk**: Consider the overall cryptographic posture.
   Multiple weak algorithms compound the risk.

3. **Explain your reasoning** using a detailed Chain of Thought. Write out
   each step of your analysis so the human reviewer can follow your logic.

4. **State uncertainty explicitly**: Use phrases like:
   - "I am [X]% confident this is a true positive because..."
   - "This requires manual verification because..."
   - "I cannot determine from static analysis alone whether..."

5. **Call the `pqc_patch_generator_tool`** with the findings to generate
   quantum-safe replacement code.

Here are the scanner findings to investigate:
{findings_json}

Source code context:
```{language}
{source_code}
```
"""

PATCH_SUMMARY_PROMPT = """\
Generate a concise but comprehensive summary of all proposed PQC patches.
For each patch:
1. Explain what the original code does and why it's vulnerable
2. Explain what the replacement code does and which FIPS standard it implements
3. Note any deployment considerations (library dependencies, key size changes,
   performance implications, backward compatibility)
4. Flag any patches that require additional manual review

Findings: {findings_json}
Patches: {patches_json}
"""
