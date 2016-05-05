import networkx as nx
import matplotlib.pyplot as plt
import time
from router import Router

r1 = Router(1)
r2 = Router(2)
r3 = Router(3)
r4 = Router(4)
r5 = Router(5)
r6 = Router(6)
r7 = Router(7)
r8 = Router(8)
r9 = Router(9)
r10 = Router(10)

routers = {1:r1, 2:r2, 3:r3, 4:r4, 5:r5, 6:r6, 7:r7, 8:r8, 9:r9, 10:r10}

# for x in routers:
# 	print "Router " + str(x.routerNum) + ": " + str(x.IP) + " " + str(x.PORT)


graph = []

# @FIXME: FIND RANDOM CONNECTIONS
# print "connecting r1 to r2: "
r1.add_neighbor(r2)
r2.add_neighbor(r1)
graph.append( (1, 2, 5) )

# print "connecting r2 to r3: "
r2.add_neighbor(r3)
r3.add_neighbor(r2)
graph.append( (2, 3, 2) )

# print "connecting r3 to r4: "
r3.add_neighbor(r4)
r4.add_neighbor(r3)
graph.append( (3, 4, 9) )

# print "connecting r3 to r5: "
r3.add_neighbor(r5)
r5.add_neighbor(r3)
graph.append( (3, 5, 1) )

# print "connecting r4 to r6: "
r4.add_neighbor(r6)
r6.add_neighbor(r4)
graph.append( (4, 6, 1) )

# print "connecting r5 to r6: "
r5.add_neighbor(r6)
r6.add_neighbor(r5)
graph.append( (5, 6, 10) )

# print "connecting r6 to r7: "
r6.add_neighbor(r7)
r7.add_neighbor(r6)
graph.append( (6, 7, 7) )

# print "connecting r7 to r8: "
r7.add_neighbor(r8)
r8.add_neighbor(r7)
graph.append( (7, 8, 1) )

# print "connecting r7 to r9: "
r7.add_neighbor(r9)
r9.add_neighbor(r7)
graph.append( (7, 9, 8) )

# print "connecting r8 to r10: "
r8.add_neighbor(r10)
r10.add_neighbor(r8)
graph.append( (8, 10, 11) )

# print "connecting r9 to r10: "
r9.add_neighbor(r10)
r10.add_neighbor(r9)
graph.append( (9, 10, 2) )

# for x in r6.neighbors:
# 	print x


def draw_graph():

    G=nx.Graph()

    for k,v in routers.items():
    	G.add_node("r" + str(v.routerNum))

    #NEED TO CHANGE THIS TO LOOP through graph and dynamically
    for x in graph:
    	G.add_edge('r' + str(x[0]),'r' + str(x[1]),weight=x[2])

    # elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >5]
    # esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=5]

    pos=nx.spring_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=700,node_color='b')

    # edges
    # nx.draw_networkx_edges(G,pos,edgelist=elarge,width=6)
    nx.draw_networkx_edges(G,pos,edgelist=None,width=6,alpha=0.5,edge_color='b',style='solid',label="e")

    # labels
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')


    # weights = []
    # weights.append(G.get_edge_data('r1','r2'))
    # weights.append(G.get_edge_data('r3','r2'))
    # weights.append(G.get_edge_data('r5','r3'))
    # weights.append(G.get_edge_data('r7','r9'))
    # weights.append(G.get_edge_data('r10','r4'))
    # weights.append(G.get_edge_data('r2','r10'))
    # weights.append(G.get_edge_data('r5','r9'))
    # weights.append(G.get_edge_data('r4','r1'))
    # weights.append(G.get_edge_data('r6','r7'))
    # weights.append(G.get_edge_data('r9','r10'))
    # weights.append(G.get_edge_data('r8','r2'))
    # weights.append(G.get_edge_data('r9','r8'))
    # weights.append(G.get_edge_data('r3','r8'))


    # print'The weights of the connected routers are: ' + str(weights)


    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

draw_graph()

print "Welcome to our Network Emulator!"
time.sleep(1)

while True:

	rDrop = input("Enter a router id to drop(integer): ")

	if rDrop == "exit":
		break

	graph2 = ()

	#Drop edges from graph:
	for x in graph:
		if x[0] == rDrop or x[1] == rDrop:
			pass
		else:
			graph2 = graph2 + (x,)

	graph = graph2

	# Drop router:
	for x in routers[rDrop].neighbors:
		routers[x[0]].drop_neighbor(rDrop)


	for x in routers[rDrop].neighbors:
		print "neighbors of r" + str(routers[x[0]].routerNum) + ":"
		for x in routers[x[0]].neighbors:
			print x

	del routers[rDrop]

	draw_graph()