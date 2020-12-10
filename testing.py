import socket
import signal
import sys

HOST = socket.gethostname()
PORT = 13037

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.close()