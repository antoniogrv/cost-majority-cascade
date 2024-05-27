import networkx as nx
import random

n = 100
p = 0.05

G = nx.erdos_renyi_graph(n, p)

# Salva gli archi del grafo nel file .EDGES
with open('networks/generated_networks/graph.EDGES', 'w') as edges_file:
    for edge in G.edges():
        edges_file.write(f"{edge[0]} {edge[1]}\n")

# Assegna casualmente i nodi ai cerchi e salva queste informazioni nel file .CIRCLES
circles = {}

for node in G.nodes():
    circle_id = f"circle_{random.randint(1, 5)}"  # Assegna casualmente il nodo a uno dei 5 cerchi
    if circle_id not in circles:
        circles[circle_id] = []
    circles[circle_id].append(str(node))

with open('networks/generated_networks/graph.CIRCLES', 'w') as circles_file:
    for circle_id, members in circles.items():
        circles_file.write(f"{circle_id} {' '.join(members)}\n")