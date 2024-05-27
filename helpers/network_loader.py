import networkx as nx
import matplotlib.pyplot as plt

def read_network(edges_file_path, circles_file_path):
    # Funzione per leggere i file .EDGES
    def read_edges(file_path):
        edges = []
        with open(file_path, 'r') as file:
            for line in file:
                nodes = line.strip().split()
                if len(nodes) == 2:
                    edges.append((nodes[0], nodes[1]))
        return edges

    # Funzione per leggere i file .CIRCLES
    def read_circles(file_path):
        circles = {}
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) > 1:
                    circle_id = parts[0]
                    members = parts[1:]
                    circles[circle_id] = members
        return circles

    # Funzione per creare il grafo
    def create_graph(edges, circles):
        G = nx.Graph()

        # Aggiungi gli archi al grafo
        G.add_edges_from(edges)

        # Aggiungi i cerchi come attributi dei nodi
        for circle_id, members in circles.items():
            for member in members:
                if member in G.nodes:
                    if 'circles' not in G.nodes[member]:
                        G.nodes[member]['circles'] = []
                    G.nodes[member]['circles'].append(circle_id)

        return G

    # Leggi i file
    edges = read_edges(edges_file_path)
    circles = read_circles(circles_file_path)

    # Crea il grafo
    G = create_graph(edges, circles)

    return G

def main():
    # Percorsi ai file .EDGES e .CIRCLES
    edges_file_path = 'sample_networks/0.edges'
    circles_file_path = 'sample_networks/0.circles'

    # Leggi il network
    G = read_network(edges_file_path, circles_file_path)

    # Stampa informazioni sul grafo
    print(nx.info(G))

    # Disegna il grafo
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()

if __name__ == "__main__":
    main()
