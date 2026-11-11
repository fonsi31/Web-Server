#import socket module
from socket import *
import sys # In order to terminate the program
import threading # for concurrency

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#Fill in start
serverPort = 6789
serverSocket.bind(('', serverPort)) #bind the socket to an address
serverSocket.listen(5) #listen for incoming connections
#Fill in end

#this loop handles client requests
while True:
    #Establish the connection
    print('CSNETWK Web Server is ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        print(filename)
        f = open(filename[1:])
        outputdata = f.readlines()
        #Send one HTTP header line into socket

        #Fill in start
        connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send(b"\r\n")
        #Fill in end

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.close()
    
    except IOError:
        #Send response message for file not found
        #Fill in start
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send(b"\r\n")
        connectionSocket.send(b"<h1>404 Not Found</h1>")
        #Fill in end
       
        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end
serverSocket.close()
sys.exit()  #Terminate the program after sending the corresponding data