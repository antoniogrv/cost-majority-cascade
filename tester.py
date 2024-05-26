import networkx as nx
import network_loader as nl
import matplotlib.pyplot as plt

G = nl.read_network("generated_networks/graph.EDGES","generated_networks/graph.CIRCLES")

# Disegno del grafo
nx.draw(G, with_labels=True)
plt.show()

for v in list(G.nodes()):
    print(G.degree(v))
