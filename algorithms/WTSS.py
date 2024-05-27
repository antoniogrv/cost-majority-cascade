from collections import Counter

def assign_treshold(G):
    for node in G.nodes():
        G.nodes[node]["t"] = G.degree(node)/2

def costs(G, cost_function: callable):
    for node in G.nodes():
        G.nodes[node]["cost"] = cost_function(G,node)

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
    while len(seed_set) < k :
        

        for node in G_copy.nodes():
            #Caso 1 -> Se la soglia del nodo è 0, allora a tutti i vicini imposta la soglia come 
            #il valore massimo tra 0 e la soglia meno 1
            if G_copy.nodes[node]["t"] == 0:
                to_delete = node
                neighbors = list(G_copy.neighbors(node))
                for neighbor in neighbors:
                    treshold = G_copy.nodes[neighbor]["t"]
                    G_copy.nodes[neighbor]["t"] = max(0,(treshold - 1))

            #Caso 2 -> Se il grado del nodo è minore della sua soglia, allora aggiungo il nodo al seedset
            # e diminuisco la soglia del vicinato di 1
            elif G_copy.degree(node) < G_copy.nodes[node]["t"]:
                seed_set.add(node)
                to_delete = node
                neighbors = list(G_copy.neighbors(node))
                for neighbor in neighbors:
                    treshold = G_copy.nodes[neighbor]["t"]
                    G_copy.nodes[neighbor]["t"] -= 1
                
                #Caso 3 -> Prendo il nodo con il maggior rapporto descritto da WTSS
                else: 
                    for node in G_copy.nodes():
                        cost = G_copy.nodes[node]["cost"]
                        treshold = G_copy.nodes[node]["t"]
                        degree = G_copy.degree(node)
                        third_case_node_selection[node] = ((cost * treshold) / (degree * (degree + 1))) if (degree != 0) else 0
                    
                    if len(third_case_node_selection) > 0:
                        # Prelevo il nodo con massimo rapporto calcolato
                        to_delete = max(third_case_node_selection, key=third_case_node_selection.get)

        if to_delete is not None:
            G_copy.remove_node(to_delete)

        if not G_copy.nodes:
            print("Grafo vuoto, esco dal loop")
            break

        return seed_set



        
