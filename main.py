import os
import time
import argparse
import networkx as nx
import matplotlib.pyplot as plt

from helpers.cascade_process import CascadeProcess
from helpers.spreading_algorithm import SpreadingAlgorithm

import helpers.cost_functions as cf
import helpers.network_loader as nl
import default_config as config

from networkx import Graph


# Consultare il README per le possibili configurazioni dello script
def setup_options() -> None:
        parser: argparse.ArgumentParser = argparse.ArgumentParser()

        parser.add_argument('-g', '--print_graph', action = 'store_true')
        parser.add_argument('-v', '--verbose', action = 'store_true')
        parser.add_argument('-s', '--save', action = 'store_true')

        parser.add_argument('-k', '--threshold', default = config.DEFAULT_THRESHOLD)
        parser.add_argument('-e', '--edges', default = config.DEFAULT_EDGES)
        parser.add_argument('-c', '--circles', default = config.DEFAULT_CIRCLES)

        parser.add_argument('-cf', '--cost_function', default = config.DEFAULT_COST_FUNCTION, choices = ['1', '2', '3'])
        parser.add_argument('-sf', '--submodular_function', default = config.DEFAULT_SUBMODULAR_FUNCTION, choices = ['1', '2', '3'])
        parser.add_argument('-a', '--algorithm', default = config.DEFAULT_ALGORITHM, choices = ['1', '2', '3'])

        args: argparse.Namespace = parser.parse_args()

        print(f"Caricati i nodi da {args.circles}")
        print(f"Caricati gli archi da {args.edges}")

        return args


class SpreadingProcess():
    def __init__(self, options: argparse.Namespace):
        self.options: argparse.Namespace = options

        self.G: Graph = self.setup_graph()
        self.k: int = int(self.options.threshold)
        self.cost_function: callable = self.setup_cost_function()
        self.spreading_algorithm: SpreadingAlgorithm = self.setup_spreading_algorithm()

        self.results_path = f"{config.DEFAULT_RESULTS_PATH}/{time.time()}_k_{self.k}_a_{self.options.algorithm}_cf_{self.options.cost_function}"


    # Per selezionare liste di nodi ed archi differenti, usare le opzioni -c (--circles) ed -e (--edges)
    def setup_graph(self) -> Graph:
        graph: Graph = nl.read_network(
            edges_file_path = self.options.edges,
            circles_file_path = self.options.circles
    )

        # Per stampare il grafo, usare l'opzione -g oppure --print_graph
        if self.options.print_graph:
            nx.draw(G = graph, pos = nx.spring_layout(graph), with_labels = True)
            plt.show(block = False)

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


# Per abilitare il salvataggio dei dati, usare l'opzione -s oppure --save
def save_results(file_path, results, graph, seed_set, influenced_nodes):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(f"{file_path}/data.txt", "a") as file:
        file.write(f"{results}\n")

    """
    Grafico della rete senza particolari colorazioni
    """
    color_map = []

    for node in graph.nodes():
        color_map.append('gray')

    nx.draw(G = graph, with_labels = True, pos = nx.spring_layout(graph), node_color = color_map)
    plt.savefig(f"{file_path}/pre-influencing.png", format = "PNG")
    plt.clf()

    """
    Grafico che evidenzia i nodi del seed set (rossi) e i nodi rimanenti (grigio)
    """
    color_map = []

    for node in graph.nodes():
        if node in seed_set:
            color_map.append('red')
        else:
            color_map.append('gray')

    nx.draw(G = graph, with_labels = True, pos = nx.spring_layout(graph), node_color = color_map)
    plt.savefig(f"{file_path}/influencing.png", format = "PNG")
    plt.clf()

    """
    Grafico che evidenzia i nodi del seed set (rossi), i nodi influenzati dal seed set (blu) e i nodi rimanenti (grigio)
    """
    color_map = []

    for node in graph.nodes():
        if node in seed_set:
            color_map.append('red')
        elif node in influenced_nodes: 
            color_map.append('blue')
        else:
            color_map.append('gray')

    nx.draw(G = graph, with_labels = True, pos=nx.spring_layout(graph), node_color = color_map)
    plt.savefig(f"{file_path}/influencing_and_influenced.png", format = "PNG")
    plt.clf()

    print(f"Risultati salvati in {file_path}")


if __name__ == "__main__": 
    spreading_process: SpreadingProcess = SpreadingProcess(options = setup_options())

    """
    Individua il seed set massimale tale che la funzione di costo c(S) sia minore o uguale al threshold k.
    """
    seed_set: list = \
         spreading_process   \
        .spreading_algorithm \
        .get_seed_set()
    
    print(f"Seed Set: {seed_set}")

    """
    Simula il processo di diffusione a partire dal grafo G e il seed set S individuato in precedenza,
    restituendo i nodi influenzati al termine del processo (inclusivi dei nodi appartenenti al seed set).
    """
    cascade_process: CascadeProcess = CascadeProcess(
        graph = spreading_process.G, 
        seed_set = seed_set,
        verbose = spreading_process.options.verbose
    )

    influenced_nodes: list = \
         cascade_process \
        .get_influenced_nodes()

    print(f"Influenced Nodes: {influenced_nodes}")

    """
    Persiste i risultati in una cartella.
    """
    if spreading_process.options.save:
        save_results(
            file_path = f"{spreading_process.results_path}",
            results = f"Seed Set: {len(seed_set)}   Influenced Nodes: {len(influenced_nodes)}",
            graph = spreading_process.G,
            seed_set = seed_set,
            influenced_nodes = influenced_nodes
        )