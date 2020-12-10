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

def recv_message(s):

    Bmessage = s.recv(1024)
    message = Bmessage.decode("utf-8")

    return message

def send_message(message, s):

    Bmessage = message.encode("utf-8")
    s.send(Bmessage)



    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    #Server IP
    PORT = 13037
    TTT_CLOSE_SIGNAL = "-1"
    message = ""
    isClientFirst = False

    for i in range(len(argv) - 1):
        if argv[i] == "-c":
            isClientFirst = True
        elif argv[i] == "-s":
            HOST = argv[i+1]

        

    #Create Socket Object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Connect to the Server and start the Three-Way Handshake
    s.connect((HOST,PORT))

    #1 SEND (ClientFirst)
    if isClientFirst == True:
        message = "True"
        Bmessage = message.encode("utf-8")
    else:
        message = "False"
        Bmessage = message.encode("utf-8")

    while (message != "-1"):
        #recieve from the serverside 'sendall'
        Bmessage = s.recv(1024)

        #decodes from bytes
        message = Bmessage.decode("utf-8")

        print('Received: \n', message)

        #user String
        message = input("Input message: ")

        #encode user string
        Bmessage = message.encode("utf-8")

        #Sends Data to the Server for Serverside .recv in byte format
        s.send(Bmessage)

    s.close()