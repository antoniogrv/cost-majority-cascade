import math
import random

#Valori minimi e massimi per il range utilizzato dalla prima funzione di costo
range_min = 1
range_max = 10

cost_map = {}

#Questa funzione va invocata una sola volta, prima di ogni esperimento in cui la funzione di costo scelta è la prima funzione di costo
def initialize_cost_map(G):
    for node in list(G.nodes()):
        cost_map[node] = random.randint(range_min, range_max)

def print_cost_map():
    for node, cost in cost_map.items():
        print(f"Nodo: {node}, Costo: {cost}")
    

def first(G,v):
    if isinstance(v, list):

        costSum = 0
        for u in v:
            costSum+=cost_map[u]
        return costSum
    else:
        return cost_map[v]

def second(G,v):
    if isinstance(v, list):
        costSum = 0
        for u in v:
            costSum+=math.ceil(G.degree(u)/2)
        return costSum
    else:
        return math.ceil(G.degree(v)/2)

'''
#To be defined
def third(G,v):
    return ...;
'''