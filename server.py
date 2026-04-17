# server.py
# Teammate 1
# Run with: python server.py

import socket
from crypto_utils import (
    generate_rsa_keypair,
    serialize_public_key,
    deserialize_public_key,
    decrypt_message,
    encrypt_message,
    compute_sha256,
)

CONTROL_PORT = 8080
DATA_PORT = 8081
BUFFER_SIZE = 4096


def start_server():
    print("Starting server...")

    # --- Generate RSA key pair ---
    print("Creating RSA keypair")
    private_key, public_key = generate_rsa_keypair()
    print("RSA keypair created")

    # --- Create control socket and wait for client ---
    print("Creating server socket")
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.bind(("", CONTROL_PORT))
    control_socket.listen(1)
    print("Awaiting connections...")

    conn, addr = control_socket.accept()
    print("Connection requested. Creating data socket")

    conn.sendall(str(DATA_PORT).encode())

    # --- Create data socket and wait for client ---
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(("", DATA_PORT))
    data_socket.listen(1)
    data_conn, _ = data_socket.accept()

    # --- Handle tunnel command ---
    command = conn.recv(BUFFER_SIZE).decode()
    print("Tunnel requested. Sending public key")

    client_pub_key_bytes = data_conn.recv(BUFFER_SIZE)
    client_public_key = deserialize_public_key(client_pub_key_bytes)

    server_pub_key_bytes = serialize_public_key(public_key)
    data_conn.sendall(server_pub_key_bytes)

    # --- Handle post command ---
    command = conn.recv(BUFFER_SIZE).decode()
    print("Post requested.")

    encrypted_msg = data_conn.recv(BUFFER_SIZE)
    print(f"Received encrypted message: {encrypted_msg}")

    decrypted_msg = decrypt_message(encrypted_msg, private_key)
    print(f"Decrypted message: {decrypted_msg}")

    print("Computing hash")
    msg_hash = compute_sha256(decrypted_msg)
    print(f"Responding with hash: {msg_hash}")

    encrypted_hash = encrypt_message(msg_hash, client_public_key)
    data_conn.sendall(encrypted_hash)

    # --- Cleanup ---
    data_conn.close()
    data_socket.close()
    conn.close()
    control_socket.close()


if __name__ == "__main__":
    start_server()