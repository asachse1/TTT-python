# File:    Socket Client Testing.py
# Author: Adam Sachsel
# Date: 10/10/2018
# Lecture Section: 08
# Discussion Section: 10
# E-mail:  asachse1@umbc.edu
# Description: 

import socket
import sys
import signal

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
    boardArray = ['.', '.', '.', '.', '.', '.', '.', '.', '.']

#Server IP
HOST = str(sys.argv[1])
PORT = 13037
message = "|-----|-----|-----|\n |  {0}  |  {1}  |  {2}  |\n |-----|-----|-----|\n |  {3}  |  {4}  |  {5}  |\n |-----|-----|-----|\n |  {6}  |  {7}  |  {8}  |\n |-----|-----|-----|\n".format(*boardArray)
messageB = bytes(message, 'utf-8')

#Create Socket Object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to the Server and start the Three-Way Handshake
s.connect((HOST,PORT))

#Sends Data to the Server for Serverside .recv in byte format
s.sendall(messageB)

#Holds program for the serverside .sendall
data = s.recv(1024)

#Decodes from bytes
tempString = data.decode("utf-8")

#prints decoded data
print('Received: \n', tempString)



#-------------------\n|-----|-----|-----|\n|  X  |  X  |  X  |\n|-----|-----|-----|\n|  X  |  X  |  X  |\n|-----|-----|-----|\n|  X  |  X  |  X  |\n|-----|-----|-----|\n-------------------