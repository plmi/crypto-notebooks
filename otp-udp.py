#!/usr/bin/env python3

from scapy.all import *
import argparse
# see also https://tools.ietf.org/html/rfc6238#appendix-A for the implementation details
from datetime import timezone, datetime
# https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html?highlight=hmac
from Crypto.Hash import SHA256, HMAC
import math

class Colors:
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  RESET = '\033[0m'

def compute_time(time_validity_delta: str) -> int:
  unix_time: int = int(time.time())
  return math.floor(unix_time / time_validity_delta)

def compute_mac_from_timestamp(unix_time: int, secret: str) -> str:
  hmac_instance: Crypto.Hash.HMAC.HMAC = HMAC.new(secret.encode(), digestmod=SHA256)
  return hmac_instance.update(time_token.to_bytes(5, byteorder='big')).hexdigest()

def truncate(mac: str) -> str:
  return mac

def send_otp(otp: str, interface: str, destination: str, port: int) -> None:
    payload = bytes.fromhex(otp)
    packet = IP(dst=destination)/UDP(dport=port)/payload
    print(f'[+] send otp: {Colors.YELLOW}{otp}{Colors.RESET}')
    send(packet, iface=interface)

def listen_for_otp(interface: str, destination: str) -> str:
    sniff_filter: str = f'ip and host {args.destination} and udp'
    packet_list = sniff(iface=args.interface, filter=sniff_filter, count=1)
    payload: bytes = packet_list[0][UDP].payload
    otp_of_sender: int = int.from_bytes(payload, byteorder='big')
    otp_as_hex: str = hex(otp_of_sender)[2:]
    print(f'[+] otp received: {Colors.YELLOW}{otp_as_hex}{Colors.RESET}')
    return otp_as_hex

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--destination', type=str, help='destination IPv4 address')
  parser.add_argument('-i', '--interface', type=str, help='interface to sniff on')
  parser.add_argument('-p', '--port', type=int, help='destination port')
  parser.add_argument('-l', '--listen', type=bool, help='listening mode')
  parser.add_argument('-s', '--secret', type=str, help='secret symmetric key')
  args = parser.parse_args()

  # alice and bob agree on domain parameters:
  time_validity_delta: int = 30
  secret: str = args.secret
  print(f'domain parameters: delta = {time_validity_delta}, secret = {secret}')

  if args.listen:
    # sudo python3 <program>.py --interface 'lo' --destination '127.0.0.1' --port 9999 --secret 'asdf'
    otp_of_sender: int = listen_for_otp(args.interface, args.destination)
    time_token: int = compute_time(time_validity_delta)
    mac_1: str = compute_mac_from_timestamp(time_token, secret)
    mac_2: str = compute_mac_from_timestamp(time_token - 1, secret)
    if otp_of_sender == truncate(mac_1) or otp_of_sender == truncate(mac_2):
      print(f'{Colors.GREEN}Accept{Colors.RESET}')
    else:
      print(f'{Colors.RED}Reject{Colors.RESET}')
  else:
    # sudo python3 <program>.py --interface 'lo' --destination '127.0.0.1' --port 9999 --secret 'asdf' --listen 1
    time_token: int = compute_time(time_validity_delta)
    mac: str = compute_mac_from_timestamp(time_token, secret)
    otp: str = truncate(mac)
    send_otp(otp, args.interface, args.destination, args.port)
