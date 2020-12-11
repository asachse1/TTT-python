# File:    ttts.py
# Author: Adam Sachsel
# Date: 12/10/2020
# E-mail:  asachse1@umbc.edu
# Description: 

#Bring in the Directories
import signal
import socket
import sys
import threading

NO_WIN = 0
CLIENT_WIN = 1
SERVER_WIN = 2
CLIENT_TOKEN = " X "
SERVER_TOKEN = " O "
TTT_CLOSE_SIGNAL = "-1"
PORT = 13037



def recv_message(s):

    Bmessage = s.recv(2048)
    message = Bmessage.decode("utf-8")

    return message

def send_message(message, s):

    Bmessage = message.encode("utf-8")
    s.send(Bmessage)

def server_move(boardList):
    ctr = 0
    hasNotMoved = True
    while ctr < (len(boardList) - 1) and hasNotMoved == True:
        if (boardList[ctr][0] =='['):
            boardList[ctr] = SERVER_TOKEN
            hasNotMoved = False
        ctr += 1
    return hasNotMoved
            

def check_win(boardList):
    winStatus = -1

    #Horizontal
    for i in range(3):
        if (boardList[0 + (3*i)] == boardList[1 + (3*i)] and boardList[1 + (3*i)] == boardList[2 + (3*i)]):
            if (boardList[0 + (3*i)] == SERVER_TOKEN):
                winStatus = SERVER_WIN
            else:
                winStatus = CLIENT_WIN
    #Vertical
    for i in range(3):
        if (boardList[i + (0*3)] == boardList[i + (1*3)] and boardList[i + (1*3)] == boardList[i + (2*3)]):
            if(boardList[i + (0*3)] == SERVER_TOKEN):
                winStatus = SERVER_WIN
            else:
                winStatus = CLIENT_WIN
    #Diagonal (TopLeft --> Bottom Right)
    if (boardList[0] == boardList[4] and boardList[4] == boardList[8]):
        if(boardList[0] == SERVER_TOKEN):
            winStatus = SERVER_WIN
        else:
            winStatus = CLIENT_WIN
    #Diagonal (TopRight --> Bottom Left)
    if (boardList[2] == boardList[4] and boardList[4] == boardList[6]):
        if(boardList[2] == SERVER_TOKEN):
            winStatus = SERVER_WIN
        else:
            winStatus = CLIENT_WIN

    return winStatus

def client_thread(conn, addr, allBoards):
    HOST = socket.gethostname()
    TTT_CLOSE_SIGNAL = "-1"
    defaultBoard = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]']
    boardString = "| {0} | {1} | {2} |\n| {3} | {4} | {5} |\n| {6} | {7} | {8} |\n"
    ClientFirst = False
    isTie = False
    winStatus = -1
    boardName = addr

    try:
        #0 sSEND (Confirm)
        message = "Connected to {}".format(HOST)
        send_message(message, conn)

        #initialize Board
        allBoards[boardName] = defaultBoard
            
        #1 RECV (ClientFirst)
        message = recv_message(conn)

        if message == "True":
            ClientFirst = True

        #server move
        if not ClientFirst:
            isTie = server_move(allBoards[boardName])

        invalidMove = False
        while message != TTT_CLOSE_SIGNAL and winStatus == -1:
            try:
                #2 SEND (BoardStatus or Invalid Move)
                if invalidMove == False:
                    message = boardString.format(*allBoards[boardName])
                send_message(message, conn)
                invalidMove = False
                #3 RECV (ClientMove)
                message = recv_message(conn)

                clientMove = int(message)

                
                if allBoards[boardName][clientMove - 1] == CLIENT_TOKEN or allBoards[boardName][clientMove - 1] == SERVER_TOKEN:
                    message = "Invalid Move, please try again."
                    invalidMove = True

                else:
                    allBoards[boardName][clientMove - 1] = CLIENT_TOKEN
                    winStatus = check_win(allBoards[boardName])
                        
                    if winStatus == -1:
                        #server move
                        isTie = server_move(allBoards[boardName])
                        if isTie == 1:
                                winStatus = 0
                        else:
                            winStatus = check_win(allBoards[boardName])
                
            except:
                continue
        if winStatus == NO_WIN:
            message = "Tie"
        elif winStatus == CLIENT_WIN:
            message = "Client"
        elif winStatus == SERVER_WIN:
            message = "Server"
        else:
            message = "Error"
        send_message(message, conn)

    except KeyboardInterrupt:
        print("Closing connection ({})...".format(boardName))
        message = TTT_CLOSE_SIGNAL
        send_message(message, conn)
        conn.close()
        print("Connection Closed")

    print("Closing connection ({})...".format(boardName))
    allBoards.pop(boardName)
    conn.close()
    print("Connection Closed")


def main():

    #Allow All public IP's to connect
    HOST = socket.gethostname()
    threadNum = 0
    #Specified Port
    
    allBoards = {}
    

    #Create Socket Object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print('Server is Up!')
    print('Connection Pending')
    #Bind Socket to port/IP
    s.bind((HOST, PORT))

    
    #Set the specified port to listening
    s.listen(5)
    try:
        while True:
            #.accept hold program until there is a connection
            #Record client's ip/hostname
            try:
                conn, addr = s.accept()
            except socket.timeout():
                continue
            #Three-Way Handshake
            #Acknowledge Handshake
            print(addr, 'connected.')
            threading.Thread(target=client_thread, name=addr[0], args=(conn,addr,allBoards), daemon=True).start()
            threadNum += 1
    except KeyboardInterrupt:
        print("Closing connection (main)...")
        s.close()
        print("Connection Closed")
    

if __name__ == "__main__":
    main()
