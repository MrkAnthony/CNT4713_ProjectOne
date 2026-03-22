#!/usr/bin/env python3
import sys
import socket
import struct
import random

DNS_PORT = 53


def build_query(domain):
    # The random transaction ID
    transaction_id = random.randint(0, 65535)

    flags = 0x000

    # Header counts: 1 question, 0 answers, 0 authority, and 0 addtionals
    header = struct.pack(">HHHHHH", transaction_id, flags, 1, 0, 0, 0)

    # Encode the domain name
    question = b""
    for part in domain.split("."):
        question += bytes([len(part)]) + part.encode()
    question += b"\x00"

    question += struct.pack(">HH", 1, 1)

    return header + question


def parse_response(data):
    # Return: (answers, authority, additional)
    # Each as a list of (name, type, value) tuples
    # Remember to handle DNS name compression (pointers)
    answers = []
    authority = []
    additional = []

    # DNS header is 12 bytes
    # ID, flags, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT
    header = struct.unpack("!HHHHHH", data[:12])
    qdcount = header[2]
    ancount = header[3]
    nscount = header[4]
    arcount = header[5]

    offset = 12

    # skip question section
    for _ in range(qdcount):
        _, offset = decode_name(data, offset)
        offset += 4  # QTYPE (2) + QCLASS (2)

    def parse_rr(offset):
        name, offset = decode_name(data, offset)

        rtype, rclass, ttl, rdlength = struct.unpack("!HHIH", data[offset:offset + 10])
        offset += 10

        rdata_offset = offset

        # A record
        if rtype == 1 and rdlength == 4:
            ip = socket.inet_ntoa(data[offset:offset + 4])
            value = ip

        # NS record
        elif rtype == 2:
            ns_name, _ = decode_name(data, offset)
            value = ns_name

        else:
            value = None

        offset += rdlength
        return (name, rtype, value), offset

    # Answer section
    for _ in range(ancount):
        record, offset = parse_rr(offset)
        if record[1] == 1:  # only keep A
            answers.append(record)

    # Authority section
    for _ in range(nscount):
        record, offset = parse_rr(offset)
        if record[1] == 2:  # only keep NS
            authority.append(record)

    # Additional section
    for _ in range(arcount):
        record, offset = parse_rr(offset)
        if record[1] == 1:  # only keep A
            additional.append(record)

    return answers, authority, additional


def decode_name(data, offset):
    # Returns (name_string, new_offset)
    labels = []
    jumped = False
    original_offset = offset

    while True:
        length = data[offset]

        # pointer compression: first two bits are 11
        if (length & 0xC0) == 0xC0:
            pointer = ((length & 0x3F) << 8) | data[offset + 1]

            # if this is the first jump, remember where to continue after name
            if not jumped:
                original_offset = offset + 2

            offset = pointer
            jumped = True
            continue

        # end of name
        if length == 0:
            if not jumped:
                offset += 1
                return ".".join(labels), offset
            else:
                return ".".join(labels), original_offset

        offset += 1
        label = data[offset:offset + length].decode("utf-8")
        labels.append(label)
        offset += length


def send_query(server_ip, packet):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    sock.sendto(packet, (server_ip, DNS_PORT))
    response, _ = sock.recvfrom(512)
    sock.close()
    return response


def print_results(answers, authority, additional):
    print(f"{len(answers)} Answers.")
    print(f"{len(authority)} Intermediate Name Servers.")
    print(f"{len(additional)} Additional Information Records.")

    print("Answers section:")
    for name, rtype, value in answers:
        print(f"Name : {name} IP : {value}")

    print("Authority Section:")
    for name, rtype, value in authority:
        print(f"Name : {name} Name Server: {value}")

    print("Additional Information Section:")
    for name, rtype, value in additional:
        print(f"Name : {name} IP : {value}")


def resolve(domain, root_ip):
    current_server = root_ip
    visited = set()

    while True:
        print("-" * 64)
        print(f"DNS server to query: {current_server}")

        if current_server in visited:
            print("Loop detected. Stopping.")
            return
        visited.add(current_server)

        packet = build_query(domain)
        response = send_query(current_server, packet)

        answers, authority, additional = parse_response(response)

        print("Reply received. Content overview:")
        print_results(answers, authority, additional)

        if answers:
            return

        next_server = None

        for _, _, ns_name in authority:
            for add_name, _, ip in additional:
                if ns_name == add_name:
                    next_server = ip
                    break
            if next_server:
                break

        if not next_server:
            print("Could not find next DNS server IP.")
            return

        current_server = next_server


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mydns.py domain-name root-dns-ip")
        sys.exit(1)

    domain = sys.argv[1]
    root_ip = sys.argv[2]
    resolve(domain, root_ip)
