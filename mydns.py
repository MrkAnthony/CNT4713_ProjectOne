#!/usr/bin/env python3
import sys
import socket
import struct
import random

DNS_PORT = 53


def build_query(domain):
    # TODO: Build DNS query packet (header + question section)
    # Header: transaction ID, flags, QDCOUNT=1, others=0
    # Question: encoded domain name + QTYPE A (1) + QCLASS IN (1)
    pass


def parse_response(data):
    # TODO: Parse the binary DNS response
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
    # TODO: Decode a DNS name from the packet, handling pointer compression
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
    # TODO: Create UDP socket, send packet to server_ip:53, return raw response
    pass


def print_results(answers, authority, additional):
    print(f"{len(answers)} Answers.")
    print(f"{len(authority)} Intermediate Name Servers.")
    print(f"{len(additional)} Additional Information Records.")
    # TODO: Print each section in the format shown in the sample output
    pass


def resolve(domain, root_ip):
    current_server = root_ip

    while True:
        print("-" * 64)
        print(f"DNS server to query: {current_server}")

        packet = build_query(domain)
        response = send_query(current_server, packet)
        answers, authority, additional = parse_response(response)

        print("Reply received. Content overview:")
        print_results(answers, authority, additional)

        # If we got an A record answer, we're done
        if answers:
            print("Resolution complete.")
            return

        # TODO: Pick one NS from authority, find its IP in additional, update current_server
        # If no IP found in additional for the chosen NS, handle that edge case


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mydns.py domain-name root-dns-ip")
        sys.exit(1)

    domain = sys.argv[1]
    root_ip = sys.argv[2]
    resolve(domain, root_ip)
