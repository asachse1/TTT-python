# File:    Socket Server Testing.py
# Author: Adam Sachsel
# Date: 10/10/2018
# E-mail:  adamsachsel@gmail.com
# Description: 

#Bring in the Directories
import signal
import socket
import sys
import threading



def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
  
    #Allow All public IP's to connect
    HOST = socket.gethostname()
    #Specified Port
    PORT = 13037
    TTT_CLOSE_SIGNAL = "-1"
    defaultBoard = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]']
    boardString = "| {0} | {1} | {2} |\n| {3} | {4} | {5} |\n| {6} | {7} | {8} |\n".format(*defaultBoard)
    allBoards = {}
    totalSent = 0

    #Create Socket Object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Server is Up!')
    print('Connection Pending')
    #Bind Socket to port/IP
    s.bind((HOST, PORT))

    #Set the specified port to listening
    s.listen(5)
    
    #.accept hold program until there is a connection
    #Record client's ip/hostname
    conn, addr = s.accept()

    #Three-Way Handshake
    #Acknowledge Handshake
    print(addr, 'connected.')
    conn.setblocking(False)

    message = "{}".format(HOST)
    Bmessage = message.encode("utf-8")
    conn.send(Bmessage)

    allBoards[addr[0]] = defaultBoard 
    print(boardString.format(*allBoards[addr[0]]))
    while message != TTT_CLOSE_SIGNAL:
        try:
            #.recv Blocks until bite size (1024) is filled with incoming data or
            # the Connection is closed.
            Bmessage = conn.recv(1024)
            message = Bmessage.decode("utf-8")
            print("{}: {}".format(addr[0], message))
            if message:
                conn.send(Bmessage)
            
        except:
            continue
            

    s.close()

