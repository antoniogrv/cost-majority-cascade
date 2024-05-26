import networkx as nx
import matplotlib.pyplot as plt

import cost_seeds_greedy_algorithm as alg
import cost_functions as cf
import submodular_functions as sf
import network_loader as nl 

G = nl.read_network("generated_networks/graph.EDGES","generated_networks/graph.CIRCLES")

# Disegno del grafo
nx.draw(G, with_labels=True)
plt.show()

#Questa funzione va chiamata solo nel caso in cui la funzione di costo scelta è la prima
cf.initialize_cost_map(G)

print("La mappa dei costi è stata inizializzata con successo!")

cf.print_cost_map()

k = 6

result = alg.cost_seeds_greedy(G, k, cf.first, sf.first, verbose=True)

print(result)



