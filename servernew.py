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

class Server(Router):

	def __init__(self, serverCode, host, port):
		super().__init__(serverCode, host, port)

		self.router = "router"
		self.dDir = "downloads"

		self.lockFiles = threading.Lock()
		self.arrFiles = []

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

	def downloadFile(self, data, source):

		#create downloads directory
		try:
			if not os.path.exists(self.dDir):
				os.makedirs(self.dDir)
		except:
			pass

		file = open(self.dDir + "/" + filePath, "wb+")
		if file:
			

		file.close()
		
	def createFile(self, data, source):
		#get filename & filesize
		fName = data[0]
		fSize = data[1]

		#add new file data to array with filename & filesize
		self.lockFiles.acquire()
		fileNum = len(self.arrFiles)
		self.arrFiles.push((fName, [None] * fSize))
		self.lockFiles.release()

		#send file number back
		self.arrSending[self.router].put(self.wrapRoute(source, fileNum))