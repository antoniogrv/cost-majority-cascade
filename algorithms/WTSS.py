from collections import Counter
import math

def assign_treshold(G):
    for node in G.nodes():
        G.nodes[node]["t"] = math.ceil(G.degree(node)/2)

def costs(G, cost_function: callable):
    for node in G.nodes():
        G.nodes[node]["cost"] = cost_function(G,node)

def print_costs(G):
    for node in G.nodes():
        print("Costo del nodo",node,":",G.nodes[node]["cost"])

def print_tresholds(G):
    for node in G.nodes():
        print("Treshold del nodo",node,":",G.nodes[node]["t"])

def WTSS(G,k, cost_function: callable):
    #assegno un valore di soglia ed un costo ai nodi del grafo
    G_copy = G.copy()
    assign_treshold(G_copy)
    costs(G_copy, cost_function)

    #inizialmente il seedset è vuoto
    seed_set = []
    to_delete = None
    third_case_node_selection = Counter()

    #G.degree(u) -> grado del nodo u
    
    sum = 0

    while len(G_copy.nodes()) > 0:

        first_case_activated = False

        for node in G_copy.nodes():
            if G_copy.nodes[node]["t"] == 0:
                first_case_activated = True
                to_delete = node
                neighbors = list(G_copy.neighbors(node))
                for neighbor in neighbors:
                    treshold = G_copy.nodes[neighbor]["t"]
                    G_copy.nodes[neighbor]["t"] = max(0,(treshold - 1))
                G_copy.remove_node(to_delete)
                break
        
        if first_case_activated:
            continue

        second_case_activated = False

        for node in G_copy.nodes():
            if G_copy.degree(node) < G_copy.nodes[node]["t"]:
                second_case_activated = True
                seed_set.append(node)
                sum += G_copy.nodes[node]["cost"]
                to_delete = node
                neighbors = list(G_copy.neighbors(node))
                for neighbor in neighbors:
                    treshold = G_copy.nodes[neighbor]["t"]
                    G_copy.nodes[neighbor]["t"] -= 1
                G_copy.remove_node(to_delete)
                break
        
        if second_case_activated: 
            continue

        third_case_node_selection = Counter()
        for node in G_copy.nodes():
            cost = G_copy.nodes[node]["cost"]
            threshold = G_copy.nodes[node]["t"]
            degree = G_copy.degree(node)
            third_case_node_selection[node] = ((cost * threshold) / (degree * (degree + 1)))
        to_delete = max(third_case_node_selection, key=third_case_node_selection.get)
        G_copy.remove_node(to_delete)

        if sum > k:
            return seed_set[:-1]
    return seed_set



        
