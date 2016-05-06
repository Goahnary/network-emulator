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

routers = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]


print 'Here are the Routers available.......'
for x in routers:
  print "Router " + str(x.routerNum) + ": " + str(x.IP) + " " + str(x.PORT)


graph = []


for x in r6.neighbors:
  print x


def draw_graph():

    G=nx.Graph()

    reply = raw_input("Do you want to add a new router (y/n): ")

    if reply == "n":
     return 

    G.add_node("r1")
    G.add_node("r2")
    G.add_node("r3")
    G.add_node("r4")
    G.add_node("r5")
    G.add_node("r6")
    G.add_node("r7")
    G.add_node("r8")
    G.add_node("r9")
    G.add_node("r10")

    G.add_edge('r1','r2',weight=6)
    G.add_edge('r3','r2',weight=4)
    G.add_edge('r5','r3',weight=2)
    G.add_edge('r7','r9',weight=2)
    G.add_edge('r10','r4',weight=8)
    G.add_edge('r2','r10',weight=3)
    G.add_edge('r5','r9',weight=6)
    G.add_edge('r4','r1',weight=10)
    G.add_edge('r6','r7',weight=9)
    G.add_edge('r9','r10',weight=1)
    G.add_edge('r8','r2',weight=1)
    G.add_edge('r9','r8',weight=1)
    G.add_edge('r3','r8',weight=1)




    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >5]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=5]

    pos=nx.spring_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=700,node_color='b')

    # edges
    nx.draw_networkx_edges(G,pos,edgelist=elarge,
                        width=6)
    nx.draw_networkx_edges(G,pos,edgelist=esmall,
                        width=6,alpha=0.5,edge_color='b',style='dashed')

    # labels
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')


    weights = []
    weights.append(G.get_edge_data('r1','r2'))
    weights.append(G.get_edge_data('r3','r2'))
    weights.append(G.get_edge_data('r5','r3'))
    weights.append(G.get_edge_data('r7','r9'))
    weights.append(G.get_edge_data('r10','r4'))
    weights.append(G.get_edge_data('r2','r10'))
    weights.append(G.get_edge_data('r5','r9'))
    weights.append(G.get_edge_data('r4','r1'))
    weights.append(G.get_edge_data('r6','r7'))
    weights.append(G.get_edge_data('r9','r10'))
    weights.append(G.get_edge_data('r8','r2'))
    weights.append(G.get_edge_data('r9','r8'))
    weights.append(G.get_edge_data('r3','r8'))


    print'The weights of the connected routers are: ' + str(weights)
    print '############################################################/n'
    print 'The shortest path from the two specified router below is: '
    print(nx.dijkstra_path(G,'r1','r10'))
    print '############################################################/n'
    mst = nx.minimum_spanning_tree(G)
   # edgelist = list(mst)
    print 'The Spanning Tree: '
    print (sorted(mst.edges(data=True)))

    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

draw_graph()


print "Welcome to our Network Emulator!"
time.sleep(1)
print "This simulator provides blah blah blah" # @FIXME: WRITE A DESCRIPTION
time.sleep(1)

r2.serve()

rDrop = input("Enter a router id to drop(integer): ")

# Drop router:

for x in routers[rDrop - 1].neighbors:
  routers[x[0]-1].drop_neighbor(rDrop)

for x in routers[rDrop - 1].neighbors:
  print "neighbors of r" + str(routers[x[0]-1].routerNum) + ":"
  for x in routers[x[0]-1].neighbors:
    print x