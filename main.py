import argparse
import networkx as nx
import matplotlib.pyplot as plt

import cost_seeds_greedy_algorithm as alg
import cost_functions as cf
import submodular_functions as sf
import network_loader as nl 

from networkx import Graph

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--print_graph', action = 'store_true')

    return parser.parse_args()

args: argparse.Namespace = setup_args()

G: Graph = nl.read_network(
    edges_file_path = "generated_networks/graph.EDGES",
    circles_file_path = "generated_networks/graph.CIRCLES"
)

k: int = 6

# Per stampare il grafo, usare l'opzione -g o --print_graph
if args.print_graph:
    nx.draw(graph = G, with_labels = True)
    plt.show()

# Questa funzione va chiamata solo nel caso in cui la funzione di costo scelta è la prima
cf.initialize_cost_map(G)

print("La mappa dei costi è stata inizializzata con successo!")

cf.print_cost_map()

result = alg.cost_seeds_greedy(
    graph = G,
    threshold = k, 
    cost_function = cf.first, 
    submodular_function = sf.first, 
    verbose = False
)

print(result)



