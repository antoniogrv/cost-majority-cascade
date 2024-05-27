import math
from networkx import Graph
import copy


class CascadeProcess():
    def __init__(self, graph: Graph, seed_set: list, verbose: bool) -> None:
        self.graph: Graph = graph
        self.seed_set: list = seed_set
        self.verbose: bool = verbose


    def get_influenced_nodes(self) -> list:
        prev_influenced: list = []
        influencing: list = copy.deepcopy(self.seed_set)
    
        while len(influencing) != len(prev_influenced):
            if self.verbose:
                print("\n##### [i - Cascade] Iterazione successiva #####\n")

            prev_influenced: list = copy.deepcopy(influencing)

            for node in set(self.graph.nodes()).difference(prev_influenced):
                intersection = len(set(self.graph.neighbors(node)).intersection(prev_influenced))
                degree_threshold = math.ceil(self.graph.degree(node) / 2)

                if self.verbose:
                    print(f"[i - {node}] Considero il nodo {node}, con {self.graph.degree(node)} vicini")
                    print(f"[i - {node}] La soglia affinché {node} venga influenzato è pari a {degree_threshold}")
                    print(f"[i - {node}] Il taglio dell'intersezione fra i vicini di {node} e i nodi influenzanti è {intersection}")
                    print(f"[i - {node}] Il nodo {node} sarà influenzato dal seed set: {intersection >= degree_threshold}\n")

                if node in prev_influenced:
                    continue

                if intersection >= degree_threshold:
                    influencing.append(node)
        
        return influencing