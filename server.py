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
    # TODO: bind control_socket to ('', CONTROL_PORT)
    # TODO: call control_socket.listen(1)
    print("Awaiting connections...")

    # TODO: accept a connection from control_socket
    # conn, addr = ???
    print("Connection requested. Creating data socket")

    # TODO: send DATA_PORT back to the client
    # conn.sendall(???)

    # --- Create data socket and wait for client ---
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TODO: bind data_socket to ('', DATA_PORT)
    # TODO: call data_socket.listen(1)
    # TODO: accept a connection from data_socket
    # data_conn, _ = ???

    # --- Handle tunnel command ---
    # TODO: receive the "tunnel" command from conn
    # command = conn.recv(BUFFER_SIZE).decode()
    print("Tunnel requested. Sending public key")

    # TODO: receive the client's public key bytes from data_conn
    # client_pub_key_bytes = data_conn.recv(BUFFER_SIZE)
    # TODO: deserialize it
    # client_public_key = deserialize_public_key(client_pub_key_bytes)

    # TODO: serialize the server's public key and send it on data_conn
    # server_pub_key_bytes = serialize_public_key(public_key)
    # data_conn.sendall(server_pub_key_bytes)

    # --- Handle post command ---
    # TODO: receive the "post" command from conn
    # command = conn.recv(BUFFER_SIZE).decode()
    print("Post requested.")

    # TODO: receive the encrypted message from data_conn
    # encrypted_msg = data_conn.recv(BUFFER_SIZE)
    # print(f"Received encrypted message: {encrypted_msg}")

    # TODO: decrypt the message using the server's private_key
    # decrypted_msg = decrypt_message(encrypted_msg, private_key)
    # print(f"Decrypted message: {decrypted_msg}")

    # TODO: compute the SHA256 hash of the decrypted message
    print("Computing hash")
    # msg_hash = compute_sha256(decrypted_msg)
    # print(f"Responding with hash: {msg_hash}")

    # TODO: encrypt the hash using the client's public key and send on data_conn
    # encrypted_hash = encrypt_message(msg_hash, client_public_key)
    # data_conn.sendall(encrypted_hash)

    # --- Cleanup ---
    # TODO: close all sockets


if __name__ == "__main__":
    start_server()