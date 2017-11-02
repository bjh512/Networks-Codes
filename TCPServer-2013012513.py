from socket import *
import chardet
import request

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',80))
serverSocket.listen(1)

print ("The server is ready to receive")

while 1:
	connectionSocket, addr = serverSocket.accept()
	print("Connection is accepted from "+ str(addr))
	sentence = connectionSocket.recv(1024)

	print(sentence)

	connectionSocket.close()


