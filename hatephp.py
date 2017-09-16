#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import socket
import select
import parser
from threading import Thread


class Server(Thread):
	def __init__(self, socket, sockList):
		Thread.__init__(self)
		self.socket = socket 
		self.sockList = sockList
		self.socket.listen(1024)
		self.read, self.write, self.error = select.select(self.sockList,[],[],0)
		self.post = {}

	def run(self):
		while True:
			self.read, self.write, self.error = select.select(self.sockList,[],[],0)
			for sock in self.read:
				if sock == self.socket:
					sockfd, addr = self.socket.accept()
					self.sockList.append(sockfd)
			
				else:
					data = sock.recv(1024)
					if data:
						self.post = parser.parse(sock, data, self.post)
						self.sockList.remove(sock)
						sock.close()
					else:
						if sock in self.sockList:
							self.sockList.remove(sock)
							


class WebServer:
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('', 80))

		self.socklist = [self.socket]

	def mainloop(self):
		self.thread = Server(self.socket, self.socklist)
		self.thread.run()