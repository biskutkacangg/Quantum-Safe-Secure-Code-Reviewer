// ============================================================
// sample_files/VulnerableJava.java
// INTENTIONALLY VULNERABLE — Test file for the PQC Scanner
// ============================================================

import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;
import java.security.spec.*;

/**
 * Intentionally vulnerable Java cryptography examples.
 * DO NOT use this code in production.
 */
public class VulnerableJava {

    // ── RSA Key Generation (Vulnerable to Shor's Algorithm) ──
    public static KeyPair generateRSAKeyPair() throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(2048);
        return kpg.generateKeyPair();
    }

    // ── RSA Encryption ──
    public static byte[] encryptRSA(PublicKey publicKey, byte[] plaintext) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        return cipher.doFinal(plaintext);
    }

    // ── ECDSA Signing (Vulnerable to Shor's Algorithm) ──
    public static byte[] signECDSA(byte[] data) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC");
        kpg.initialize(new ECGenParameterSpec("secp256r1"));
        KeyPair keyPair = kpg.generateKeyPair();

        Signature sig = Signature.getInstance("SHA256withECDSA");
        sig.initSign(keyPair.getPrivate());
        sig.update(data);
        return sig.sign();
    }

    // ── DSA Signing ──
    public static byte[] signDSA(byte[] data) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA");
        kpg.initialize(2048);
        KeyPair keyPair = kpg.generateKeyPair();

        Signature sig = Signature.getInstance("SHA256withDSA");
        sig.initSign(keyPair.getPrivate());
        sig.update(data);
        return sig.sign();
    }

    // ── DES Encryption (Critically Broken) ──
    public static byte[] encryptDES(byte[] key, byte[] plaintext) throws Exception {
        SecretKeyFactory factory = SecretKeyFactory.getInstance("DES");
        Cipher cipher = Cipher.getInstance("DES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, factory.generateSecret(new DESKeySpec(key)));
        return cipher.doFinal(plaintext);
    }

    // ── MD5 Hashing (Broken) ──
    public static byte[] hashMD5(byte[] data) throws Exception {
        MessageDigest md = MessageDigest.getInstance("MD5");
        return md.digest(data);
    }

    // ── SHA-1 Hashing (Deprecated) ──
    public static byte[] hashSHA1(byte[] data) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        return md.digest(data);
    }

    // ── Diffie-Hellman Key Exchange ──
    public static KeyPair generateDHKeyPair() throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DH");
        kpg.initialize(2048);
        return kpg.generateKeyPair();
    }

    public static void main(String[] args) throws Exception {
        System.out.println("Vulnerable Java crypto examples — for testing only.");
        KeyPair rsa = generateRSAKeyPair();
        System.out.println("RSA Key generated: " + rsa.getPublic().getAlgorithm());
    }
}
