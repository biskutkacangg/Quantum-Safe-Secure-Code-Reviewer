# ============================================================
# pqc_agent/tools.py
# Custom LangGraph Tools — Code Scanner & PQC Patch Generator
# ============================================================
"""
Production-grade tool implementations that are bound to the LLM via
LangGraph's ToolNode.  Each tool is a pure function decorated with
@tool so that the agent can invoke it by name.

Tool 1 — code_scanner_tool
    Performs AST-based (Python) and regex-based (Java / fallback)
    static analysis to detect legacy cryptographic primitives.

Tool 2 — pqc_patch_generator_tool
    Rewrites flagged legacy code blocks with NIST-standardised
    post-quantum equivalents (ML-KEM for key exchange, ML-DSA
    for digital signatures).
"""

from __future__ import annotations

import ast
import json
import re
import textwrap
import uuid
from typing import Any

from langchain_core.tools import tool

# ════════════════════════════════════════════════════════════════
# ░░░ KNOWLEDGE BASE — Legacy → PQC Mapping ░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

# Canonical mapping of deprecated algorithms to their properties
LEGACY_CRYPTO_DB: dict[str, dict[str, Any]] = {
    # ── Key Exchange / Encapsulation ──
    "RSA": {
        "category": "key_exchange",
        "severity": "CRITICAL",
        "quantum_threat": (
            "Shor's algorithm can factor RSA moduli in polynomial time on a "
            "cryptographically-relevant quantum computer (CRQC), completely "
            "breaking RSA key exchange and encryption."
        ),
        "pqc_replacement": "ML-KEM-768",
        "fips_standard": "FIPS 203",
    },
    "DH": {
        "category": "key_exchange",
        "severity": "CRITICAL",
        "quantum_threat": (
            "Diffie-Hellman key exchange relies on the discrete logarithm "
            "problem, which is solvable in polynomial time by Shor's algorithm."
        ),
        "pqc_replacement": "ML-KEM-768",
        "fips_standard": "FIPS 203",
    },
    "ECDH": {
        "category": "key_exchange",
        "severity": "CRITICAL",
        "quantum_threat": (
            "Elliptic Curve Diffie-Hellman is vulnerable to Shor's algorithm "
            "applied to the elliptic curve discrete logarithm problem (ECDLP)."
        ),
        "pqc_replacement": "ML-KEM-768",
        "fips_standard": "FIPS 203",
    },
    # ── Digital Signatures ──
    "ECDSA": {
        "category": "digital_signature",
        "severity": "CRITICAL",
        "quantum_threat": (
            "ECDSA relies on ECDLP; Shor's algorithm breaks it entirely. "
            "Signature forgery becomes trivial on a CRQC."
        ),
        "pqc_replacement": "ML-DSA-65",
        "fips_standard": "FIPS 204",
    },
    "DSA": {
        "category": "digital_signature",
        "severity": "CRITICAL",
        "quantum_threat": (
            "DSA depends on the discrete logarithm problem, broken by Shor's."
        ),
        "pqc_replacement": "ML-DSA-65",
        "fips_standard": "FIPS 204",
    },
    "EdDSA": {
        "category": "digital_signature",
        "severity": "HIGH",
        "quantum_threat": (
            "EdDSA (Ed25519/Ed448) uses elliptic curves and is vulnerable to "
            "quantum attack via Shor's algorithm, despite being modern."
        ),
        "pqc_replacement": "ML-DSA-65",
        "fips_standard": "FIPS 204",
    },
    "ECC": {
        "category": "digital_signature",
        "severity": "CRITICAL",
        "quantum_threat": (
            "Generic ECC operations (key generation, signing) are broken by "
            "Shor's algorithm applied to the ECDLP."
        ),
        "pqc_replacement": "ML-DSA-65",
        "fips_standard": "FIPS 204",
    },
    # ── Symmetric / Hashing (reduced severity — Grover only) ──
    "AES-128": {
        "category": "symmetric_encryption",
        "severity": "MEDIUM",
        "quantum_threat": (
            "Grover's algorithm halves the effective key length. AES-128 "
            "offers only 64-bit quantum security — upgrade to AES-256."
        ),
        "pqc_replacement": "AES-256-GCM",
        "fips_standard": "NIST SP 800-38D",
    },
    "DES": {
        "category": "symmetric_encryption",
        "severity": "CRITICAL",
        "quantum_threat": (
            "DES is already broken classically (56-bit key). Grover's reduces "
            "brute force to ~2^28 operations."
        ),
        "pqc_replacement": "AES-256-GCM",
        "fips_standard": "NIST SP 800-38D",
    },
    "3DES": {
        "category": "symmetric_encryption",
        "severity": "HIGH",
        "quantum_threat": (
            "Triple-DES has a 112-bit effective key length. Grover's halves it "
            "to ~56 bits — inadequate for long-term security."
        ),
        "pqc_replacement": "AES-256-GCM",
        "fips_standard": "NIST SP 800-38D",
    },
    "MD5": {
        "category": "hashing",
        "severity": "CRITICAL",
        "quantum_threat": (
            "MD5 is already broken classically (collision attacks). Grover's "
            "further halves preimage resistance to 64 bits."
        ),
        "pqc_replacement": "SHA-3-256 or SHA-512",
        "fips_standard": "FIPS 202",
    },
    "SHA1": {
        "category": "hashing",
        "severity": "HIGH",
        "quantum_threat": (
            "SHA-1 has known collision attacks. Grover's halves preimage "
            "resistance to 80 bits — below recommended thresholds."
        ),
        "pqc_replacement": "SHA-3-256 or SHA-512",
        "fips_standard": "FIPS 202",
    },
    "Blowfish": {
        "category": "symmetric_encryption",
        "severity": "HIGH",
        "quantum_threat": (
            "Blowfish has a 64-bit block size (birthday attacks at 2^32 blocks) "
            "and is deprecated. Grover's further weakens it."
        ),
        "pqc_replacement": "AES-256-GCM",
        "fips_standard": "NIST SP 800-38D",
    },
    "RC4": {
        "category": "symmetric_encryption",
        "severity": "CRITICAL",
        "quantum_threat": (
            "RC4 is cryptographically broken classically. Must be replaced "
            "regardless of quantum considerations."
        ),
        "pqc_replacement": "AES-256-GCM / ChaCha20-Poly1305",
        "fips_standard": "NIST SP 800-38D",
    },
}

# ════════════════════════════════════════════════════════════════
# ░░░ DETECTION PATTERNS ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

# ── Python-specific import / call patterns ──
PYTHON_CRYPTO_PATTERNS: list[dict[str, Any]] = [
    # --- RSA ---
    {
        "algorithm": "RSA",
        "import_modules": [
            "cryptography.hazmat.primitives.asymmetric.rsa",
            "Crypto.PublicKey.RSA",
            "Cryptodome.PublicKey.RSA",
        ],
        "function_calls": [
            r"rsa\.generate_private_key",
            r"RSA\.generate",
            r"RSA\.import_key",
            r"PKCS1_OAEP\.new",
            r"PKCS1_v1_5\.new",
        ],
    },
    # --- ECDSA / ECC ---
    {
        "algorithm": "ECDSA",
        "import_modules": [
            "cryptography.hazmat.primitives.asymmetric.ec",
            "Crypto.PublicKey.ECC",
            "Cryptodome.PublicKey.ECC",
            "ecdsa",
        ],
        "function_calls": [
            r"ec\.generate_private_key",
            r"ec\.ECDSA",
            r"ec\.ECDH",
            r"ECC\.generate",
            r"ECDSA\.from_string",
            r"SigningKey\(",
            r"VerifyingKey\(",
        ],
    },
    # --- DSA ---
    {
        "algorithm": "DSA",
        "import_modules": [
            "cryptography.hazmat.primitives.asymmetric.dsa",
            "Crypto.PublicKey.DSA",
        ],
        "function_calls": [
            r"dsa\.generate_private_key",
            r"DSA\.generate",
        ],
    },
    # --- DH ---
    {
        "algorithm": "DH",
        "import_modules": [
            "cryptography.hazmat.primitives.asymmetric.dh",
        ],
        "function_calls": [
            r"dh\.generate_parameters",
            r"generate_dh_parameters",
        ],
    },
    # --- DES / 3DES ---
    {
        "algorithm": "DES",
        "import_modules": [
            "Crypto.Cipher.DES",
            "Cryptodome.Cipher.DES",
        ],
        "function_calls": [
            r"DES\.new\(",
            r"DES3\.new\(",
            r"algorithms\.TripleDES",
        ],
    },
    {
        "algorithm": "3DES",
        "import_modules": [
            "Crypto.Cipher.DES3",
            "Cryptodome.Cipher.DES3",
            "cryptography.hazmat.primitives.ciphers.algorithms.TripleDES",
        ],
        "function_calls": [
            r"DES3\.new\(",
            r"TripleDES\(",
        ],
    },
    # --- Blowfish ---
    {
        "algorithm": "Blowfish",
        "import_modules": [
            "Crypto.Cipher.Blowfish",
            "Cryptodome.Cipher.Blowfish",
            "cryptography.hazmat.primitives.ciphers.algorithms.Blowfish",
        ],
        "function_calls": [
            r"Blowfish\.new\(",
            r"Blowfish\(",
        ],
    },
    # --- RC4 ---
    {
        "algorithm": "RC4",
        "import_modules": [
            "Crypto.Cipher.ARC4",
            "Cryptodome.Cipher.ARC4",
        ],
        "function_calls": [
            r"ARC4\.new\(",
        ],
    },
    # --- MD5 ---
    {
        "algorithm": "MD5",
        "import_modules": [],
        "function_calls": [
            r"hashlib\.md5",
            r"MD5\.new\(",
            r"Crypto\.Hash\.MD5",
        ],
    },
    # --- SHA-1 ---
    {
        "algorithm": "SHA1",
        "import_modules": [],
        "function_calls": [
            r"hashlib\.sha1",
            r"SHA\.new\(",
            r"SHA1\.new\(",
            r"Crypto\.Hash\.SHA\b",
        ],
    },
    # --- AES-128 (flag only small key sizes) ---
    {
        "algorithm": "AES-128",
        "import_modules": [],
        "function_calls": [
            r"AES\.new\(.{0,80}(16|AES\.block_size)",
            r"algorithms\.AES\(\s*\w{0,30}\s*\)",
        ],
    },
]

# ── Java regex patterns (no AST — regex only) ──
JAVA_CRYPTO_PATTERNS: list[dict[str, Any]] = [
    {
        "algorithm": "RSA",
        "patterns": [
            r'KeyPairGenerator\.getInstance\(\s*"RSA"',
            r'Cipher\.getInstance\(\s*"RSA',
            r'KeyFactory\.getInstance\(\s*"RSA"',
            r'Signature\.getInstance\(\s*"SHA\d*withRSA"',
        ],
    },
    {
        "algorithm": "ECDSA",
        "patterns": [
            r'KeyPairGenerator\.getInstance\(\s*"EC"',
            r'Signature\.getInstance\(\s*"SHA\d*withECDSA"',
            r'ECGenParameterSpec\(',
            r'KeyAgreement\.getInstance\(\s*"ECDH"',
        ],
    },
    {
        "algorithm": "DSA",
        "patterns": [
            r'KeyPairGenerator\.getInstance\(\s*"DSA"',
            r'Signature\.getInstance\(\s*"SHA\d*withDSA"',
        ],
    },
    {
        "algorithm": "DH",
        "patterns": [
            r'KeyPairGenerator\.getInstance\(\s*"DH"',
            r'KeyAgreement\.getInstance\(\s*"DiffieHellman"',
            r'DHParameterSpec\(',
        ],
    },
    {
        "algorithm": "DES",
        "patterns": [
            r'Cipher\.getInstance\(\s*"DES[/")\s]',
            r'SecretKeyFactory\.getInstance\(\s*"DES"',
        ],
    },
    {
        "algorithm": "3DES",
        "patterns": [
            r'Cipher\.getInstance\(\s*"DESede',
            r'SecretKeyFactory\.getInstance\(\s*"DESede"',
        ],
    },
    {
        "algorithm": "Blowfish",
        "patterns": [
            r'Cipher\.getInstance\(\s*"Blowfish',
        ],
    },
    {
        "algorithm": "RC4",
        "patterns": [
            r'Cipher\.getInstance\(\s*"RC4"',
            r'Cipher\.getInstance\(\s*"ARCFOUR"',
        ],
    },
    {
        "algorithm": "MD5",
        "patterns": [
            r'MessageDigest\.getInstance\(\s*"MD5"',
        ],
    },
    {
        "algorithm": "SHA1",
        "patterns": [
            r'MessageDigest\.getInstance\(\s*"SHA-?1"',
        ],
    },
]


# ════════════════════════════════════════════════════════════════
# ░░░ TOOL 1 — CODE SCANNER ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

class _PythonCryptoVisitor(ast.NodeVisitor):
    """AST visitor that detects legacy cryptographic imports and calls."""

    def __init__(self, source_lines: list[str]) -> None:
        self.source_lines = source_lines
        self.findings: list[dict[str, Any]] = []
        self._import_aliases: dict[str, str] = {}  # alias → full module

    # ── Import tracking ──────────────────────────────────────

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            full_module = alias.name
            local_name = alias.asname or alias.name.split(".")[-1]
            self._import_aliases[local_name] = full_module
            self._check_import(full_module, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        base = node.module or ""
        for alias in node.names:
            full_module = f"{base}.{alias.name}" if base else alias.name
            local_name = alias.asname or alias.name
            self._import_aliases[local_name] = full_module
            self._check_import(full_module, node.lineno)
        self.generic_visit(node)

    def _check_import(self, module: str, lineno: int) -> None:
        for pattern_set in PYTHON_CRYPTO_PATTERNS:
            for target_module in pattern_set["import_modules"]:
                if target_module in module or module in target_module:
                    algo = pattern_set["algorithm"]
                    db_entry = LEGACY_CRYPTO_DB.get(algo, {})
                    snippet = self._get_line(lineno)
                    self.findings.append(
                        {
                            "finding_id": uuid.uuid4().hex[:8],
                            "line_number": lineno,
                            "code_snippet": snippet,
                            "algorithm_detected": algo,
                            "category": db_entry.get("category", "other"),
                            "severity": db_entry.get("severity", "HIGH"),
                            "confidence": 0.95,
                            "rationale": (
                                f"Import of '{module}' indicates usage of "
                                f"{algo}, which is quantum-vulnerable."
                            ),
                            "quantum_threat_level": db_entry.get(
                                "quantum_threat", ""
                            ),
                            "detection_method": "ast_import",
                        }
                    )
                    return  # one match per import is sufficient

    # ── Call-site tracking ───────────────────────────────────

    def visit_Call(self, node: ast.Call) -> None:
        call_str = self._reconstruct_call(node)
        if call_str:
            for pattern_set in PYTHON_CRYPTO_PATTERNS:
                for regex in pattern_set["function_calls"]:
                    if re.search(regex, call_str):
                        algo = pattern_set["algorithm"]
                        db_entry = LEGACY_CRYPTO_DB.get(algo, {})
                        snippet = self._get_line(node.lineno)
                        self.findings.append(
                            {
                                "finding_id": uuid.uuid4().hex[:8],
                                "line_number": node.lineno,
                                "code_snippet": snippet,
                                "algorithm_detected": algo,
                                "category": db_entry.get("category", "other"),
                                "severity": db_entry.get("severity", "HIGH"),
                                "confidence": 0.85,
                                "rationale": (
                                    f"Call to '{call_str}' matches {algo} "
                                    f"usage pattern."
                                ),
                                "quantum_threat_level": db_entry.get(
                                    "quantum_threat", ""
                                ),
                                "detection_method": "ast_call",
                            }
                        )
                        break  # one match per call
        self.generic_visit(node)

    # ── Helpers ──────────────────────────────────────────────

    def _reconstruct_call(self, node: ast.Call) -> str:
        """Best-effort reconstruction of a call expression as a string."""
        try:
            return ast.unparse(node)
        except Exception:
            return ""

    def _get_line(self, lineno: int) -> str:
        idx = lineno - 1
        if 0 <= idx < len(self.source_lines):
            return self.source_lines[idx].rstrip()
        return ""


def _scan_python(source_code: str, file_name: str) -> list[dict]:
    """Run AST + regex scan on Python source code."""
    lines = source_code.splitlines()
    findings: list[dict] = []

    # --- Phase 1: AST walk ---
    try:
        tree = ast.parse(source_code, filename=file_name)
        visitor = _PythonCryptoVisitor(lines)
        visitor.visit(tree)
        findings.extend(visitor.findings)
    except SyntaxError:
        pass  # Fall through to regex-only

    # --- Phase 2: Regex fallback (catches comments, strings, etc.) ---
    for lineno, line in enumerate(lines, start=1):
        for pattern_set in PYTHON_CRYPTO_PATTERNS:
            for regex in pattern_set["function_calls"]:
                if re.search(regex, line):
                    algo = pattern_set["algorithm"]
                    # Deduplicate against AST findings
                    if any(
                        f["line_number"] == lineno
                        and f["algorithm_detected"] == algo
                        for f in findings
                    ):
                        continue
                    db_entry = LEGACY_CRYPTO_DB.get(algo, {})
                    findings.append(
                        {
                            "finding_id": uuid.uuid4().hex[:8],
                            "line_number": lineno,
                            "code_snippet": line.rstrip(),
                            "algorithm_detected": algo,
                            "category": db_entry.get("category", "other"),
                            "severity": db_entry.get("severity", "HIGH"),
                            "confidence": 0.70,
                            "rationale": (
                                f"Regex match for {algo} on line {lineno}. "
                                f"Lower confidence — verify manually."
                            ),
                            "quantum_threat_level": db_entry.get(
                                "quantum_threat", ""
                            ),
                            "detection_method": "regex",
                        }
                    )

    # Enrich every finding with file metadata
    for f in findings:
        f["file_path"] = file_name
        f["language"] = "python"

    return findings


def _scan_java(source_code: str, file_name: str) -> list[dict]:
    """Regex-only scan for Java source code."""
    lines = source_code.splitlines()
    findings: list[dict] = []

    for lineno, line in enumerate(lines, start=1):
        for pattern_set in JAVA_CRYPTO_PATTERNS:
            for regex in pattern_set["patterns"]:
                if re.search(regex, line):
                    algo = pattern_set["algorithm"]
                    if any(
                        f["line_number"] == lineno
                        and f["algorithm_detected"] == algo
                        for f in findings
                    ):
                        continue
                    db_entry = LEGACY_CRYPTO_DB.get(algo, {})
                    findings.append(
                        {
                            "finding_id": uuid.uuid4().hex[:8],
                            "file_path": file_name,
                            "language": "java",
                            "line_number": lineno,
                            "code_snippet": line.rstrip(),
                            "algorithm_detected": algo,
                            "category": db_entry.get("category", "other"),
                            "severity": db_entry.get("severity", "HIGH"),
                            "confidence": 0.75,
                            "rationale": (
                                f"Regex match for {algo} in Java source "
                                f"on line {lineno}."
                            ),
                            "quantum_threat_level": db_entry.get(
                                "quantum_threat", ""
                            ),
                            "detection_method": "regex",
                        }
                    )

    return findings


@tool
def code_scanner_tool(
    source_code: str,
    file_name: str,
    language: str = "python",
) -> str:
    """Scan source code for legacy cryptographic algorithms that are
    vulnerable to quantum computing attacks.

    Supports Python (AST + regex) and Java (regex). Returns a JSON
    array of findings, each containing the algorithm detected, line
    number, severity, confidence score, and quantum threat assessment.

    Args:
        source_code: The raw source code string to analyse.
        file_name: The filename for reporting (e.g. 'crypto_utils.py').
        language: Programming language — 'python' or 'java'.

    Returns:
        JSON string of a list of finding dictionaries.
    """
    language = language.lower().strip()

    if language == "python":
        findings = _scan_python(source_code, file_name)
    elif language == "java":
        findings = _scan_java(source_code, file_name)
    else:
        # Fallback: try Python first, then Java
        findings = _scan_python(source_code, file_name)
        if not findings:
            findings = _scan_java(source_code, file_name)

    # Sort by severity then line number
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    findings.sort(
        key=lambda f: (severity_order.get(f.get("severity", "INFO"), 5), f.get("line_number", 0))
    )

    return json.dumps(findings, indent=2)


# ════════════════════════════════════════════════════════════════
# ░░░ TOOL 2 — PQC PATCH GENERATOR ░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

# ── Patch Templates ─────────────────────────────────────────────

_PYTHON_MLKEM_TEMPLATE = textwrap.dedent("""\
    # ┌──────────────────────────────────────────────────────────┐
    # │  PQC Migration: ML-KEM-768 Key Encapsulation (FIPS 203) │
    # │  Replaces: {original_algo}                               │
    # │  Generated by PQC Secure-Code Reviewer Agent             │
    # └──────────────────────────────────────────────────────────┘
    import oqs  # liboqs-python — Open Quantum Safe

    def pqc_key_exchange():
        \"\"\"
        Perform post-quantum key encapsulation using ML-KEM-768.

        ML-KEM (Module-Lattice-Based Key Encapsulation Mechanism) is
        standardised in FIPS 203.  ML-KEM-768 provides NIST Security
        Level 3 (~AES-192 equivalent).

        Returns:
            tuple: (shared_secret_client, shared_secret_server, public_key, ciphertext)
        \"\"\"
        kem_algorithm = "ML-KEM-768"

        # --- Client: generate keypair ---
        with oqs.KeyEncapsulation(kem_algorithm) as client:
            client_public_key = client.generate_keypair()

            # --- Server: encapsulate shared secret ---
            with oqs.KeyEncapsulation(kem_algorithm) as server:
                ciphertext, shared_secret_server = server.encap_secret(
                    client_public_key
                )

            # --- Client: decapsulate to recover shared secret ---
            shared_secret_client = client.decap_secret(ciphertext)

        assert shared_secret_client == shared_secret_server, (
            "Key encapsulation mismatch — integrity failure"
        )

        return (
            shared_secret_client,
            shared_secret_server,
            client_public_key,
            ciphertext,
        )
""")

_PYTHON_MLDSA_TEMPLATE = textwrap.dedent("""\
    # ┌──────────────────────────────────────────────────────────┐
    # │  PQC Migration: ML-DSA-65 Digital Signature (FIPS 204)  │
    # │  Replaces: {original_algo}                               │
    # │  Generated by PQC Secure-Code Reviewer Agent             │
    # └──────────────────────────────────────────────────────────┘
    import oqs  # liboqs-python — Open Quantum Safe

    def pqc_sign(message: bytes) -> tuple[bytes, bytes, bytes]:
        \"\"\"
        Sign a message using ML-DSA-65 (Module-Lattice-Based Digital
        Signature Algorithm), standardised in FIPS 204.

        ML-DSA-65 provides NIST Security Level 3.

        Args:
            message: The byte-string message to sign.

        Returns:
            tuple: (signature, public_key, message) for verification.
        \"\"\"
        sig_algorithm = "ML-DSA-65"

        with oqs.Signature(sig_algorithm) as signer:
            public_key = signer.generate_keypair()
            signature = signer.sign(message)

        return signature, public_key, message


    def pqc_verify(
        message: bytes, signature: bytes, public_key: bytes
    ) -> bool:
        \"\"\"
        Verify an ML-DSA-65 signature.

        Args:
            message: The original message bytes.
            signature: The signature to verify.
            public_key: The signer's public key.

        Returns:
            bool: True if signature is valid, False otherwise.
        \"\"\"
        sig_algorithm = "ML-DSA-65"

        with oqs.Signature(sig_algorithm) as verifier:
            is_valid = verifier.verify(message, signature, public_key)

        return is_valid
""")

_PYTHON_AES256_TEMPLATE = textwrap.dedent("""\
    # ┌──────────────────────────────────────────────────────────┐
    # │  Quantum-Hardened: AES-256-GCM Authenticated Encryption │
    # │  Replaces: {original_algo}                               │
    # │  Generated by PQC Secure-Code Reviewer Agent             │
    # └──────────────────────────────────────────────────────────┘
    import os
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    def encrypt_aes256_gcm(
        plaintext: bytes, associated_data: bytes | None = None
    ) -> tuple[bytes, bytes, bytes]:
        \"\"\"
        Encrypt using AES-256-GCM (NIST SP 800-38D).

        AES-256 provides 128-bit quantum security under Grover's algorithm,
        meeting NIST's post-quantum symmetric recommendations.

        Args:
            plaintext: Data to encrypt.
            associated_data: Optional AAD for authenticated encryption.

        Returns:
            tuple: (ciphertext, nonce, key)
        \"\"\"
        key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
        return ciphertext, nonce, key


    def decrypt_aes256_gcm(
        ciphertext: bytes,
        nonce: bytes,
        key: bytes,
        associated_data: bytes | None = None,
    ) -> bytes:
        \"\"\"Decrypt AES-256-GCM ciphertext.\"\"\"
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, associated_data)
""")

_PYTHON_SHA3_TEMPLATE = textwrap.dedent("""\
    # ┌──────────────────────────────────────────────────────────┐
    # │  Quantum-Hardened: SHA-3-256 Hashing (FIPS 202)         │
    # │  Replaces: {original_algo}                               │
    # │  Generated by PQC Secure-Code Reviewer Agent             │
    # └──────────────────────────────────────────────────────────┘
    import hashlib

    def hash_sha3_256(data: bytes) -> str:
        \"\"\"
        Compute SHA-3-256 digest.

        SHA-3 (Keccak) provides 128-bit quantum security against Grover's
        algorithm for preimage attacks, and is recommended by NIST for
        post-quantum hash function usage.

        Args:
            data: Bytes to hash.

        Returns:
            Hex-encoded digest string.
        \"\"\"
        return hashlib.sha3_256(data).hexdigest()
""")

_JAVA_MLKEM_TEMPLATE = textwrap.dedent("""\
    // ┌──────────────────────────────────────────────────────────┐
    // │  PQC Migration: ML-KEM Key Encapsulation (FIPS 203)     │
    // │  Replaces: {original_algo}                               │
    // │  Generated by PQC Secure-Code Reviewer Agent             │
    // │  Requires: Bouncy Castle PQC Provider (bcprov-jdk18on)   │
    // └──────────────────────────────────────────────────────────┘
    import org.bouncycastle.pqc.jcajce.provider.BouncyCastlePQCProvider;
    import org.bouncycastle.pqc.jcajce.spec.KyberParameterSpec;
    import java.security.*;
    import javax.crypto.KEM;

    public class PQCKeyExchange {{
        static {{
            Security.addProvider(new BouncyCastlePQCProvider());
        }}

        public static byte[][] performKeyEncapsulation() throws Exception {{
            // Generate ML-KEM-768 keypair
            KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM", "BCPQC");
            kpg.initialize(KyberParameterSpec.kyber768);
            KeyPair keyPair = kpg.generateKeyPair();

            // Encapsulate
            KEM kem = KEM.getInstance("ML-KEM", "BCPQC");
            KEM.Encapsulator encapsulator = kem.newEncapsulator(keyPair.getPublic());
            KEM.Encapsulated encapsulated = encapsulator.encapsulate();

            byte[] sharedSecretSender = encapsulated.key().getEncoded();
            byte[] ciphertext = encapsulated.encapsulation();

            // Decapsulate
            KEM.Decapsulator decapsulator = kem.newDecapsulator(keyPair.getPrivate());
            byte[] sharedSecretReceiver = decapsulator.decapsulate(ciphertext).key().getEncoded();

            assert java.util.Arrays.equals(sharedSecretSender, sharedSecretReceiver);

            return new byte[][]{{sharedSecretSender, ciphertext}};
        }}
    }}
""")

_JAVA_MLDSA_TEMPLATE = textwrap.dedent("""\
    // ┌──────────────────────────────────────────────────────────┐
    // │  PQC Migration: ML-DSA Digital Signature (FIPS 204)     │
    // │  Replaces: {original_algo}                               │
    // │  Generated by PQC Secure-Code Reviewer Agent             │
    // │  Requires: Bouncy Castle PQC Provider (bcprov-jdk18on)   │
    // └──────────────────────────────────────────────────────────┘
    import org.bouncycastle.pqc.jcajce.provider.BouncyCastlePQCProvider;
    import org.bouncycastle.pqc.jcajce.spec.DilithiumParameterSpec;
    import java.security.*;

    public class PQCDigitalSignature {{
        static {{
            Security.addProvider(new BouncyCastlePQCProvider());
        }}

        public static boolean signAndVerify(byte[] message) throws Exception {{
            // Generate ML-DSA-65 keypair
            KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-DSA", "BCPQC");
            kpg.initialize(DilithiumParameterSpec.dilithium3);
            KeyPair keyPair = kpg.generateKeyPair();

            // Sign
            Signature signer = Signature.getInstance("ML-DSA", "BCPQC");
            signer.initSign(keyPair.getPrivate());
            signer.update(message);
            byte[] signature = signer.sign();

            // Verify
            Signature verifier = Signature.getInstance("ML-DSA", "BCPQC");
            verifier.initVerify(keyPair.getPublic());
            verifier.update(message);
            return verifier.verify(signature);
        }}
    }}
""")


def _select_template(
    algorithm: str, category: str, language: str
) -> tuple[str, str, str]:
    """Return (template, pqc_algorithm, migration_notes) for the finding."""

    if language == "java":
        if category in ("key_exchange",):
            return (
                _JAVA_MLKEM_TEMPLATE,
                "ML-KEM-768",
                "Requires Bouncy Castle PQC provider. Add bcprov-jdk18on "
                "and bcpqc-jdk18on to your Maven/Gradle dependencies.",
            )
        elif category in ("digital_signature",):
            return (
                _JAVA_MLDSA_TEMPLATE,
                "ML-DSA-65",
                "Requires Bouncy Castle PQC provider. Consider hybrid "
                "signatures (ML-DSA + ECDSA) for backward compatibility.",
            )
        else:
            return (
                "// TODO: Replace with AES-256-GCM or SHA-3-256 equivalent.",
                "AES-256-GCM / SHA-3-256",
                "Consult NIST SP 800-38D for authenticated encryption or "
                "FIPS 202 for quantum-safe hashing.",
            )

    # Python templates
    if category in ("key_exchange",):
        return (
            _PYTHON_MLKEM_TEMPLATE,
            "ML-KEM-768",
            "Requires liboqs-python (pip install liboqs-python). "
            "Consider hybrid KEM (ML-KEM + X25519) for transitional "
            "deployments per NIST SP 800-227.",
        )
    elif category in ("digital_signature",):
        return (
            _PYTHON_MLDSA_TEMPLATE,
            "ML-DSA-65",
            "Requires liboqs-python. ML-DSA-65 signatures are ~3.3 KB "
            "— larger than ECDSA. Evaluate bandwidth constraints. "
            "Consider composite signatures for backward compatibility.",
        )
    elif category in ("symmetric_encryption",):
        return (
            _PYTHON_AES256_TEMPLATE,
            "AES-256-GCM",
            "AES-256 is considered quantum-safe under Grover's algorithm "
            "(128-bit quantum security). Always use authenticated "
            "encryption (GCM/CCM) — never use ECB or CBC without HMAC.",
        )
    elif category in ("hashing",):
        return (
            _PYTHON_SHA3_TEMPLATE,
            "SHA-3-256",
            "SHA-3-256 provides 128-bit quantum security. For HMAC, use "
            "SHA-3 or SHA-512. Avoid MD5 and SHA-1 in all contexts.",
        )
    else:
        return (
            "# TODO: Manual review required — no automated template available.",
            "MANUAL_REVIEW",
            "This finding requires manual assessment for PQC migration.",
        )


@tool
def pqc_patch_generator_tool(findings_json: str) -> str:
    """Generate quantum-safe code patches for detected legacy crypto findings.

    Takes the JSON output from code_scanner_tool and produces replacement
    code using ML-KEM (FIPS 203) for key encapsulation, ML-DSA (FIPS 204)
    for digital signatures, AES-256-GCM for symmetric encryption, and
    SHA-3-256 for hashing.

    Args:
        findings_json: JSON string — a list of finding dicts from the scanner.

    Returns:
        JSON string of a list of patch dictionaries, each containing
        original_code, patched_code, pqc_algorithm, and migration_notes.
    """
    try:
        findings: list[dict] = json.loads(findings_json)
    except json.JSONDecodeError:
        return json.dumps(
            [{"error": "Invalid JSON input to patch generator"}]
        )

    patches: list[dict] = []
    seen_algos: set[str] = set()

    for finding in findings:
        algo = finding.get("algorithm_detected", "UNKNOWN")
        category = finding.get("category", "other")
        language = finding.get("language", "python")

        # Generate one patch per unique algorithm (avoids duplicate templates)
        patch_key = f"{algo}_{category}_{language}"
        if patch_key in seen_algos:
            # Still record the link but reuse the template
            patches.append(
                {
                    "patch_id": uuid.uuid4().hex[:8],
                    "finding_id": finding.get("finding_id", ""),
                    "original_code": finding.get("code_snippet", ""),
                    "patched_code": f"# See patch for {algo} above — same migration applies.",
                    "pqc_algorithm": LEGACY_CRYPTO_DB.get(algo, {}).get(
                        "pqc_replacement", "MANUAL_REVIEW"
                    ),
                    "migration_notes": "Duplicate finding — refer to primary patch.",
                    "is_hybrid": False,
                }
            )
            continue

        seen_algos.add(patch_key)
        template, pqc_algo, notes = _select_template(algo, category, language)

        patches.append(
            {
                "patch_id": uuid.uuid4().hex[:8],
                "finding_id": finding.get("finding_id", ""),
                "original_code": finding.get("code_snippet", ""),
                "patched_code": template.format(original_algo=algo),
                "pqc_algorithm": pqc_algo,
                "migration_notes": notes,
                "is_hybrid": False,
            }
        )

    return json.dumps(patches, indent=2)


# ════════════════════════════════════════════════════════════════
# ░░░ TOOL REGISTRY ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ════════════════════════════════════════════════════════════════

ALL_TOOLS = [code_scanner_tool, pqc_patch_generator_tool]
