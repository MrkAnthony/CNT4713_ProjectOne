# client.py
# Teammate 2
# Run with: python client.py  (after starting server.py)

import socket
from crypto_utils import (
    generate_rsa_keypair,
    serialize_public_key,
    deserialize_public_key,
    encrypt_message,
    decrypt_message,
    compute_sha256,
)

SERVER_HOST = "localhost"
CONTROL_PORT = 8080
BUFFER_SIZE = 4096
MESSAGE = "Hello"


def start_client():
    print("Starting client...")


    print("Creating RSA keypair")
    private_key, public_key = generate_rsa_keypair()
    print("RSA keypair created")


    print("Creating client socket")
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to server")
    control_socket.connect((SERVER_HOST, CONTROL_PORT))


    control_socket.sendall(b"connect")


    data_port = int(control_socket.recv(BUFFER_SIZE).decode().strip())


    print("Creating data socket")
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((SERVER_HOST, data_port))


    print("Requesting tunnel")
    control_socket.sendall(b"tunnel")


    client_pub_key_bytes = serialize_public_key(public_key)
    data_socket.sendall(client_pub_key_bytes)


    server_pub_key_bytes = data_socket.recv(BUFFER_SIZE)
    server_public_key = deserialize_public_key(server_pub_key_bytes)
    print("Server public key received")
    print("Tunnel established")


    print(f"Encrypting message: {MESSAGE}")
    encrypted_msg = encrypt_message(MESSAGE, server_public_key)
    print(f"Sending encrypted message: {encrypted_msg}")


    control_socket.sendall(b"post")


    data_socket.sendall(encrypted_msg)


    encrypted_hash = data_socket.recv(BUFFER_SIZE)
    print("Received hash")

    received_hash = decrypt_message(encrypted_hash, private_key)

    print("Computing hash")
    local_hash = compute_sha256(MESSAGE)

    if received_hash == local_hash:
        print("Secure")
    else:
        print("Compromised")


    data_socket.close()
    control_socket.close()


if __name__ == "__main__":
    start_client()