from networkx import Graph


def cost_seeds_greedy(graph: Graph, threshold: int, cost_function, submodular_function, verbose: bool):
    Sd = []
    Sp = []
    step = 0

    while cost_function(graph, Sd) <= threshold:
        if verbose:
            print(f"[COST_SEEDS_GREEDY - STEP {step}] : Sp = {Sp}")
            print(f"[COST_SEEDS_GREEDY - STEP {step}] : Sd = {Sd}")
            print(f"[COST_SEEDS_GREEDY - STEP {step}] : c(Sd) = {cost_function(graph, Sd)} <= {threshold} ... proceeding")
        
        u = argmaxselect(graph, submodular_function, Sd, cost_function, verbose)
        Sp = Sd.copy()
        Sd.append(u)
        step = step + 1

    return Sp

def argmaxselect(G, submodular_function, Sd, cost_function, verbose):
    if verbose:
        print("\t[ARGMAXSELECT] : Finding best node to insert in the target set...")
    tempSet = list(G.nodes())
    if verbose:
        print("\t[ARGMAXSELECT] : V = ", tempSet)
        print("\t[ARGMAXSELECT] : Sd = ", Sd)
    set = tempSet.copy()
    for u in tempSet:
        if u in Sd:
            set.remove(u)
    #operiamo sull'insieme set, che rappresenta l'insieme V-Sd
    if verbose:
        print("\t[ARGMAXSELECT] : V-Sd = ", set)
    # Verifica se Sd è vuoto
    if not set:
        if verbose:
            print("\t[ARGMAXSELECT] : V-Sd is empty!")
        return None  # Restituisci None se set è vuoto

    bestNode = set[0]
    bestValue = 0.0
    for v in set:
        if verbose:
            print("\n\t[ARGMAXSELECT] : f(Sd U ",v,") = ", submodular_function(G, Sd + [v]))
            print("\t[ARGMAXSELECT] : f(Sd) = ", submodular_function(G, Sd))
            print("\t[ARGMAXSELECT] : c(",v,") = ", cost_function(G,v))

        value = (submodular_function(G, Sd + [v]) - submodular_function(G, Sd)) / cost_function(G,v)

        if verbose:
            print("\t[ARGMAXSELECT] : value = ", value)
        if value>bestValue:
            bestValue = value
            bestNode = v
            if verbose:
                print("\t[ARGMAXSELECT] : bestValue(bestNode) was changed = ", value)
        if verbose:
            print("\t[ARGMAXSELECT] : bestValue(bestNode) = ", bestValue, "(", bestNode,")")
    if verbose:
        print("\t[ARGMAXSELECT] : FINAL bestValue(bestNode) = ", bestValue, "(", bestNode,")")
    return bestNode