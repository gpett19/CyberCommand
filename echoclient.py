#!/usr/bin/env python3
# The echo client

import socket # sockets are the transport layer API

HOST = '192.168.1.100'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	
	while True:
		msg = input("Me: ")
		s.sendall(msg.encode())
		data = s.recv(1024)
		
		print("Recieved: ", str(data))