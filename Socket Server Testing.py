# File:    Socket Server Testing.py
# Author: Adam Sachsel
# Date: 10/10/2018
# E-mail:  adamsachsel@gmail.com
# Description: 

#Bring in the Directories
import signal
import socket
import sys



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
    boardArray = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]']
    boardString = "|-----|-----|-----|\n |  {0}  |  {1}  |  {2}  |\n |-----|-----|-----|\n |  {3}  |  {4}  |  {5}  |\n |-----|-----|-----|\n |  {6}  |  {7}  |  {8}  |\n |-----|-----|-----|\n".format(*boardArray)
    allBoards = []
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

    while True:
        #.recv Blocks until bite size (1024) is filled with incoming data or
        # the Connection is closed.
        data = conn.recv(1024)
        if data:
            conn.sendall(data)
        

    s.close()

