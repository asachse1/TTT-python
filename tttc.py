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

    Bmessage = s.recv(2048)
    message = Bmessage.decode("utf-8")

    return message

def send_message(message, s):

    Bmessage = message.encode("utf-8")
    s.send(Bmessage)



    
def main():

    #Server IP
    PORT = 13037
    TTT_CLOSE_SIGNAL = "-1"
    message = ""
    isClientFirst = False
    gameFinished = 0

    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == "-c":
            isClientFirst = True
        elif sys.argv[i] == "-s":
            HOST = sys.argv[i+1]

        

    #Create Socket Object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Connect to the Server and start the Three-Way Handshake
    s.connect((HOST,PORT))

    try:
        #0 RECV (Confirm)
        message = recv_message(s)

        #1 SEND (ClientFirst)
        if isClientFirst == True:
            message = "True"
            send_message(message, s)
        else:
            message = "False"
            send_message(message, s)

        while message != TTT_CLOSE_SIGNAL and gameFinished == False:
            #2 RECV (BoardStatus)
            message = recv_message(s)
            if(message != "Tie" and message != "Client" and message != "Server" and message != "Error"):
                #not Closing
                print("Between")
                print(message)

                #user String
                message = input("Input message: ")

                #3 SEND (ClientMove)
                send_message(message, s)
            else:
                gameFinished = 1

                
        if message == "Tie":
            print("THE GAME WAS A TIE!!!!!")
        elif message == "Client":
            print("CONGRATS!!! YOU, THE CLIENT, WON!!!")
        elif message == "Server":
            print("Too Bad... You lost to the Server...")
        elif message == "Error":
            print("Hmm... you shouldn't see this... something went wrong.")
        else:
            print("You REALLY shouldn't see this one...")

        print("Closing connection...")
        s.close()
        print("Connection Closed")
    except KeyboardInterrupt:
        print("Connection Closing...")
        message = "-1"
        send_message(message, s)
        s.close()
        print("Connection Closed.")

if __name__ == "__main__":
    main()