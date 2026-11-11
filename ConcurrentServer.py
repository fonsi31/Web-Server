from socket import *
import sys
import threading
import random
import time

def handleClient(connectionSocket):
    print(f"Client Started: {threading.current_thread().name}")

    delay = random.randint(1, 8)
    print(f"Please wait for {delay} seconds")
    time.sleep(delay)

    try:
        message = connectionSocket.recv(1024).decode() #client request
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines() #will be delivered to client

        connectionSocket.send(b"HTTP/1.1 200 OK\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send(b"\r\n")

        for line in outputdata:
            connectionSocket.send(line.encode())

        connectionSocket.close()

    except IOError:
        connectionSocket.send(b"HTTP/1.1 404 Not Found\r\n")
        connectionSocket.send(b"Content-Type: text/html\r\n")
        connectionSocket.send(b"r\n")
        connectionSocket.send(b"<h1> 404 Not Found </h1>")

    finally:
        connectionSocket.close()
        print(f"Client Finished: {threading.current_thread().name}")

#create listening socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#bind socket
serverPort = 6789
serverSocket.bind(('', serverPort))

#wait for incoming client requests
serverSocket.listen(5)

print('CSNETWK Web Server is ready to serve...')

while True:
    #socket provided for a client
    connectionSocket, cli_addr = serverSocket.accept()
    
    clientThread = threading.Thread(target=handleClient, args=(connectionSocket,))
    clientThread.start()

serverSocket.close() 
sys.exit()