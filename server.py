from router import Router
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
			self.arrReceiving[self.router] = queue.Queue()

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
		fileNum = data[0]
		#fData = int(data[2], 2)
		#fData = fData.to_bytes((fData.bit_length() + 7) // 8, 'big')
		fData = data[2].encode("latin-1")
		numBytes = data[1] * Router.PACKET_SIZE + len(fData)
		startBytes = data[1] * Router.PACKET_SIZE

		#add bytes to file
		file = self.arrFiles[fileNum][2]
		file.seek(startBytes)
		file.write(bytearray(fData))

		print(str(numBytes) + " / " + str(self.arrFiles[fileNum][1]))

		#create the file from the array of bytes if its completed
		if (numBytes >= self.arrFiles[fileNum][1]):
			print("File " + self.arrFiles[fileNum][0] + " finished downloading.")
			file.close()
		
	def createFile(self, data, source):
		#get filename & filesize
		fName = data[0]
		fSize = data[1]

		# create downloads directory
		try:
			if not os.path.exists(self.dDir):
				os.makedirs(self.dDir)
		except:
			pass

		#add new file data to array with filename & filesize
		self.lockFiles.acquire()
		fileNum = len(self.arrFiles)
		#create file of necessary size
		file = open(self.dDir + "/" + fName, "wb+")
		if file:
			file.seek(fSize - 1)
			file.write(b"\0")
		self.arrFiles.append([fName, fSize, file])
		self.lockFiles.release()

		#send file number back
		self.arrSending[self.router].put(self.wrapRoute(source, "rFile", fileNum))