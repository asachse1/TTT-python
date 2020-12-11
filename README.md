# Adam Sachsel
# 12/10/2020
# CMSC 481 - Networking
# Tues/Thurs 7:10PM
# Fall 2020
# Socket Assignment
# TTT-python
 
Tic-Tac-Toe PROTOCOL SPECIFICATION
-----------------------------------

This RFC specifies a standard for the CMSC 481 - Networking community.
Hosts and Clients are expected to adopt and implement this standard.

INTRODUCTION
-----------------------------------

The purpose of the Tic-Tac-Toe Protocol is to provide a simple,
bi-directional, integer-oriented communication facility to enable the
playing of the traditional Tic-Tac-Toe (TTT) game on a dedicated
multi-client central server. Its primary goal is to store and simplify the
playing of this game over many clients connected to the same host
independently.

DATA ENCODING
-----------------------------------
All of the strings being passed between the client and server will be
encoded using the "utf-8" format. Each message must start as a basic
Python data type (string/integer) and must be encoded to "utf-8" standard
before being transmitted. Each transmission will be done with python's
"socket" commands of "socket.send(2048)" and "socket.recv()". Likewise,
all data recieved will be encoded in "utf-8" format and must be decoded
from "utf-8" format. The encoding and decoding may be simply done with
Python's built in .decode("utf-8") and .encode("utf-8") functions.

TTT PROTOCOL PROCEDURES
-----------------------------------
1.0) Session Preperation A session is prepared when the TTT server is run
    on a dedicated host and the port "13037" is set as OPEN on the
    computers network OR the clients and server are on the same internal
    network.

1.1) Session Initiation Once the server has been started and prints out
    the "Connection Pending" message, it is prepared to recieve the
    Clients signal to initiate a session. The client is in charge of
    initiating the connection by using the ".connect()" function that is
    present in Python's "socket" object from the corresponding library.
    Once the connect function has been run with the parameters of 1.)
    Server IP address, and 2.) 13037 the server will acknowledge the
    session by using the "accept" function and will create a separate
    thread specifically for this clients session. 
    
    The server will then send a basic message of form "Connected to 
    {HostName}" which the client must simply recieve.

    After the basic initiation, The server will wait to receive either 
    "True" or "False" which indicates whether the client will make the 
    first move in the TTT game. "True" denotes that the client will move 
    first, while "False" denotes that the server will move first.

    The server will then generate a clean gameboard and store it server-side 
    for this specific client.

1.2) BoardStatus/Invalid Move Transactions Once the session has been
    initiated and acknowledged on both sides the bi-directional
    transmissions begin and will continue on until either end of the
    connection terminates the connection. The server will begin by sending
    a copy of the gameboard for the client to print out to their interface
    (CMD or otherwise). The client must recieve up to 2048 bytes. 

    The other possible transmission from the server will be a message 
    "Invalid Move, please try again." which indicates that the last move 
    made by the client was either a full space or invalid number. Both of 
    these are handled by the same "send" statement

1.3) ClientMove Transactions The ClientMove transaction is a message being
    sent from the Client to the server. This message must contain either a
    "utf-8" encoded string of a number 1-9 or of the termination string
    "-1". Validation should be client-side to make sure this input is a
    valid string and is NEVER empty data. 
    
    BUG: If this data sent is ever empty the Client will hang and the server 
    will freeze, validation is neccessary client-side.

1.4) Session Termination There are three valid possibilities for
    termination of the connection between client and host. The FIRST
    possibility is that the client will send the termination string "-1"
    during the "ClientMove" transaction. This will signal to the server to
    end the connection with the client. The server will send one last
    termination string "-1" to the client to validate the termination and
    then it will close the socket server-side.

    The second possibility is if a "KeyboardInterrupt" is used to close the 
    client-side or server-side programs. There must be some way to deal with 
    this possibility on any newly created client scripts. The default scripts 
    have exception handlers to successfully close teh sockets on both ends and 
    then end the program gracefully.

    The final possibility is that the game has ended with either a Client Victory, 
    Server Victory, or a Tie. When this happens, the server will send either "Tie" 
    to denote a tie, "Client" to denote a client victory, or "Server" to denote a 
    server victory. This will be sent after the "ClientMove" transmission has been 
    recieved and in place of the "BoardStatus" transmission. The CLIENT must handle 
    these 3 messages and how it communicates to the user. 

1.5) Error messages There is a single error message that can be sent from
    the server at the time of a victory if the victory signal was never
    assigned to "Tie" "Client" or "Server". This will default the message
    to "Error" to denote something has gone wrong server-side. This should
    be dealt with on the client-side with a graceful shutdown of the
    socket.

NECCESSARY SIGNAL KNOWLEDGE (APPENDIX)
-----------------------------------
TTT_CLOSE_SIGNAL = "-1" : this is used client-side to signal to the server
that it must terminate the current connection.

PORT = 13037 : this is the port that the server will be running the open
socket on.

isClientFirst : the first SEND that must be done by the Client to the
server signalling who has first move. "True" = Client first, "False" =
Server First

winStatus : "Tie" = Tie, "Server" Server won the game, "Client" Client won
the Game.

