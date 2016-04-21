import socket
import sys
import os
import ast
import select
import random

class router(object):
	
	"""docstring for router"""

	# CONSTANT VARS
	BASE_PORT = 7770
	MULTIPLIER = 10

	#TRACKING
	neighbors = []


	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    print 'Socket created'
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


	def update_table(self, json): #Updates the forwarding table to the current one
		pass

	def add_neighbor(self, address):
		n = add_weight(address)

		self.neighbors.append(neighbor)

	def add_weight(self, router): # Adds weight between two neighbors 
		weight = random.randrange(1,11)
		return (router, weight)

	def get_address(self): # Gives router IP and Port
		self.IP = "localhost"
		self.PORT = BASE_PORT + (MULTIPLIER * self.routerNum)

	def get_neighbors(self): # Returns list of adjacent routers
		pass


