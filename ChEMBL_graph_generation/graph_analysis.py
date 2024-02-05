import matplotlib.pyplot as plt
import networkx as nx

def analyse_graph(G, phase = True):
    # Basic Analysis
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")

    # Degree Distribution
    if phase == True:
        degrees = [G.degree(n) for n in G.nodes() if G.nodes[n]['node_type'] != 'phase']
        plt.hist(degrees, bins='auto')
        plt.title('Degree Distribution Excluding Phase Nodes')
        plt.xlabel('Degree')
        plt.ylabel('Number of Nodes')
        plt.show()

    else:
        degrees = [G.degree(n) for n in G.nodes()]
        plt.hist(degrees, bins='auto')
        plt.title('Degree Distribution')
        plt.xlabel('Degree')
        plt.ylabel('Number of Nodes')
        plt.show()

    # Connected Components
    num_connected_components = nx.number_connected_components(G)
    print(f"Number of connected components: {num_connected_components}")

    # Largest Connected Component
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc)
    print(f"Number of nodes in the largest connected component: {subgraph.number_of_nodes()}")
    print(f"Number of edges in the largest connected component: {subgraph.number_of_edges()}")

    # Centrality Measures
    # Degree Centrality for a subset of nodes to limit output size
    subset_of_nodes = list(G.nodes())[:10]  # First 10 nodes
    degree_centrality = nx.degree_centrality(G)
    for node in subset_of_nodes:
        print(f"Degree centrality for {node}: {degree_centrality[node]}")