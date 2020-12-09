# File:    Socket Server Testing.py
# Author: Adam Sachsel
# Date: 10/10/2018
# E-mail:  adamsachsel@gmail.com
# Description: 

#Bring in the Directories
import socket
import select
import sys
             
#Allow All public IP's to connect
HOST = ''
#Specified Port
PORT = 8876

#Create Socket Object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind Socket to port/IP
s.bind((HOST, PORT))

#Set the specified port to listening
s.listen()

#.accept hold program until there is a connection
#Record client's ip/hostname
conn, addr = s.accept()
#Three-Way Handshake

#Acknowledge Handshake
print(addr, 'connected.')

while True:
    #.recv Blocks until bite size (1024) is filled with incoming data or
    # the Connection is closed.
    data = conn.recv(1024)
    if data:
        conn.sendall(data)
    else:
        break
s.close()