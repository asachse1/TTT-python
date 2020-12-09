# File:    Socket Client Testing.py
# Author: Adam Sachsel
# Date: 10/10/2018
# Lecture Section: 08
# Discussion Section: 10
# E-mail:  asachse1@umbc.edu
# Description: 

import socket
import sys

#Server IP
HOST = str(sys.argv[1])
PORT = 8876

#Create Socket Object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to the Server and start the Three-Way Handshake
s.connect((HOST,PORT))

#Sends Data to the Server for Serverside .recv
s.sendall(b'Hello,world')

#Holds program for the serverside .sendall
data = s.recv(1024)
#Prints the data on Serverside???
print('Received', repr(data))