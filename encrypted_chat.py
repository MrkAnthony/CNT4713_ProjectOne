# crypto_utils.py
# Teammate 3 - Shared cryptography utilities
# Used by both server.py and client.py

import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def generate_rsa_keypair() -> tuple:
    """
    Generate a new RSA public/private key pair.
    Returns:
        tuple: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_public_key(public_key) -> bytes:
    """
    Serialize a public key to bytes, so it can be sent over a socket.
    Args:
        public_key: RSA public key object
    Returns:
        bytes: The serialized public key in PEM format
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def deserialize_public_key(public_key_bytes):
    """
    Deserialize a public key received over a socket back into a key object.
    Args:
        public_key_bytes (bytes): PEM-encoded public key
    Returns:
        RSA public key object
    """
    return load_pem_public_key(public_key_bytes)


def encrypt_message(message: str, public_key) -> bytes:
    """
    Encrypt a plaintext message using an RSA public key.
    Args:
        message (str): The plaintext message to encrypt
        public_key: RSA public key object
    Returns:
        bytes: The encrypted ciphertext

    """
    encoded_string = message.encode()
    return public_key.encrypt(encoded_string, padding)


def decrypt_message(ciphertext: bytes, private_key) -> str:
    """
    Decrypt a ciphertext using an RSA private key.

    Args:
        ciphertext (bytes): The encrypted message
        private_key: RSA private key object
    Returns:
        str: The decrypted plaintext message
    """
    encrypted_string = private_key.decrypt(ciphertext, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))
    return encrypted_string.decode()


def compute_sha256(message: str) -> str:
    """
    Compute the SHA256 hash of a plaintext message.
    Args:
        message (str): The plaintext message
    Returns:
        str: The hex-encoded SHA256 hash
    """
    return hashlib.sha256(message.encode()).hexdigest()
