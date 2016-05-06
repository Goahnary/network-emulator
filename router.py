import socket
import sys
import os
import ast
import select
import random
import json


class Router:
	
	"""docstring for router"""

	# CONSTANT VARS
	BASE_PORT = 7770
	MULTIPLIER = 9

	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except socket.error, msg :
		print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	def __init__(self, rn):
		self.routerNum = rn
		self.get_address()
		self.neighbors = []

	def add_neighbor(self, neighbor): 	# address = (IP, Port)

		try :
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg :
			print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

		try:
			self.socket.bind((neighbor.IP, self.PORT - len(self.neighbors) ))
			
			n = (neighbor.routerNum, neighbor.IP, neighbor.PORT)			# n = (IP, PORT, WEIGHT, routerNum)
			self.neighbors.append(n)

			# print 'Successfully connected to neighbor.............................'
		except socket.error, msg :
			print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

	def drop_neighbor(self, n):
		cnt = -1

		for x in self.neighbors:
			cnt += 1

			if x[0] == n:
				index = cnt

		del self.neighbors[index]

	def get_address(self): # Gives router IP and Port
		self.IP = "localhost"
		self.PORT = self.BASE_PORT + self.routerNum*self.MULTIPLIER

	def update_table(self, json_table): #Updates the forwarding table to the current one
		self.table = json.loads(json_table)

	def serve(self):
		BUFFER_SIZE = 128
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', self.PORT))
		print 'Now listening ........ '
		s.listen(1)				# listens for response
		conn, addr = s.accept()			# sets these two variables to socket accept object
		print 'connection address: ', addr	# prints who is connecting
		data = conn.recv(BUFFER_SIZE)
		s.sendto(data,("localhost",7788))
		s.close()

	def client(self, neighbor):
		BUFFER_SIZE = 128
		MESSAGE = ""
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates socket
		s.connect((neighbor.IP, neighbour.PORT))	# connects to the server
		s.send(MESSAGE)			# sends message
		data = s.recv(BUFFER_SIZE)	# Recieves return messages
		s.close()
		print "reply: ", data		