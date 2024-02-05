import networkx as nx
import matplotlib.pyplot as plt


def visualise_largest_cc(G, phase = True):
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc)
    pos = nx.spring_layout(subgraph, seed=42)
    if phase == True:
        # Create a color map based on node types
        node_colors = []
        for node, data in subgraph.nodes(data=True):
            if data['node_type'] == 'compound':
                node_colors.append('orange')  # Color for compounds
            elif data['node_type'] == 'assay':
                node_colors.append('lightblue')  # Color for assays
            elif data['node_type'] == 'phase':
                node_colors.append('red')  # Color for phases

        # Draw the network
        plt.figure(figsize=(12, 12))
        nx.draw_networkx(subgraph, pos, with_labels=False, node_size=20, alpha=0.5,
                        node_color=node_colors)  # Use the color map
        plt.title("Largest Connected Component")
        plt.axis('off')  # Hide axes
        plt.show()

    else:
        node_colors = []
        for node, data in subgraph.nodes(data=True):
            if data['node_type'] == 'compound':
                node_colors.append('orange')  # Color for compounds
            elif data['node_type'] == 'assay':
                node_colors.append('lightblue')  # Color for assays

        # Draw the network
        plt.figure(figsize=(12, 12))
        nx.draw_networkx(subgraph, pos, with_labels=False, node_size=20, alpha=0.5,
                        node_color=node_colors)  # Use the color map
        plt.title("Largest Connected Component")
        plt.axis('off')  # Hide axes
        plt.show()