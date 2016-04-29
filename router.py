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
	MULTIPLIER = 10

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
		get_address()

	def add_neighbor(self, address): 	# address = (IP, Port)
		n = add_weight(address)			# returns a 
		self.neighbors.append(n)

	def add_weight(self): # Adds weight between this router and a neighbor 
		self.weight = random.randint(1,11)		

	def get_address(self, PORT): # Gives router IP and Port
		self.IP = "localhost"
		self.PORT = BASE_PORT + self.routerNum*7

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


# print "hi"
# router1 = Router(1)
# router2 = Router(2)
# router3 = Router(3)
# router4 = Router(4)
# router5 = Router(5)

# print "hello router " + str(router1.routerNum)
# print "hello router " + str(router2.routerNum)
# print "hello router " + str(router3.routerNum)
# print "hello router " + str(router4.routerNum)
# print "hello router " + str(router5.routerNum)

# router1.get_address("localhost", 7777)
# router2.get_address("localhost", 1080)
# router3.get_address("localhost", 1098)
# router4.get_address("localhost", 1140)
# router5.get_address("localhost", 1214)

# print router1.IP
# print router1.PORT
# print router2.IP
# print router2.PORT
# print router3.IP
# print router3.PORT
# print router4.IP
# print router4.PORT
# print router5.IP
# print router5.PORT

# router1.add_weight()
# router2.add_weight()
# router3.add_weight()
# router4.add_weight()
# router5.add_weight()

# router1.connectNeighbour(router2)
# router2.connectNeighbour(router5)
# router3.connectNeighbour(router4)

# print router1.weight
# print router2.weight
# print router3.weight
# print router4.weight
# print router5.weight