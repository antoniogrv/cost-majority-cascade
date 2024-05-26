import math

def first(G,s):
    sum = 0
    for v in list(G.nodes()):
        first_term = len(list(set(list(G.neighbors(v))) & set(s)))
        second_term = math.ceil(G.degree(v)/2)
        sum += min(first_term,second_term)
    return sum

def second(G,s):
    sum = 0
    for v in list(G.nodes()):
        for i in range(1, len(list(set(list(G.neighbors(v))) & set(s))) + 1):
            first_term = math.ceil(G.degree(v)/2) - i + 1
            second_term = 0
            sum += max(first_term,second_term)
    return sum

def third(G,s):
    sum = 0
    for v in list(G.nodes()):
        for i in range(1, len(list(set(list(G.neighbors(v))) & set(s))) + 1):
            first_term = (math.ceil(G.degree(v)/2) - i + 1)/(G.degree(v) - i + 1)
            second_term = 0
            sum += max(first_term,second_term)
    return sum
