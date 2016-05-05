import matplotlib.pyplot as plt
from router import Router 
import networkx as nx


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

G=nx.cubical_graph()
pos=nx.spring_layout(G) # positions for all nodes

# nodes
nx.draw_networkx_nodes(G,pos,
                       nodelist=[r1,r2,r3,r4,r5],
                       node_color='r',
                       node_size=500,
               alpha=1.0)
nx.draw_networkx_nodes(G,pos,
                       nodelist=[r6,r7,r8,r9,r10],
                       node_color='b',
                       node_size=500,
               alpha=1.0)

# edges
nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
nx.draw_networkx_edges(G,pos,
                       edgelist=[(r1,r2),(r2,r3),(r3,r4),(r4,r5)],
                       width=8,alpha=0.5,edge_color='r')
nx.draw_networkx_edges(G,pos,
                       edgelist=[(r6,r7),(r8,r9),(r6,r8),(r4,r8)],
                       width=8,alpha=0.5,edge_color='b')


# some math labels
labels={}
labels[0]=r'$a$'
labels[1]=r'$b$'
labels[2]=r'$c$'
labels[3]=r'$d$'
labels[4]=r'$\alpha$'
labels[5]=r'$\beta$'
labels[6]=r'$\gamma$'
labels[7]=r'$\delta$'
labels[7]=r'$\delta$'
labels[7]=r'$\delta$'

nx.draw_networkx_labels(G,pos,labels,font_size=16)

plt.axis('off')
plt.savefig("labels_and_colors.png") # save as png
plt.show() # display


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

for x in routers:
  print "Router " + str(x.routerNum) + ": " + str(x.IP) + " " + str(x.PORT)


graph = []

# FIXME: FIND RANDOM CONNECTION
print "connecting r1 to r2: "
r1.add_neighbor(r2)
r2.add_neighbor(r1)
graph.append( (1, 2, 5) )

print "connecting r2 to r3: "
r2.add_neighbor(r3)
r3.add_neighbor(r2)
graph.append( (2, 3, 2) )

print "connecting r3 to r4: "
r3.add_neighbor(r4)
r4.add_neighbor(r3)
graph.append( (3, 4, 9) )

print "connecting r3 to r5: "
r3.add_neighbor(r5)
r5.add_neighbor(r3)
graph.append( (3, 5, 1) )

print "connecting r4 to r6: "
r4.add_neighbor(r6)
r6.add_neighbor(r4)
graph.append( (4, 6, 1) )

print "connecting r5 to r6: "
r5.add_neighbor(r6)
r6.add_neighbor(r5)
graph.append( (5, 6, 10) )

print "connecting r6 to r7: "
r6.add_neighbor(r7)
r7.add_neighbor(r6)
graph.append( (6, 7, 7) )

print "connecting r7 to r8: "
r7.add_neighbor(r8)
r8.add_neighbor(r7)
graph.append( (7, 8, 1) )

print "connecting r7 to r9: "
r7.add_neighbor(r9)
r9.add_neighbor(r7)
graph.append( (7, 9, 8) )

print "connecting r8 to r10: "
r8.add_neighbor(r10)
r10.add_neighbor(r8)
graph.append( (8, 10, 11) )

print "connecting r9 to r10: "
r9.add_neighbor(r10)
r10.add_neighbor(r9)
graph.append( (9, 10, 2) )

for x in r6.neighbors:
  print x


def draw_graph():

    G=nx.Graph()

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


    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

draw_graph()


print "Welcome to our Network Emulator!"
time.sleep(1)
print "This simulator provides blah blah blah" # @FIXME: WRITE A DESCRIPTION
time.sleep(1)

rDrop = input("Enter a router id to drop(integer): ")

# Drop router:

for x in routers[rDrop - 1].neighbors:
  routers[x[0]-1].drop_neighbor(rDrop)

print "neighbors of r5:"
for x in r5.neighbors:
  print x

print "neighbors of r4:"
for x in r4.neighbors:
  print x

print "neighbors of r7:"
for x in r7.neighbors:
  print x