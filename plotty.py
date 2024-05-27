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

from main import SpreadingProcess


k_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
cost_functions = [1, 2, 3]
submodular_functions = [1, 2, 3]
algorithms = [1, 2, 3]

inf_sizes_csg = [[[0 for _ in range(len(submodular_functions))] for _ in range(len(cost_functions))] for _ in range(len(k_list))]
inf_sizes_wtss = [[0 for _ in range(len(cost_functions))] for _ in range(len(k_list))]
inf_sizes_custom = [[0 for _ in range(len(cost_functions))] for _ in range(len(k_list))]

class Options:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def print_results(list):
    with open(f"results/plots/data.txt", "a") as file:
        file.write(f"{list}\n")

if __name__ == "__main__": 
    if not os.path.exists("results"):
        os.makedirs("results")

    if not os.path.exists("results/plots"):
        os.makedirs("results/plots")

    """
    CSG
    """
    for i, k in enumerate(k_list):
        for j, cost_function in enumerate(cost_functions):
            for z, submodular_function in enumerate(submodular_functions):
                print(f"###### CSG - k: {k}, cost_function: {cost_function}, submodular_function: {submodular_function} ######")

                options = Options(
                    print_graph=False,
                    verbose=False,
                    save=False,
                    threshold=k,
                    edges='networks/generated_networks/graph.EDGES',
                    circles='networks/generated_networks/graph.CIRCLES',
                    cost_function=cost_function,
                    submodular_function=submodular_function,
                    algorithm=1
                )

                spreading_process: SpreadingProcess = SpreadingProcess(options)

                seed_set: list = \
                    spreading_process   \
                    .spreading_algorithm \
                    .get_seed_set()
                        
                cascade_process: CascadeProcess = CascadeProcess(
                    graph = spreading_process.G, 
                    seed_set = seed_set,
                    verbose = spreading_process.options.verbose
                )

                influenced_nodes: list = \
                    cascade_process \
                    .get_influenced_nodes()

                print(f"Influenced Nodes: {influenced_nodes}")

                inf_sizes_csg[i][j][z] = len(influenced_nodes)

                print_results(inf_sizes_csg)

    for j, submodular_function in enumerate(submodular_functions):
        for z, cost_function in enumerate(cost_functions):
            label = f"Funzione di costo {cost_function}"
            plt.plot(k_list, [row[j][z] for row in inf_sizes_csg], label=label)
        
        plt.xlabel('Budget (k)')
        plt.ylabel('Numero di nodi influenzati')
        plt.title(f'CSG - Numero di nodi influenzati rispetto al budget k (funzione submodulare {submodular_function})')
        plt.legend()
        plt.show()



    """
    WTSS
    """
    for i, k in enumerate(k_list):
        for j, cost_function in enumerate(cost_functions):
            print(f"###### WTSS - k: {k}, cost_function: {cost_function} ######")

            options = Options(
                print_graph=False,
                verbose=False,
                save=False,
                threshold=k,
                edges='networks/generated_networks/graph.EDGES',
                circles='networks/generated_networks/graph.CIRCLES',
                cost_function=cost_function,
                submodular_function=1,
                algorithm=2
            )

            spreading_process: SpreadingProcess = SpreadingProcess(options)

            seed_set: list = \
                spreading_process   \
                .spreading_algorithm \
                .get_seed_set()
                        
            cascade_process: CascadeProcess = CascadeProcess(
                graph = spreading_process.G, 
                seed_set = seed_set,
                verbose = spreading_process.options.verbose
            )

            influenced_nodes: list = \
                cascade_process \
                .get_influenced_nodes()

            print(f"Influenced Nodes: {influenced_nodes}")

            inf_sizes_wtss[i][j] = len(influenced_nodes)
            print("Matrice", inf_sizes_wtss)


    for j, cost_function in enumerate(cost_functions):
        label = f"Funzione di costo {cost_function}"
        plt.plot(k_list, [row[j] for row in inf_sizes_wtss], label = label)

        plt.xlabel('Budget (k)')
        plt.ylabel('Numero di nodi influenzati')
        plt.title('WTSS - Numero di nodi influenzati rispetto al budget k')

    plt.legend()
    plt.show()

    """
    MySeeds
    """
    for i, k in enumerate(k_list):
        for j, cost_function in enumerate(cost_functions):
            print(f"###### MySeeds - k: {k}, cost_function: {cost_function} ######")

            options = Options(
                print_graph=False,
                verbose=False,
                save=False,
                threshold=k,
                edges='networks/generated_networks/graph.EDGES',
                circles='networks/generated_networks/graph.CIRCLES',
                cost_function=cost_function,
                submodular_function=1,
                algorithm=3
            )

            spreading_process: SpreadingProcess = SpreadingProcess(options)

            seed_set: list = \
                spreading_process   \
                .spreading_algorithm \
                .get_seed_set()
                        
            cascade_process: CascadeProcess = CascadeProcess(
                graph = spreading_process.G, 
                seed_set = seed_set,
                verbose = spreading_process.options.verbose
            )

            influenced_nodes: list = \
                cascade_process \
                .get_influenced_nodes()

            print(f"Influenced Nodes: {influenced_nodes}")

            inf_sizes_custom[i][j] = len(influenced_nodes)

            print(inf_sizes_custom)


    for j, cost_function in enumerate(cost_functions):
        label = f"Funzione di costo {cost_function}"
        plt.plot(k_list, [row[j] for row in inf_sizes_custom], label = label)

        plt.xlabel('Budget (k)')
        plt.ylabel('Numero di nodi influenzati')
        plt.title('MySeeds - Numero di nodi influenzati rispetto al budget k')

    plt.legend()
    plt.show()


