# crypto_utils.py
# Teammate 3 - Shared cryptography utilities
# Used by both server.py and client.py
#
# TODO: Install the required library before starting:
#   pip install cryptography

import hashlib
# TODO: Import the necessary classes from the cryptography library
# Hint: You'll need RSA key generation, OAEP padding, and SHA256 from
# the `cryptography` package (cryptography.hazmat.primitives)


def generate_rsa_keypair():
    """
    Generate a new RSA public/private key pair.

    Returns:
        tuple: (private_key, public_key)

    TODO:
        - Generate an RSA key with a secure key size (e.g. 2048 bits)
        - Return both the private and public key objects
    """
    pass


def serialize_public_key(public_key):
    """
    Serialize a public key to bytes so it can be sent over a socket.

    Args:
        public_key: RSA public key object

    Returns:
        bytes: The serialized public key in PEM format

    TODO:
        - Use the serialization module to encode the key as PEM
    """
    pass


def deserialize_public_key(public_key_bytes):
    """
    Deserialize a public key received over a socket back into a key object.

    Args:
        public_key_bytes (bytes): PEM-encoded public key

    Returns:
        RSA public key object

    TODO:
        - Use the serialization module to load the key from PEM bytes
    """
    pass


def encrypt_message(message: str, public_key) -> bytes:
    """
    Encrypt a plaintext message using an RSA public key.

    Args:
        message (str): The plaintext message to encrypt
        public_key: RSA public key object

    Returns:
        bytes: The encrypted ciphertext

    TODO:
        - Encode the message string to bytes
        - Encrypt using OAEP padding with SHA256
    """
    pass


def decrypt_message(ciphertext: bytes, private_key) -> str:
    """
    Decrypt a ciphertext using an RSA private key.

    Args:
        ciphertext (bytes): The encrypted message
        private_key: RSA private key object

    Returns:
        str: The decrypted plaintext message

    TODO:
        - Decrypt using OAEP padding with SHA256 (matching encrypt_message)
        - Decode the result back to a string
    """
    pass


def compute_sha256(message: str) -> str:
    """
    Compute the SHA256 hash of a plaintext message.

    Args:
        message (str): The plaintext message

    Returns:
        str: The hex-encoded SHA256 hash

    TODO:
        - Encode the message to bytes
        - Return the hex digest
    """
    return hashlib.sha256(message.encode()).hexdigest()