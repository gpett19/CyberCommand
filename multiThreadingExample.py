import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

	#Handles the incoming bot connections
	# NOTE that this is run once when a bot connects, and then does not repeat
	# So, we basically need to have some sort of repeating listener that will determine when
	# we send commands. 
	def handle(self):
		#Gets the connection data
		data = str(self.request.recv(1024), 'ascii')
		self.cur_thread = threading.current_thread()
		#response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
		#self.request.sendall(response)
		while True:
			#Now, let's figure out how to get it to send commands instead!
			command =input("Enter a command for {}:\n".format(self.cur_thread.name))
			self.sendCommand(command)

	#Handles sending the command to the bot
	# Takes in a command string, and will send it, wait for a response, and then print the response. 
	def sendCommand(self, cmd):
		self.request.sendall(cmd.encode()) #Sends the message over to the bot
		message = self.request.recv(1024).strip().decode() #... and receives the response
		response = bytes("{}: {}".format(self.cur_thread.name, message), 'ascii').decode()
		print(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "", 8000

	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	
	#Fixes a bug where closing and reopening the server too quickly
	# gives a "port already in use" error
	socketserver.TCPServer.allow_reuse_address = True
	with server:
		ip, port = server.server_address

		# Start a thread with the server -- that thread will then start one
		# more thread for each request
		server_thread = threading.Thread(target=server.serve_forever())
		# Exit the server thread when the main thread terminates
		server_thread.daemon = True
		server_thread.start()
		print("Server loop running in thread:", server_thread.name)

		#server.shutdown()
