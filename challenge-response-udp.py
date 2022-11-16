#!/usr/bin/env python3

from scapy.all import *
import argparse
# https://pycryptodome.readthedocs.io/en/latest/src/hash/hmac.html?highlight=hmac
from Crypto.Hash import SHA256, HMAC
from Crypto.Random import get_random_bytes

class Colors:
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  RESET = '\033[0m'

def send_challenge(challenge: bytes, interface: str, destination: str, port: int) -> None:
  packet = IP(dst=destination)/UDP(dport=port)/challenge
  send(packet, iface=interface, verbose=False)

def listen_for_challenge_response(interface: str, destination: str) -> bytes:
    sniff_filter: str = f'ip and host {args.destination} and udp'
    packet_list = sniff(iface=args.interface, filter=sniff_filter, count=1)
    payload: bytes = bytes(packet_list[0][UDP].payload)
    return payload

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--destination', type=str, help='destination IPv4 address')
  parser.add_argument('-i', '--interface', type=str, help='interface to sniff on')
  parser.add_argument('-p', '--port', type=int, help='destination port')
  parser.add_argument('-l', '--listen', type=bool, help='listening mode')
  parser.add_argument('-s', '--secret', type=str, help='secret symmetric key')
  args = parser.parse_args()

  # alice and bob agree on domain parameters:
  # TODO: secret should be negotiated via DH
  time_validity_delta: int = 30
  secret: str = args.secret
  print(f'domain parameters: delta = {time_validity_delta}, secret = {secret}')

  if args.listen:
    # sudo python3 <program>.py --interface 'lo' --destination '127.0.0.1' --port 9999 --secret 'asdf'
    challenge: bytes = listen_for_challenge_response(args.interface, args.destination)
    hmac_instance = HMAC.new(secret.encode(), digestmod=SHA256)
    response: bytes = hmac_instance.update(challenge).digest()
    time.sleep(0.5)
    send_challenge(response, args.interface, args.destination, args.port)
  else:
    # sudo python3 <program>.py --interface 'lo' --destination '127.0.0.1' --port 9999 --secret 'asdf' --listen 1
    challenge: bytes = get_random_bytes(8)
    send_challenge(challenge, args.interface, args.destination, args.port)
    response: bytes = listen_for_challenge_response(args.interface, args.destination)
    hmac_instance = HMAC.new(secret.encode(), digestmod=SHA256)
    if response.hex() == hmac_instance.update(challenge).hexdigest():
      print(f'{Colors.GREEN}ACCEPT{Colors.RESET}')
    else:
      print(f'{Colors.RED}REJECT{Colors.RESET}')
