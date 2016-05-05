import monitor
import networkx as nx
import matplotlib.pyplot as plt
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

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):


    # create networkx graph
    G=nx.Graph()
    pos=nx.spring_layout(G) 


    G.add_node(r1)
    G.add_node(r2)
    G.add_node(r3)
    G.add_node(r3)
    G.add_node(r4)
    G.add_node(r5)
    G.add_node(r6)
    G.add_node(r7)
    G.add_node(r8)
    G.add_node(r9)



    G.add_edge(r1,r2)

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



    # show graph
    plt.show()

graph = [(r1,r2), (r3,r4), (r5,r6), (r7,r8), (r8,r9)]

# you may name your edge labels
labels = map(chr, range(65, 65+len(graph)))
#draw_graph(graph, labels)

# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
draw_graph(graph)