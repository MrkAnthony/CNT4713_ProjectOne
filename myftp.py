#!/usr/bin/env python3
# Help: https://www.eventhelix.com/networking/ftp/
# Help: https://www.eventhelix.com/networking/ftp/FTP_Port_21.pdf
# Help: https://realpython.com/python-sockets/
# Help: PASV mode may be easier in the long run. Active mode works
# Reading: https://unix.stackexchange.com/questions/93566/ls-command-in-ftp-not-working
# Reading: https://stackoverflow.com/questions/14498331/what-should-be-the-ftp-response-to-pasv-command

# import socket module
from socket import *
import sys  # In order to terminate the program


def sendCommand(socket, command) -> str:
    command += '\r\n'
    # encode the command
    dataOut = command.encode("utf-8")
    # sendout all the bytes through the network
    socket.sendall(dataOut)

    response = receiveData(socket)
    return response


def receiveData(clientSocket) -> str:
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data


def quitFTP(clientSocket) -> None:
    response = sendCommand(clientSocket, "QUIT")
    print(response)


# Adrian
def modePASV(clientSocket):

    # Send PASV
    response = sendCommand(clientSocket, "PASV")
    print(response)

    # Check
    if not response.startswith("227"):
        return 0, None

    # Extract numbers inside ()
    start = response.find("(") + 1
    end = response.find(")")
    numbers = response[start:end]

    parts = numbers.split(",")

    # Build IP
    ip = parts[0] + "." + parts[1] + "." + parts[2] + "." + parts[3]

    # Build port
    port = int(parts[4]) * 256 + int(parts[5])

    # Open data socket
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.connect((ip, port))

    return 227, dataSocket


# Adrian
def ftp_list(clientSocket):
    # Enter passive mode
    status, dataSocket = modePASV(clientSocket)

    if status != 227:
        print("Failure")
        return

    # Send LIST command
    response = sendCommand(clientSocket, "LIST")
    print(response)

    # Receive directory data
    data = b""
    while True:
        chunk = dataSocket.recv(1024)
        if not chunk:
            break
        data += chunk

    # Close data socket
    dataSocket.close()

    # Print directory listing
    print(data.decode())

    # Final server response
    final_response = receiveData(clientSocket)
    print(final_response)

    if final_response.startswith("226"):
        print("Success")
    else:
        print("Failure")




# Adrian
def ftp_cd(clientSocket, directory):

    response = sendCommand(clientSocket, "CWD " + directory)
    print(response)

    if response.startswith("250"):
        print("Success")
    else:
        print("Failure")




# Milan
def ftp_get(clientSocket, filename):
    status, dataSocket = modePASV(clientSocket)
    if status != 227:
        print("Failure")
        return

    resp = sendCommand(clientSocket, "RETR " + filename)
    print(resp)
    if not (resp.startswith("150") or resp.startswith("125")):
        dataSocket.close()
        print("Failure")
        return

    total = 0
    try:
        with open(filename, "wb") as f:
            while True:
                chunk = dataSocket.recv(4096)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
    except Exception:
        dataSocket.close()
        print("Failure")
        return

    dataSocket.close()
    final_resp = receiveData(clientSocket)
    print(final_resp)

    print("Success" if (final_resp.startswith("226") or final_resp.startswith("250")) else "Failure")
    print(f"Bytes transferred: {total}")



# Milan
def ftp_put(clientSocket, filename):
    try:
        f = open(filename, "rb")
    except Exception:
        print("Failure")
        return

    status, dataSocket = modePASV(clientSocket)
    if status != 227:
        f.close()
        print("Failure")
        return

    resp = sendCommand(clientSocket, "STOR " + filename)
    print(resp)
    if not (resp.startswith("150") or resp.startswith("125")):
        f.close()
        dataSocket.close()
        print("Failure")
        return

    total = 0
    try:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            dataSocket.sendall(chunk)
            total += len(chunk)
    except Exception:
        f.close()
        dataSocket.close()
        print("Failure")
        return

    f.close()
    try:
        dataSocket.shutdown(SHUT_WR)
    except Exception:
        pass
    dataSocket.close()

    final_resp = receiveData(clientSocket)
    print(final_resp)

    print("Success" if (fina
    l_resp.startswith("226") or final_resp.startswith("250")) else "Failure")
    print(f"Bytes transferred: {total}")



# Milan
def ftp_delete(clientSocket, filename):
    resp = sendCommand(clientSocket, "DELE " + filename)
    print(resp)
    print("Success" if resp.startswith("250") else "Failure")


def main():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    HOST = sys.argv[1]
    clientSocket.connect((HOST, 21))
    dataIn = receiveData(clientSocket)

    status = 0
    if dataIn.startswith("220"):
        status = 220
    else:
        print("The server isn't ready")
        sys.exit()

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    # Capturing the server's response
    email_response = sendCommand(clientSocket, "USER " + username)
    pass_response = sendCommand(clientSocket, "PASS " + password)

    print(dataIn)

    print("Sending username")
    print(email_response)
    print("Sending password")

    # validating the server's response
    if email_response.startswith("331"):
        status = 331
    else:
        status = 530
    print(pass_response)

    if pass_response.startswith("230"):
        status = 230
    else:
        status = 530

    # Command loop needs to be finished up
    # will only run if the login was successful with a status code of 230
    '''
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE
        pasvStatus, dataSocket = modePASV(clientSocket)
        if pasvStatus == 227:
            # COMPLETE
            pass
    '''

    print("Disconnecting...")
    clientSocket.close()
    # dataSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data


main()
