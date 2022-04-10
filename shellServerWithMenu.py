import threading
import socketserver
from menuInfo import *

from os.path import exists



'''
	Handles the incoming connection
	Indefinitely reads commands from the respective file & executes them
'''
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	#Need to figure out a way to update the menu when a new bot connects...
	def handle(self):
	
	
		client_ip = self.client_address[0]
	
		#Gets the connection data
		data = str(self.request.recv(1024), 'ascii')
		self.cur_thread = threading.current_thread()
	
		
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

	


#----------Apologies if you have to look below this line... -----------#
#It's a load of poorly put-together junk 



if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "", 8000
	
	
	
	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	
	#Fixes a bug where closing and reopening the server too quickly
	# gives a "port already in use" error

	socketserver.TCPServer.allow_reuse_address = True


	with server:
		ip, port = server.server_address
		#print("here")
		# Start a thread with the server -- that thread will then start one
		# more thread for each request
		server_thread = threading.Thread(target=server.serve_forever)
		
		
		# Exit the server thread when the main thread terminates
		server_thread.daemon = True
		server_thread.start()
		print("Server loop running in thread:", server_thread.name)
		
		#Should return the list of bot choices for the menu
		#Right now returns junk!
		def get_bots():
			print(threading.enumerate())
			threads = threading.enumerate()
			botList = []
			for thread in threads:
				name = thread.name
				botList.append(BotChoice(name, ["1","2"]))
			return botList

		def get_bot_count():
			count = threading.activeCount()
			print(count)
			return [str(count), " bots connected"]
				
		
		#ACTUALLY POPULATES THE MENU WITH STUFF AND OPTIONS
		#Probably a bad idea to have this here...
		menu_top = Menu("Main Menu", [
		Menu(get_bot_count(), get_bots()),
		Menu("Send Commands", [])]) #Have get_bots return a list of bot "Choices"?
		
		
		top = HorizMenus()
		top.make_self(top)
		top.open_box(menu_top.menu)
		urwid.MainLoop(urwid.Filler(top, 'middle', 10), palette).run()

'''
		while True:
			
			# BELOW is meant to check the threads 
			#threads = threading.enumerate()
			#print(threading.activeCount())
			#threads_check(threads)
			
			command = input("enter a command:\n")
			print(command)
			bots = input("which bots should run this? ").split(",")
			print(bots)
			for bot in bots:
				with open("tmpfiles/" + bot.strip() + ".txt", 'w') as file:
					print("Writing", command)
					file.write(command)
	#server.shutdown()

'''
