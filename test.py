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