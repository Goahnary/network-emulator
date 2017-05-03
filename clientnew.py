from routernew import Router
import _thread
import socket
import queue
import sys
import tkinter as tk
from tkinter import filedialog
import os
import ntpath
import threading
import math

class Client(Router):

	def __init__(self, clientCode, host, port):
		super().__init__(clientCode, host, port)

		self.router = "router"
		self.sendLocation = "server"

		self.condReceiving = threading.Condition()
		self.fileNum = 0

		# listen for new Routers
		"""
		try:
			_thread.start_new_thread(self.listen, ())
		except:
			print("Error: unable to start listen thread")
		"""

	def createConnection(self, IP, port):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((IP, port))

			# send routerCode and weight
			weight = 1
			data = (self.routerCode, weight)
			self.dataSend(sock, data)
			# get the neighbor router's code
			self.router = self.dataReceive(sock)

			# set the neighbor router's weight
			self.neighbors[self.router] = weight
			# create a queue to send data to this connection
			self.arrSending[self.router] = queue.Queue()

			# continuously send whatever data is in the buffer
			_thread.start_new_thread(self.cycleSend, (sock, self.router))
			# continuously receive whatever data is in the buffer
			_thread.start_new_thread(self.cycleRecv, (sock, self.router))

			self.generateGraph()
			self.generateTree()

		except socket.error as msg:
			print('Failed to create socket. Error Code : ' + str(msg.errno) + ' Message ' + msg.strerror)
			sys.exit()

	def userListen(self):
		# get user input (removing, asking stuff, testing, idk)
		while True:
			uInput = input("Enter number to choose option:\n\t[1] : Send file to server"
						   "\nEnter choice: ")

			# shows all router codes in network
			if (uInput == "1"):
				root = tk.Tk()
				#root.withdraw()
				filePath = filedialog.askopenfilename()

				if (filePath):
					file = open(filePath, "rb")
					if file:
						fSize = os.stat(filePath).st_size
						dSize = 150#Router.DATA_SIZE - Router.FILE_PADDING
						loops = int(math.ceil(fSize / dSize))
						fName = self.pathName(filePath)

						#send initial file data and wait for filenum
						with self.condReceiving:
							self.arrSending[self.router].put(self.wrapRoute(self.sendLocation, (fName, fSize), True))
							self.condReceiving.wait()

						for i in range(0, loops):
							print("Sending part " + str(i + 1) + " of " + str(loops))
							data = file.read(dSize)
							self.arrSending[self.router].put(self.wrapRoute(self.sendLocation, (self.fileNum, i, data)))

					print("File completed.\n")
					file.close()

	def receivedFile(self, data, source):
		self.fileNum = data[0]

		with self.condReceiving:
			self.condReceiving.notify_all()

	def pathName(self, path):
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)

c = Client("client", "", 5677)
c.createConnection("localhost", 5501)
c.userListen()