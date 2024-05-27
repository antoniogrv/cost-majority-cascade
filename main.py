import argparse
import networkx as nx
import matplotlib.pyplot as plt

import cost_seeds_greedy_algorithm as alg
import cost_functions as cf
import submodular_functions as sf
import network_loader as nl 
import default_config as config

from networkx import Graph

# Consultare il README per le possibili configurazioni dello script
def setup_options():
        parser = argparse.ArgumentParser()

        parser.add_argument('-g', '--print_graph', action = 'store_true')
        parser.add_argument('-v', '--verbose', action = 'store_true')

        parser.add_argument('-k', '--threshold', default = config.DEFAULT_THRESHOLD)
        parser.add_argument('-e', '--edges', default = config.DEFAULT_EDGES)
        parser.add_argument('-c', '--circles', default = config.DEFAULT_CIRCLES)

        parser.add_argument('-cf', '--cost_function', default = '1', choices = ['1', '2', '3'])
        parser.add_argument('-a', '--algorithm', default = '1', choices = ['1', '2', '3'])

        args = parser.parse_args()

        print(f"Caricati i nodi da {args.circles}")
        print(f"Caricati gli archi da {args.edges}")

        return args

class Runner():
    def __init__(self, options):
        self.options = options

        self.G = self.setup_graph()
        self.k = self.options.threshold
        self.cost_function = self.setup_cost_function()
        self.algorithm = self.setup_algorithm()


    # Per selezionare liste di nodi ed archi differenti, usare le opzioni -c (--circles) ed -e (--edges)
    def setup_graph(self) -> Graph:
        graph = nl.read_network(
            edges_file_path = self.options.edges,
            circles_file_path = self.options.circles
        )

        # Per stampare il grafo, usare l'opzione -g oppure --print_graph
        if self.options.print_graph:
            nx.draw(graph, with_labels = True)
            plt.show()

        return graph


    # Per selezionare una funzione di costo, usare l'opzione -cf oppure --cost-function, es. -cf 1 (valori ammessi: 1, 2, 3)
    def setup_cost_function(self) -> callable:
        choice = int(self.options.cost_function)
        
        if choice == 1:
            cost_function = cf.first

            cf.initialize_cost_map(self.G)

            if self.options.verbose:
                cf.print_cost_map()
        elif choice == 2:
            cost_function = cf.second
        
        return cost_function


    # Per selezionare un algoritmo, usare l'opzione -a oppure --algorithm, es. -a 1 (valori ammessi: 1, 2, 3)
    def setup_algorithm(self) -> callable:
        choice = int(self.options.algorithm)

        # Cost-Seeds-Greedy
        if choice == 1:
            algorithm = alg.cost_seeds_greedy

        return algorithm
    
    # Restituisce il seed set massimale S così come individuato dall'algoritmo in base al threshold e alla funzione di costo
    def get_seed_set(self):
        seed_set = self.algorithm(
            graph = self.G,
            threshold = self.k,
            cost_function = self.cost_function, 
            submodular_function = sf.first, 
            verbose = self.options.verbose
        )

        return seed_set
    

if __name__ == "__main__":
    runner = Runner(options = setup_options())

    seed_set = runner.get_seed_set()

    print(seed_set)