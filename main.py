import argparse
import networkx as nx
import matplotlib.pyplot as plt

from helpers.spreading_algorithm import SpreadingAlgorithm

import helpers.cost_functions as cf
import helpers.network_loader as nl
import helpers.spreading_algorithm as sa
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

        parser.add_argument('-cf', '--cost_function', default = config.DEFAULT_COST_FUNCTION, choices = ['1', '2', '3'])
        parser.add_argument('-sf', '--submodular_function', default = config.DEFAULT_SUBMODULAR_FUNCTION, choices = ['1', '2', '3'])
        parser.add_argument('-a', '--algorithm', default = config.DEFAULT_ALGORITHM, choices = ['1', '2', '3'])

        args = parser.parse_args()

        print(f"Caricati i nodi da {args.circles}")
        print(f"Caricati gli archi da {args.edges}")

        return args


class SpreadingProcess():
    def __init__(self, options: argparse.Namespace):
        self.options: argparse.Namespace = options

        self.G: Graph = self.setup_graph()
        self.k: int = self.options.threshold
        self.cost_function: callable = self.setup_cost_function()
        self.spreading_algorithm: SpreadingAlgorithm = self.setup_spreading_algorithm()


    # Per selezionare liste di nodi ed archi differenti, usare le opzioni -c (--circles) ed -e (--edges)
    def setup_graph(self) -> Graph:
        graph: Graph = nl.read_network(
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
        selected_algorithm_index: int = int(self.options.cost_function) # Rappresenta la funzione di costo scelta (1, 2 o 3)

        cost_function_factory: cf.CostFunctionFactory = cf.CostFunctionFactory(
            selected_algorithm_index = selected_algorithm_index,
            graph = self.G,
            range_min = config.DEFAULT_RANGE_MIN,
            range_max = config.DEFAULT_RANGE_MAX,
            d_max = max(dict(self.G.degree()).values()),
            verbose = self.options.verbose
        )
        
        return cost_function_factory.get_function()


    # Per selezionare un algoritmo, usare l'opzione -a oppure --algorithm, es. -a 1 (valori ammessi: 1, 2, 3)
    def setup_spreading_algorithm(self) -> SpreadingAlgorithm:
        selected_algorithm_index: int = int(self.options.algorithm) # Rappresenta l'algoritmo scelto (1, 2 o 3)

        """
        Questa variabile rappresenta la funzione submodulare selezionata tramite l'opzione -sf oppure --submodular--function (valori ammessi: 1, 2, 3).
        La funzione entra in gioco solo nel caso dell'algoritmo Cost-Seeds-Greedy, ma viene ugualmente pre-impostato ad un valore di default.
        """
        selected_submodular_function_index: int = int(self.options.submodular_function) 

        spreading_algorithm: SpreadingAlgorithm = SpreadingAlgorithm(
            selected_algorithm_index = selected_algorithm_index,
            selected_submodular_function_index = selected_submodular_function_index,
            graph = self.G,
            threshold = self.k,
            cost_function = self.cost_function,
            verbose = self.options.verbose
        )

        return spreading_algorithm
    

if __name__ == "__main__":
    spreading_process: SpreadingProcess = SpreadingProcess(options = setup_options())

    seed_set = \
         spreading_process   \
        .spreading_algorithm \
        .get_seed_set()

    print(seed_set)