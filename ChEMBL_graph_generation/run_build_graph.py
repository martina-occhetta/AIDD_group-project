from data_loader import load_processed_data
from graph_construction import build_graph
from graph_analysis import analyse_graph
from graph_visualisation import visualise_largest_cc

def main():
    df_graph = load_processed_data('processed_data.csv')
    print('Data loaded \nBuilding graph...')
    G = build_graph(df_graph, phase=True)
    print('Graph built \nAnalysing graph...')
    analyse_graph(G)
    print('Graph analysed \nVisualising largest connected component...')
    visualise_largest_cc(G)

if __name__ == "__main__":
    main()
