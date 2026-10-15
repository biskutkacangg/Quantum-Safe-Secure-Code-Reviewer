# ============================================================
# sample_files/vulnerable_python.py
# INTENTIONALLY VULNERABLE — Test file for the PQC Scanner
# ============================================================
"""
This file contains intentionally deprecated cryptographic code
for testing the Post-Quantum Cryptography-Based Secure Code Review Tool's
detection capabilities. DO NOT use this code in production.
"""

import hashlib
import os

from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding, dsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from Crypto.PublicKey import RSA as PyCryptoRSA
from Crypto.Cipher import DES, AES, DES3


# ── RSA Key Generation (Vulnerable to Shor's Algorithm) ──
def generate_rsa_keypair():
    """Generate an RSA-2048 keypair — QUANTUM VULNERABLE."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key


# ── ECDSA Signing (Vulnerable to Shor's Algorithm) ──
def sign_with_ecdsa(private_key, message: bytes) -> bytes:
    """Sign a message with ECDSA P-256 — QUANTUM VULNERABLE."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256()),
    )
    return signature


# ── DSA Key Generation (Vulnerable to Shor's Algorithm) ──
def generate_dsa_key():
    """Generate a DSA key — QUANTUM VULNERABLE."""
    private_key = dsa.generate_private_key(key_size=2048)
    return private_key


# ── DES Encryption (Broken classically + Grover's) ──
def encrypt_des(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt with DES — CRITICALLY INSECURE."""
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(plaintext)


# ── 3DES Encryption (Weak, deprecated by NIST) ──
def encrypt_3des(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt with Triple-DES — DEPRECATED."""
    cipher = DES3.new(key, DES3.MODE_ECB)
    return cipher.encrypt(plaintext)


# ── MD5 Hashing (Broken collision resistance) ──
def hash_md5(data: bytes) -> str:
    """Hash with MD5 — CRYPTOGRAPHICALLY BROKEN."""
    return hashlib.md5(data).hexdigest()


# ── SHA-1 Hashing (Deprecated, known collisions) ──
def hash_sha1(data: bytes) -> str:
    """Hash with SHA-1 — DEPRECATED."""
    return hashlib.sha1(data).hexdigest()


# ── AES-128 (Reduced quantum security under Grover's) ──
def encrypt_aes_128(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt with AES-128-CBC — Reduced quantum security."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return iv + encryptor.update(plaintext) + encryptor.finalize()


if __name__ == "__main__":
    print("This file is for testing only. Do not use in production.")
    print(f"RSA keypair: {generate_rsa_keypair()}")
    print(f"MD5 hash: {hash_md5(b'test')}")
    print(f"SHA-1 hash: {hash_sha1(b'test')}")
