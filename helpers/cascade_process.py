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
            casted_prev_influenced = [str(node) for node in prev_influenced]

            for node in self.graph.nodes():
                if node in casted_prev_influenced:
                    continue

                intersection = len([x for x in casted_prev_influenced if x in list(self.graph.neighbors(node))])

                degree_threshold = math.ceil(self.graph.degree(node) / 2)

                if self.verbose:
                    print(f"[i - {node}] Considero il nodo {node}, con {self.graph.degree(node)} vicini")
                    print(f"[i - {node}] La soglia affinché {node} venga influenzato è pari a {degree_threshold}")
                    print(f"[i - {node}] Il taglio dell'intersezione fra i vicini di {node} e i nodi influenzanti è {intersection}")
                    print(f"[i - {node}] Il nodo {node} sarà influenzato dal seed set: {intersection >= degree_threshold}\n")

                if intersection >= degree_threshold:
                    influencing.append(int(node))
        
        return influencing