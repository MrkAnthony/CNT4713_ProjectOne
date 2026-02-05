#!/usr/bin/env python3
"""
Simple FTP Client - Passive Mode
Usage: python myftp.py server-name

References:
- https://www.eventhelix.com/networking/ftp/
- https://realpython.com/python-sockets/
- RFC 959: https://www.ietf.org/rfc/rfc959.txt
"""

from socket import socket, AF_INET, SOCK_STREAM
import sys
import os


def send_command(client_socket, command):
    """Send a command to the FTP server and return the response."""
    full_command = command + "\r\n"
    client_socket.sendall(full_command.encode("utf-8"))
    response = receive_data(client_socket)
    return response


def receive_data(client_socket):
    """Receive data from a socket and decode it."""
    data = client_socket.recv(4096)
    return data.decode("utf-8")


def receive_all_data(data_socket):
    """Receive all data from a socket until connection closes."""
    chunks = []
    while True:
        chunk = data_socket.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    return b"".join(chunks)


def parse_pasv_response(response):
    """
    Parse PASV response to extract IP and port.
    Response format: 227 Entering Passive Mode (h1,h2,h3,h4,p1,p2)
    IP = h1.h2.h3.h4
    Port = p1 * 256 + p2
    """
    # Find the numbers inside parentheses
    start = response.find("(")
    end = response.find(")")
    if start == -1 or end == -1:
        return None, None

    numbers = response[start + 1:end].split(",")
    if len(numbers) != 6:
        return None, None

    # Build IP address
    ip = ".".join(numbers[:4])

    # Calculate port number
    port = int(numbers[4]) * 256 + int(numbers[5])

    return ip, port


def enter_pasv_mode(client_socket):
    """
    Enter passive mode and return a connected data socket.
    Returns: (status_code, data_socket) or (0, None) on failure
    """
    response = send_command(client_socket, "PASV")
    print(response.strip())

    if not response.startswith("227"):
        return 0, None

    ip, port = parse_pasv_response(response)
    if ip is None:
        return 0, None

    # Create and connect data socket
    data_socket = socket(AF_INET, SOCK_STREAM)
    data_socket.connect((ip, port))

    return 227, data_socket


def ftp_login(client_socket, username, password):
    """
    Perform FTP login sequence.
    Returns True on success, False on failure.
    """
    # Send username
    response = send_command(client_socket, f"USER {username}")
    print(response.strip())

    if not response.startswith("331"):
        print("Failed: Username not accepted")
        return False

    # Send password
    response = send_command(client_socket, f"PASS {password}")
    print(response.strip())

    if response.startswith("230"):
        print("Login successful")
        return True
    else:
        print("Failed: Login incorrect")
        return False


def ftp_list(client_socket):
    """List files in current directory (ls command)."""
    status, data_socket = enter_pasv_mode(client_socket)
    if status != 227:
        print("Failed: Could not enter passive mode")
        return

    response = send_command(client_socket, "LIST")
    print(response.strip())

    if response.startswith("150") or response.startswith("125"):
        # Receive directory listing
        data = receive_all_data(data_socket)
        print(data.decode("utf-8"))
        data_socket.close()

        # Get completion response
        response = receive_data(client_socket)
        print(response.strip())
    else:
        data_socket.close()
        print("Failed: Could not list directory")


def ftp_cd(client_socket, directory):
    """Change working directory (cd command)."""
    response = send_command(client_socket, f"CWD {directory}")
    print(response.strip())

    if response.startswith("250"):
        print("Success: Directory changed")
    else:
        print("Failed: Could not change directory")


def ftp_get(client_socket, filename):
    """Download a file from the server (get command)."""
    status, data_socket = enter_pasv_mode(client_socket)
    if status != 227:
        print("Failed: Could not enter passive mode")
        return

    response = send_command(client_socket, f"RETR {filename}")
    print(response.strip())

    if response.startswith("150") or response.startswith("125"):
        # Receive file data
        data = receive_all_data(data_socket)
        data_socket.close()

        # Save to local file
        with open(filename, "wb") as f:
            f.write(data)

        # Get completion response
        response = receive_data(client_socket)
        print(response.strip())
        print(f"Success: Downloaded {len(data)} bytes")
    else:
        data_socket.close()
        print("Failed: Could not download file")


def ftp_put(client_socket, filename):
    """Upload a file to the server (put command)."""
    # Check if local file exists
    if not os.path.isfile(filename):
        print(f"Failed: Local file '{filename}' not found")
        return

    status, data_socket = enter_pasv_mode(client_socket)
    if status != 227:
        print("Failed: Could not enter passive mode")
        return

    response = send_command(client_socket, f"STOR {filename}")
    print(response.strip())

    if response.startswith("150") or response.startswith("125"):
        # Read and send file data
        with open(filename, "rb") as f:
            data = f.read()

        data_socket.sendall(data)
        data_socket.close()

        # Get completion response
        response = receive_data(client_socket)
        print(response.strip())
        print(f"Success: Uploaded {len(data)} bytes")
    else:
        data_socket.close()
        print("Failed: Could not upload file")


def ftp_delete(client_socket, filename):
    """Delete a file on the server (delete command)."""
    response = send_command(client_socket, f"DELE {filename}")
    print(response.strip())

    if response.startswith("250"):
        print("Success: File deleted")
    else:
        print("Failed: Could not delete file")


def ftp_quit(client_socket):
    """Quit the FTP session."""
    response = send_command(client_socket, "QUIT")
    print(response.strip())
    print("Disconnecting...")


def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python myftp.py server-name")
        sys.exit(1)

    server = sys.argv[1]
    port = 21

    # Create control socket and connect
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        client_socket.connect((server, port))
    except Exception as e:
        print(f"Failed: Could not connect to {server}:{port}")
        print(f"Error: {e}")
        sys.exit(1)

    # Receive welcome message
    welcome = receive_data(client_socket)
    print(welcome.strip())

    if not welcome.startswith("220"):
        print("Failed: Server did not send welcome message")
        client_socket.close()
        sys.exit(1)

    # Get credentials
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Login
    if not ftp_login(client_socket, username, password):
        client_socket.close()
        sys.exit(1)

    # Main command loop
    while True:
        try:
            user_input = input("myftp> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            ftp_quit(client_socket)
            break

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if command == "ls":
            ftp_list(client_socket)

        elif command == "cd":
            if not argument:
                print("Usage: cd remote-dir")
            else:
                ftp_cd(client_socket, argument)

        elif command == "get":
            if not argument:
                print("Usage: get remote-file")
            else:
                ftp_get(client_socket, argument)

        elif command == "put":
            if not argument:
                print("Usage: put local-file")
            else:
                ftp_put(client_socket, argument)

        elif command == "delete":
            if not argument:
                print("Usage: delete remote-file")
            else:
                ftp_delete(client_socket, argument)

        elif command == "quit":
            ftp_quit(client_socket)
            break

        else:
            print(f"Unknown command: {command}")
            print("Available commands: ls, cd, get, put, delete, quit")

    client_socket.close()
    sys.exit(0)


if __name__ == "__main__":
    main()

