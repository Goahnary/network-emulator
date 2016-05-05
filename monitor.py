from router import Router
import networkx as nx
import matplotlib.pyplot as plt

print "() = weight"

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
graph.append( (1, 2, 5) )

print "connecting r2 to r3: "
r2.add_neighbor(r3)
graph.append( (2, 3, 2) )

print "connecting r3 to r4: "
r3.add_neighbor(r4)
graph.append( (3, 4, 9) )

print "connecting r3 to r5: "
r3.add_neighbor(r5)
graph.append( (3, 5, 1) )

print "connecting r4 to r6: "
r4.add_neighbor(r6)
graph.append( (4, 6, 1) )

print "connecting r5 to r6: "
r5.add_neighbor(r6)
graph.append( (5, 6, 10) )

print "connecting r6 to r7: "
r6.add_neighbor(r7)
graph.append( (6, 7, 7) )

print "connecting r7 to r8: "
r7.add_neighbor(r8)
graph.append( (7, 8, 1) )

print "connecting r7 to r9: "
r7.add_neighbor(r9)
graph.append( (7, 9, 8) )

print "connecting r8 to r10: "
r8.add_neighbor(r10)
graph.append( (8, 10, 11) )

print "connecting r9 to r10: "
r9.add_neighbor(r10)
graph.append( (9, 10, 2) )

for x in r3.neighbors:
	print x


def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1], edge[2]) # (edge1, edge2, weight)

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # show graph
    plt.show()

G=nx.path_graph(10)
length,path=nx.single_source_dijkstra(G,1,10)

# print length[10]
print path[10]

