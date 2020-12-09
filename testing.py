import socket
import signal
import sys

def signal_handler(signal, frame):
    print("HELLO")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
i = 0

while True:
    
    i += 1