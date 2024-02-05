import networkx as nx
from tqdm import tqdm

def build_graph(df_graph, phase = True):
    G = nx.Graph()
    for _, row in tqdm(df_graph.iterrows()):
        G.add_node(row['compound_ids'], node_type='compound')
        G.add_node(row['assay_chembl_id'], node_type='assay')

        G.add_edge(row['compound_ids'], row['assay_chembl_id'])

        if phase == True:
            G.add_node(row['clinical_trial_stages'], node_type='phase')
            G.add_edge(row['compound_ids'], row['clinical_trial_stages'])  # Connect compound to its max phase

    return G
