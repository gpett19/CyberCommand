import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)
        while True:
                #Now, let's figure out how to get it to send commands instead!
                command =input("Enter a command for {}:\n".format(cur_thread.name))
                self.request.sendall(command.encode())
                message = self.request.recv(1024).strip().decode()
                response = bytes("{}: {}".format(cur_thread.name, message), 'ascii').decode()
                print(response)

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

        #server.shutdown()
