import _thread
import threading
import socket
import sys
import random
import json
import queue
import operator
import time

class Router:
	monitorIP = "127.0.0.1"
	monitorPort = 5000

	#constants
	DATA_SIZE = 8192
	FILE_PADDING = 64

	#routerCode = "A" or some other letter.
	def __init__(self, routerCode, host, port):
		self.routerCode = routerCode
		self.monitorCode = "monitor"
		self.host = host
		self.port = port

		#killswitch for router
		self.kill = False

		#seed for generating random weights
		random.seed()

		# { "router code": weight }
		# { "A": 6, "C": 2 }
		self.neighbors = {}
		# { "router code": queue }
		# { "A": Queue(), "C": Queue() }
		self.arrSending = {}

		#forwarding table (dict)
		# { "A": "B", "B": "B", "C": "B" ... }
		self.forwarding = {}

		#adjacency list (dict)
		# { "A": {"B": 3}, "B": {"A": 3, "C": 5}, "C": {"B": 5}}
		self.networkGraph = {}
		self.lastGraphTime = 0

		#minimum spanning tree (dict)
		#same format as graph, but no cycles
		# { "A": {"B": 3}, "B": {"A": 3, "C": 5}, "C": {"B": 5}}
		self.networkTree = {}
		self.lastTreeTime = 0

		#conditional locks
		self.condGraph = threading.Condition()
		self.lockGraph = threading.Lock()
		self.condTree = threading.Condition()
		self.lockTree = threading.Lock()
		self.condTable = threading.Condition()
		self.lockTable = threading.Lock()

		try:
			self.sockListen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sockMonitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as msg:
			print('Failed to create socket. Error Code: ' + str(msg.errno) + ' Message ' + msg.strerror)
			sys.exit()

		try:
			self.sockListen.bind((host, port))
		except socket.error as msg:
			print("Bind failed. Error Code: " + str(msg.errno) + " Message " + msg.strerror)

	#nArray = [ (IP, port), (IP, port), ... ]
	def initConnections(self, nArray):
		# attach the monitor to gather data about the network
		self.attachMonitor()

		#Connect to adjacent Routers
		for router in nArray:
			self.createNewConnection(router)

		#Listen for new Routers
		try:
			_thread.start_new_thread(self.listen, ())
		except:
			print("Error: unable to start listen thread")

		#Generate map and tree
		self.generateGraph()
		self.generateTree()
		self.generateForwarding()

	def generateGraph(self):
		#request only one neighbor's graph
		for key, value in self.neighbors.items():
			data = self.wrapMessage("rGraph", ())

			#request updated graph and wait for it
			with self.condGraph:
				self.arrSending[key].put(data)
				self.condGraph.wait()
			break

		#update network graph with neighbors
		self.networkGraph[self.routerCode] = {}
		for key, value in self.neighbors.items():
			#make sure neighbor is in the graph
			if key not in self.networkGraph:
				self.networkGraph[key] = {}

			#add neighbor weights to each other in graph
			self.networkGraph[self.routerCode][key] = value
			self.networkGraph[key][self.routerCode] = value

		#send that the network graph has been updated
		self.broadcastUpdatedGraph()

	#remove specified router from Graph
	def removeFromGraph(self, removedCode):
		self.lockGraph.acquire()
		for key, value in self.networkGraph.items():
			value.pop(removedCode, None)
		self.networkGraph.pop(removedCode, None)
		self.lockGraph.release()

	def broadcastUpdatedGraph(self):
		for key, value in self.neighbors.items():
			data = self.wrapMessage("uGraph", (self.networkGraph, time.time()))
			self.arrSending[key].put(data)

	def generateTree(self):
		tree = {}

		#create list of all Routers and set their weight to be really high
		vertexList = {}
		for key, value in self.networkGraph.items():
			vertexList[key] = 100000000
		#set the first node to be 0 weight
		vertexList[self.routerCode] = 0

		#outside so we can update its parent
		currentCode = ""
		while vertexList:
			#get the smallest weighted Router code
			smallestVertex = sorted(vertexList.items(), key=operator.itemgetter(1))[0]
			currentCode = smallestVertex[0]
			currentWeight = smallestVertex[1]
			vertexList.pop(currentCode, None)

			#add the node to the MST
			tree[currentCode] = {}

			#set the parent of current Router if in tree
			for key, value in tree.items():
				for vKey, vValue in value.items():
					if vKey == currentCode:
						tree[currentCode][key] = vValue

			#update neightbor weights in vertex list
			updatedCodes = []
			for key, value in self.networkGraph[currentCode].items():
				for vKey, vValue in vertexList.items():
					if key == vKey and currentWeight + value < vValue:
						vertexList[key] = currentWeight + value
						#set that it's a child
						tree[currentCode][key] = value
						updatedCodes.append(vKey)

			#remove updated nodes from other parents
			for code in updatedCodes:
				for key, value in tree.items():
					if key != currentCode:
						value.pop(code, None)


		#set the parent of last Router added in tree
		for key, value in tree.items():
			for vKey, vValue in value.items():
				if vKey == currentCode:
					tree[currentCode][key] = vValue

		#set the router's MST
		self.lockTree.acquire()
		self.networkTree = tree
		self.lockTree.release()

		#send updated tree to all routers
		self.broadcastUpdatedTree()

	def broadcastUpdatedTree(self):
		for key, value in self.neighbors.items():
			data = self.wrapMessage("uTree", (self.networkTree, time.time()))
			self.arrSending[key].put(data)

	#find a path from the target to the current Router
	def searchRouterTree(self, start, path = []):
		path = path + [start]
		if start == self.routerCode:
			return path
		if start not in self.networkTree:
			return None
		for key, value in self.networkTree[start].items():
			if key not in path:
				newPath = self.searchRouterTree(key, path)
				if newPath:
					return newPath
		return None

	def generateForwarding(self):
		forward = {}

		for key, value in self.networkTree.items():
			if key != self.routerCode:
				path = self.searchRouterTree(key)
				if path:
					forward[key] = path[-2]

		self.lockTable.acquire()
		self.forwarding = forward
		self.lockTable.release()

	#unplug/remove router
	def unplug(self):
		for key, value in self.neighbors.items():
			self.arrSending[key].put(self.wrapMessage("removed", self.routerCode))
		self.kill = True

	#removedCode = code of the router to remove
	def removeRouter(self, removedCode):
		#remove from neighbors
		self.neighbors.pop(removedCode, None)
		#remove Queue from arrSending
		self.arrSending.pop(removedCode, None)

		#update graph
		self.removeFromGraph(removedCode)
		#update MST
		self.generateTree()
		#update forwarding table
		self.generateForwarding()
		pass


	#tupRouter = ("IP", port)
	def createNewConnection(self, tupRouter):
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect(tupRouter)

			#send routerCode and weight
			weight = random.randint(1, 10)		#generate random weight between 1 and 10
			data = (self.routerCode, weight)
			self.dataSend(sock, data)
			#get the neighbor router's code
			code = self.dataReceive(sock)

			#set the neighbor router's weight
			self.neighbors[code] = weight
			#create a queue to send data to this connection
			self.arrSending[code] = queue.Queue()

			# continuously send whatever data is in the buffer
			_thread.start_new_thread(self.cycleSend, (sock, code))
			# continuously receive whatever data is in the buffer
			_thread.start_new_thread(self.cycleRecv, (sock, code))

		except socket.error as msg:
			print('Failed to create socket. Error Code : ' + str(msg.errno) + ' Message ' + msg.strerror)
			sys.exit()

	def attachMonitor(self):
		#connect to the monitor
		self.sockMonitor.connect((self.monitorIP, self.monitorPort))

		# send routerCode and weight
		weight = 0 	#because the monitor isn't part of the network
		data = (self.routerCode, weight)
		self.dataSend(self.sockMonitor, data)
		# get the neighbor router's code
		self.monitorCode = self.dataReceive(self.sockMonitor)

		#create queue to send data to the monitor
		self.arrSending[self.monitorCode] = queue.Queue()

		# continuously send data in queue and receive from new Router
		_thread.start_new_thread(self.cycleSend, (self.sockMonitor, self.monitorCode))
		_thread.start_new_thread(self.cycleRecv, (self.sockMonitor, self.monitorCode))

	#listen for new routers to connect and cycling sending and receiving
	def listen(self):
		self.sockListen.listen(10)

		while True:
			conn, addr = self.sockListen.accept()

			#get the router's code and weight
			code, weight = self.dataReceive(conn)
			#send its own code
			self.dataSend(conn, self.routerCode)

			#add weight and receiving queue
			self.neighbors[code] = weight
			self.arrSending[code] = queue.Queue()

			#continuously send data in queue and receive from new Router
			_thread.start_new_thread(self.cycleRecv, (conn, code))
			_thread.start_new_thread(self.cycleSend, (conn, code))

	#wrap message with request in a tuple
	def wrapMessage(self, msgType, msgData):
		if not isinstance(msgData, tuple):
			msgData = (msgData,)
		return (msgType, msgData)

	#wrap data to route through the network
	def wrapRoute(self, destination, data, newFile = False):
		dType = "sFile"
		if (newFile):
			dType = "cFile"

		inner = data
		if not isinstance(data, tuple):
			inner = (data,)
		return self.wrapMessage("data", ((destination, self.routerCode), (dType, data)))

	#wrap sending and receiving data in JSON
	def dataReceive(self, conn):
		try:
			return json.loads(conn.recv(DATA_SIZE).decode())
		except:
			print("Recv Error: " + self.routerCode)

	def dataSend(self, conn, msg):
		try:
			conn.send(json.dumps(msg).encode())
		except:
			print("Send Error: " + self.routerCode)

	#continuously send any data that code into the specified queue
	def cycleSend(self, conn, code):
		while True:
			try:
				msg = self.arrSending[code].get()
				self.dataSend(conn, msg)
			except socket.error as msg:
				print('Socket send error. Error Code: ' + str(msg.errno) + ' Message ' + msg.strerror)
				break
			except:
				print("Sending Disconnected: " + code)
				break

		# remove router from graph (as something OBVIOUSLY happened)
		self.removeRouter(code)

		conn.close()

	#continuously receive data from the adjacent Router and process it
	def cycleRecv(self, conn, code):
		while True:
			try:
				data = self.dataReceive(conn)
				if not data:
					break

				#output some flavor text to the log
				if (code == self.monitorCode):
					#print("Monitor sent: ", str(data))
					pass
				else:
					#print("Router ", code, " sent: ", str(data))
					pass

				msgType = data[0]
				msgData = data[1]

				msgSrc = ""
				#routed data in the form:
				#("data", (("destCode", "srcCode"), ("type", (actual, data, here))))
				if (msgType == "data"):
					routerCode = msgData[1][0][0]
					if (routerCode == self.routerCode):
						#handle the message properly below
						msgType = msgData[1][1][0]
						msgData = msgData[1][1][1]
						msgSrc = msgData[1][0][1]
					else:
						#forward the data where it needs to go and continue with the next loop
						self.arrSending[self.forwarding[routerCode]].put(data)
						continue

				#request for network graph
				if (msgType == "rGraph"):
					self.arrSending[code].put(self.wrapMessage("sGraph", (self.networkGraph)))

				#received network graph
				elif (msgType == "sGraph"):
					self.lockGraph.acquire()
					try:
						self.networkGraph = msgData[0]
					finally:
						self.lockGraph.release()
						with self.condGraph:
							self.condGraph.notify_all()

				# received updated network graph
				elif (msgType == "uGraph"):
					#broadcast to all neighbors if the graph is newer than previous
					self.lockGraph.acquire()
					if (self.networkGraph != msgData[0] and msgData[1] > self.lastGraphTime):
						# update own graph
						self.networkGraph = msgData[0]
						self.broadcastUpdatedGraph()
					self.lockGraph.release()

				# request for network tree
				if (msgType == "rTree"):
					self.arrSending[code].put(self.wrapMessage("sTree", self.networkTree))

				# received network tree
				elif (msgType == "sTree"):
					self.lockTree.acquire()
					try:
						self.networkTree = msgData[0]
					finally:
						self.lockTree.release()
						with self.condTree:
							self.condTree.notify_all()

				# received updated MST
				elif (msgType == "uTree"):
					# broadcast to all neighbors if the graph is newer than previous graph
					self.lockTree.acquire()
					if (self.networkTree != msgData[0] and msgData[1] > self.lastGraphTime):
						# update own graph
						self.networkTree = msgData[0]
						self.lockTree.release()
						#elf.broadcastUpdatedTree()
					else:
						self.lockTree.release()

					#generate forwarding table based on new MST
					self.generateForwarding()

				# request for forwarding table
				if (msgType == "rTable"):
					self.arrSending[code].put(self.wrapMessage("sTable", self.forwarding))

				# received forwarding table
				elif (msgType == "sTable"):
					self.lockTable.acquire()
					try:
						self.forwarding = msgData[0]
					finally:
						self.lockTable.release()
						with self.condTable:
							self.condTable.notify_all()

				#command for router to be removed
				elif (msgType == "unplug"):
					if not self.kill:
						self.unplug()

				#router was unplugged
				elif (msgType == "removed"):
					#remove router and broadcast if this router hasn't been removed yet
					if msgData[0] in self.networkGraph:
						self.removeRouter(msgData[0])

						#forward broadcast to all neighbors
						for key, value in self.neighbors:
							self.arrSending[key].put(data)

				#file data received from the server
				elif (msgType == "rFile"):
					self.receivedFile(msgData, msgSrc)

				#file data sent to the server
				elif (msgType == "sFile"):
					self.downloadFile(msgData, msgSrc)

				#create file on the server
				elif (msgType == "cFile"):
					self.createFile(msgData, msgSrc)

				#print text received
				elif (msgType == "text"):
					print(str(code) + " sent: " + msgData[0])

			except socket.error as msg:
				print('Socket receive error. Error Code: ' + str(msg.errno) + ' Message ' + msg.strerror)
				break
			except:
				print("Listening Disconnected: " + code)
				break

		#remove router from graph (as something OBVIOUSLY happened)
		self.removeRouter(code)

		conn.close()

	def receivedFile(self, data, source):
		pass

	def downloadFile(self, data, source):
		pass

	def createFile(self, data, source):
		pass