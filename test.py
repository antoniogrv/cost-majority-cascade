import os
import time
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import random

from helpers.cascade_process import CascadeProcess
from helpers.spreading_algorithm import SpreadingAlgorithm

import helpers.cost_functions as cf
import helpers.network_loader as nl
import default_config as config

from networkx import Graph

from main import SpreadingProcess


k_list = [10, 20, 30]
cost_functions = [1, 2, 3]
submodular_functions = [1, 2, 3]
algorithms = [1, 2, 3]

inf_sizes_csg = []
inf_sizes_wtss = []
inf_sizes_custom = []

class Options:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def print_results(list):
    with open(f"results/plots/data.txt", "a") as file:
        file.write(f"{list}\n")

if __name__ == "__main__": 
    matrix = [[0 for _ in range(4)] for _ in range(3)]

    for i in range(3):
        for j in range(4):
            matrix[i][j] = random.randint(1, 10)

    print(matrix)

    column = [row[1] for row in matrix]

    print(column)


