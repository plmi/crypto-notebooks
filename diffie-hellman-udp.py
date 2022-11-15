#!/usr/bin/env python3

from scapy.all import *
import argparse
# https://github.com/amiralis/pyDH
import pyDH

class Colors:
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  RESET = '\033[0m'

def listen_for_public_key(interface: str, destination: str) -> str:
    print(f'[+] listening for public key of sender..')
    sniff_filter: str = f'ip and host {args.destination} and udp'
    packet_list = sniff(iface=args.interface, filter=sniff_filter, count=1)
    packet = packet_list[0]
    payload: bytes = packet[UDP].payload
    public_key_of_sender: int = int.from_bytes(payload, byteorder='big')
    print(f'[+] received public key: {Colors.YELLOW if args.listen else Colors.GREEN}{public_key_of_sender}{Colors.RESET}')
    return public_key_of_sender

def send_public_key(public_key: str, interface: str, destination: str, port: int) -> None:
    print(f'[+] send own public key: {public_key}')
    payload = bytes.fromhex(hex(public_key)[2:])
    packet = IP(dst=destination)/UDP(dport=port)/payload
    send(packet, iface=interface)

def compute_shared_secret(diffie_hellman: pyDH.DiffieHellman, other_public_key: str) -> str:
    shared_key = diffie_hellman.gen_shared_key(other_public_key)
    print(f'computed shared secret: {Colors.RED}{shared_key}{Colors.RESET}')
    return shared_key

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--destination', type=str, help='destination IPv4 address')
  parser.add_argument('-i', '--interface', type=str, help='interface to sniff on')
  parser.add_argument('-p', '--port', type=int, help='destination port')
  parser.add_argument('-l', '--listen', type=bool, help='listening mode')
  args = parser.parse_args()

  diffie_hellman = pyDH.DiffieHellman()
  public_key = diffie_hellman.gen_public_key()
  print(f'[+] generate public key: {Colors.GREEN if args.listen else Colors.YELLOW}{public_key}{Colors.RESET}')

  if args.listen:
    # sudo python3 <program>.py --interface 'lo' --destination '127.0.0.1' --port 9999 --listen 1
    public_key_of_sender = listen_for_public_key(args.interface, args.destination)
    compute_shared_secret(diffie_hellman, public_key_of_sender)
    send_public_key(public_key, args.interface, args.destination, args.port)
  else:
    # sudo python3 <program>.py --interface 'lo' --destination '127.0.0.1' --port 9999
    send_public_key(public_key, args.interface, args.destination, args.port)
    public_key_of_sender = listen_for_public_key(args.interface, args.destination)
    compute_shared_secret(diffie_hellman, public_key_of_sender)
