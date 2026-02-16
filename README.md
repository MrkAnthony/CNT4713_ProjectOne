# FTP Client — Python

A simple FTP client built from scratch using Python sockets that supports passive mode file transfers.

## Demo Video

🎥 **[Watch the Demo](https://www.dropbox.com/scl/fi/ekg3fddkdtvbq5ov495fh/Succesful-Video.mp4?rlkey=2r15maoj612up4209nd3wzcz6&st=4kk9qqvs&dl=0)**

---

## Overview

This project recreates the basic `ftp` command-line tool by implementing all networking code from scratch. The client connects to an FTP server over TCP, authenticates, and supports common file operations using **passive (PASV) mode**.

FTP uses two separate connections:
- **Control connection (port 21)** — stays open the entire session for sending commands
- **Data connection (dynamic port)** — opens temporarily for file transfers and directory listings

---

## Features

- User authentication (USER/PASS)
- Directory listing (`ls`)
- Change directory (`cd`)
- Download files (`get`)
- Upload files (`put`)
- Delete files (`delete`)
- Graceful disconnection (`quit`)
- Passive mode (PASV) for data transfers

---

## Team Contributions

| Member                 | Role | Responsibilities |
|------------------------|------|------------------|
| **Mark-Anthony Delva** | Connection & Login (Foundation) | `sendCommand()`, `receiveData()`, `main()` setup, login flow (USER/PASS), `quitFTP()` |
| **Adrian Franquin**    | Passive Mode & Navigation | `modePASV()`, PASV response parsing, `ls` (LIST), `cd` (CWD) |
| **Milan**              | File Transfers | `get` (RETR), `put` (STOR), `delete` (DELE) |

---

## Getting Started

### Prerequisites

- Python 3.x
- No external dependencies (uses only Python standard library: `socket`, `sys`, `os`)

### Usage

```bash
python myftp.py <server-address>
```

### Example

```bash
python myftp.py inet.cs.fiu.edu
```

Then log in when prompted:

```
Enter the username: demo
Enter the password: demopass
```

---

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ls` | List files in the current directory | `myftp> ls` |
| `cd <dir>` | Change directory | `myftp> cd pub` |
| `get <file>` | Download a file | `myftp> get readme.txt` |
| `put <file>` | Upload a file | `myftp> put testfile.txt` |
| `delete <file>` | Delete a remote file | `myftp> delete testfile.txt` |
| `quit` | Disconnect from the server | `myftp> quit` |

---

## Project Structure

```
├── myftp.py              # Main FTP client
├── requirements.txt      # Dependencies (standard library only)
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

---

## References

- [FTP Protocol Overview — EventHelix](https://www.eventhelix.com/networking/ftp/)
- [FTP Port 21 Diagram (PDF)](https://www.eventhelix.com/networking/ftp/FTP_Port_21.pdf)
- [Python Sockets — Real Python](https://realpython.com/python-sockets/)
- [RFC 959 — FTP Specification](https://www.ietf.org/rfc/rfc959.txt)