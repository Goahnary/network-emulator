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

	#TRACKING
	neighbors = []


	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	except socket.error, msg :
		print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()


	def __init__(self, rn):
		self.routerNum = rn
		self.get_address()

	def add_neighbor(self, neighbor): 	# address = (IP, Port)

		try :
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg :
			print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

		try:
			self.socket.bind((neighbor.IP, self.PORT - len(self.neighbors) ))
			
			n = (neighbor.routerNum, neighbor.IP, neighbor.PORT, self.get_weight())			# n = (IP, PORT, WEIGHT, routerNum)
			self.neighbors.append(n)

			print 'Successfully connected to neighbor.............................'
		except socket.error, msg :
			print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

	def get_weight(self): # Adds weight between this router and a neighbor 
		return random.randint(1,11)

	def get_address(self): # Gives router IP and Port
		self.IP = "localhost"
		self.PORT = self.BASE_PORT + self.routerNum*self.MULTIPLIER

	def update_table(self, json_table): #Updates the forwarding table to the current one
		self.table = json.loads(json_table)

	def connectNeighbour(self, neighbor):#YOU MUST ADD NEIGHBOR BEFORE CONNECTING NEIGHBOR
		


#EOF