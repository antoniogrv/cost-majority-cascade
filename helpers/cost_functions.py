import math
import random

from networkx import Graph

class CostFunctionFactory():
    def __init__(self, selected_algorithm_index, graph, range_min, range_max, d_max, verbose = False):
        self.selected_algorithm_index = selected_algorithm_index

        self.G = graph
        self.range_min = range_min
        self.range_max = range_max
        self.d_max = d_max

        self.verbose = verbose

        self.cost_map = self.create_cost_map()


    def print_cost_map(self):
        for node, cost in self.cost_map.items():
            print(f"Nodo: {node}, Costo: {cost}")
        

    def first(self, graph: Graph, v):
        if isinstance(v, list):
            costSum = 0

            for u in v:
                costSum += self.cost_map[u]
            return costSum
        else:
            return self.cost_map[v]


    def second(self, G: Graph, v):
        if isinstance(v, list):
            costSum = 0

            for u in v:
                costSum += math.ceil(G.degree(u) / 2)
            return costSum
        else:
            return math.ceil(G.degree(v) / 2)


    def third(self, G: Graph, v):
        if isinstance(v, list):
            costSum = 0

            for u in v:
                costSum += math.ceil((G.degree(u) ** 2) / self.d_max)
            return costSum
        else:
            return math.ceil((G.degree(v) ** 2) / self.d_max)
        

    def create_cost_map(self):
        cost_map = {}

        for node in list(self.G.nodes()):
            cost_map[node] = random.randint(
                self.range_min, 
                self.range_max
            )

        self.cost_map = cost_map
        
        #if self.verbose:
        #    self.print_cost_map()

        return cost_map
    
    
    def get_function(self):
        if self.selected_algorithm_index not in [1, 2, 3]:
            raise IndexError("La funzione di costo indicata non è valida.")

        if self.selected_algorithm_index == 1:
            fn = self.first
        elif self.selected_algorithm_index == 2:
            fn = self.second
        elif self.selected_algorithm_index == 3: # Custom Function Cost
            fn = self.third

        return fn