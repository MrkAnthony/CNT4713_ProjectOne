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

    # --- Generate RSA key pair ---
    print("Creating RSA keypair")
    private_key, public_key = generate_rsa_keypair()
    print("RSA keypair created")

    # --- Connect to server on control socket ---
    print("Creating client socket")
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TODO: connect control_socket to (SERVER_HOST, CONTROL_PORT)
    print("Connecting to server")

    # TODO: send the "connect" command to the server
    # control_socket.sendall(???)

    # TODO: receive the data port number from the server
    # data_port = int(control_socket.recv(BUFFER_SIZE).decode())

    # --- Connect to server on data socket ---
    print("Creating data socket")
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # TODO: connect data_socket to (SERVER_HOST, data_port)

    # --- Send tunnel command and exchange keys ---
    print("Requesting tunnel")
    # TODO: send "tunnel" command on control_socket
    # control_socket.sendall(???)

    # TODO: serialize and send client's public key on data_socket
    # client_pub_key_bytes = serialize_public_key(public_key)
    # data_socket.sendall(client_pub_key_bytes)

    # TODO: receive the server's public key from data_socket
    # server_pub_key_bytes = data_socket.recv(BUFFER_SIZE)
    # server_public_key = deserialize_public_key(server_pub_key_bytes)
    print("Server public key received")
    print("Tunnel established")

    # --- Encrypt and send the message ---
    print(f"Encrypting message: {MESSAGE}")
    # TODO: encrypt MESSAGE using server_public_key
    # encrypted_msg = encrypt_message(MESSAGE, server_public_key)
    # print(f"Sending encrypted message: {encrypted_msg}")

    # TODO: send "post" command on control_socket
    # control_socket.sendall(???)

    # TODO: send encrypted_msg on data_socket
    # data_socket.sendall(encrypted_msg)

    # --- Receive and verify hash ---
    # TODO: receive the encrypted hash from data_socket
    # encrypted_hash = data_socket.recv(BUFFER_SIZE)
    print("Received hash")

    # TODO: decrypt the hash using client's private_key
    # received_hash = decrypt_message(encrypted_hash, private_key)

    # TODO: compute the SHA256 hash of the original MESSAGE locally
    print("Computing hash")
    # local_hash = compute_sha256(MESSAGE)

    # TODO: compare received_hash to local_hash and print result
    # if received_hash == local_hash:
    #     print("Secure")
    # else:
    #     print("Compromised")

    # --- Cleanup ---
    # TODO: close all sockets


if __name__ == "__main__":
    start_client()