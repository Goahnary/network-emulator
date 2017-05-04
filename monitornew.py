from routernew import Router
import _thread
import json
import time
from ast import literal_eval
import networkx as nx
import matplotlib.pyplot as plt

class Monitor(Router):
	
	def __init__(self, monitorCode, host, port):
		super().__init__(monitorCode, host, port)

		# listen for new Routers
		try:
			_thread.start_new_thread(self.listen, ())
# 			_thread.start_new_thread(self.redraw, ())
		except:
			print("Error: unable to start listen thread")

# 	def redraw(self):
# 		while True:
# 			plt.pause(1)
# 			plt.draw()

	def userListen(self, *args):
		plt.ion()
		plt.show()
		
		#get user input (removing, asking stuff, testing, idk)
		while True:
			plt.draw()
			plt.pause(2)
			
			uInput = input("Enter number to choose option:\n\t[1] : list all routers\n\t[2] : send text to router"
						   "\n\t[3] : show network graph\n\t[4] : show minimum spanning tree"
						   "\n\t[5] : show router's forwarding table\n\t[6] : Add Router\n\t[7] : Remove Router"
						   "\n\t[8] : Display Link Weights"
						   "\nEnter choice: ")

			#shows all router codes in network
			if (uInput == "1"):
				print(json.dumps(self.neighbors, sort_keys=True, indent=4), "\n")

			#send some text to a router
			elif (uInput == "2"):
				code = input("Enter router code to send to (i.e. A): ")
				try:
					qSend = self.arrSending[code]
					uMsg = input("Message: \n")
					qSend.put(self.wrapMessage("text", uMsg))
					print("Message '" + uMsg + "' sent.\n")
				except KeyError:
					print("That router does not exist.\n")

			#show network graph
			elif (uInput == "3"):

				for key, value in self.neighbors.items():
					data = self.wrapMessage("rGraph", ())

					# request updated graph and wait for it
					with self.condGraph:
						self.arrSending[key].put(data)
						self.condGraph.wait()
					break

				self.drawGraph(self.networkGraph)
				self.drawGraph(self.networkGraph)
				self.drawGraph(self.networkGraph)

			#show spanning tree
			elif (uInput == "4"):
				for key, value in self.neighbors.items():
					data = self.wrapMessage("rTree", ())

					# request updated graph and wait for it
					with self.condTree:
						self.arrSending[key].put(data)
						self.condTree.wait()
					break

				self.drawGraph(self.networkTree)
				#print(json.dumps(self.networkTree, sort_keys=True, indent=4), "\n")

			# show a specific router's forwarding table
			elif (uInput == "5"):
				
				code = input("Enter router code to get table (i.e. A): ")
				try:
					data = self.wrapMessage("rTable", ())

					#update this table with router's forwarding table
					with self.condTable:
						self.arrSending[code].put(data)
						self.condTable.wait()

					#print forwarding table
					print(json.dumps(self.forwarding, sort_keys=True, indent=4), "\n")
				except KeyError:
					print("That router does not exist.\n")

			#add a new router
			elif (uInput == "6"):
				code = input("Enter new router code (i.e. A): ")
				if code not in self.neighbors:
					port = input("Enter new port for router: ")
					try:
						nRouters = literal_eval(input("Enter routers to connect to in the form:\n"
													  "[('host', port), ('host', port), ...)]\n "))
						router = Router(code, "", eval(port))
						router.initConnections(nRouters)

						print("Router " + code + " added.\n")
					except:
						print("That wasn't formatted correctly.\n")

				else:
					print("That router already exists.\n")
					
				self.drawGraph(self.networkGraph)
				self.drawGraph(self.networkGraph)
				self.drawGraph(self.networkGraph)
			
			#remove a router
			elif (uInput == "7"):
				code = input("Enter router code to remove (i.e. A): ")
				if code in self.neighbors:
					self.arrSending[code].put( self.wrapMessage("unplug", ()))
					self.neighbors.pop(code, None)
				else:
					print("That router does not exist.\n")
					
				self.drawGraph(self.networkGraph)
				self.drawGraph(self.networkGraph)
				self.drawGraph(self.networkGraph)
				
			#list link weights
			elif (uInput == "8"):
				code = input("Enter router code (i.e. A): ")
				
				try:
					data = self.wrapMessage("rWeights", ())

					#update this table with router's forwarding table
					with self.condWeights:
						self.arrSending[code].put(data)
						self.condWeights.wait()

					#print forwarding table
					print(json.dumps(self.neighbors, sort_keys=True, indent=4), "\n")
				except KeyError:
					print("That router does not exist.\n")


	def drawGraph(self, container):
		plt.clf()

		G = nx.Graph()

		for key, value in container.items():
			G.add_node(str(key))

		edge_labels = {}
		for key, value in container.items():
			for vKey, vValue in value.items():
				G.add_edge(str(key), str(vKey), weight=vValue)
				edge_labels[(str(key), str(vKey))] = vValue


		pos = nx.spring_layout(G)  # positions for all nodes

		# nodes
		nx.draw_networkx_nodes(G, pos, node_size=700, node_color='b')

		# edges
		nx.draw_networkx_edges(G, pos, edgelist=None, width=6, alpha=0.5, edge_color='b', style='solid', label="e")

		# labels
		nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif', font_color='w')
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, font_family='sans-serif', font_color='b')