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
    pass


def decode_name(data, offset):
    # TODO: Decode a DNS name from the packet, handling pointer compression
    # Returns (name_string, new_offset)
    pass


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
