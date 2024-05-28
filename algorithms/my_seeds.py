import networkx
from networkx import Graph


def costs(G: Graph, cost_function: callable) -> None:
    for node in G.nodes():
        G.nodes[node]["cost"] = cost_function(G,node)


def total_cost(G: Graph) -> int:
    total_cost = 0
    
    for node in G.nodes():
        total_cost += node["cost"]


def my_seeds(G: Graph, k: int, cost_function: callable) -> list:
    costs(G, cost_function)

    sum_costs = 0
    remaining_graph = G.copy()
    seed_set = []

    while sum_costs <= k:
        selected_node = None
        best_score = 0

        for node in remaining_graph.nodes():
            score = networkx.clustering(G, node) * G.degree(node) / cost_function(G, node)

            if score > best_score:
                best_score = score
                selected_node = node

        if selected_node == None:
            break

        sum_costs += remaining_graph.nodes[node]["cost"]
        seed_set.append(selected_node)
        remaining_graph.remove_node(selected_node)
        
    return seed_set 
