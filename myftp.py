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
    command = "PASV" + "\r\n"
    # Complete
    status = 0
    if data.startswith(""):
        status = 227
    # Complete
    dataSocket.connect((ip, port))
    return status, dataSocket


# Adrian
def ftp_list(clientSocket):
    pass


# Adrian
def ftp_cd(clientSocket, directory):
    pass


# Milan
def ftp_get(clientSocket, filename):
    pass


# Milan
def ftp_put(clientSocket, filename):
    pass


# Milan
def ftp_delete(clientSocket, filename):
    pass


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
