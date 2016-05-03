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
	MULTIPLIER = 7

	#TRACKING
	neighbors = []


	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	except socket.error, msg :
		print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

# try:
#     s.bind((IP, PORT))

# except socket.error , msg:
#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()


	def __init__(self, rn):
		self.routerNum = rn
		self.get_address()

	def add_neighbor(self, address): 	# address = (IP, Port)
		n = add_weight(address)			# returns a 
		self.neighbors.append(n)

	def add_weight(self): # Adds weight between this router and a neighbor 
		self.weight = random.randint(1,11)		

	def get_address(self): # Gives router IP and Port
		self.IP = "localhost"
		self.PORT = self.BASE_PORT + self.routerNum*self.MULTIPLIER

	def get_neighbors(self): # Returns list of adjacent routers
		return neighbors

	def update_table(self, json_table): #Updates the forwarding table to the current one
		self.table = json.loads(json_table)

	def connectNeighbour(self, neighbor):
		try :
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except socket.error, msg :
			print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

		try:
			self.socket.bind((neighbor.IP, neighbor.PORT))
			print 'Successfully connected to neighbor.............................'
		except socket.error, msg :
			print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

# router1.connectNeighbour(router2)
# router2.connectNeighbour(router5)
# router3.connectNeighbour(router4)

# print router1.weight
# print router2.weight
# print router3.weight
# print router4.weight
# print router5.weight