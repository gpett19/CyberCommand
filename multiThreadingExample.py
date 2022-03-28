import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = str(self.request.recv(1024), 'ascii')
		cur_thread = threading.current_thread()
		response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
		self.request.sendall(response)
		while True:
			thread_num = cur_thread.name.split("-")[-1]
			with open(thread_num + ".txt", 'wr') as file:
				
			#Now, let's figure out how to get it to send commands instead!
				command = file.readline()
				self.request.sendall(command.encode())
				message = self.request.recv(1024).strip().decode()
				response = bytes("{}: {}".format(cur_thread.name, message), 'ascii').decode()
				print(response)
				file.truncate(0)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "", 8000

	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
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

	while true:
		command = input("enter a command: ")
		bots = input("which bots should run this?").split(",")
		for bot in bots:
			with open(bot + ".txt", 'w') as file:
				file.write(command)

	#server.shutdown()
