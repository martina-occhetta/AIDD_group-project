## Graph Generation

This project focuses on generating and analyzing a graph based on data from ChEMBL (see ChEMBL_data_visualisation directory to see data retrieval and processing functions).
The graph represents connections between compounds and assays, including information about the maximum phase each compound has reached.

### Project Structure

The `ChEMBL_graph_generation` directory contains the following files:

- `processed_data.csv`: The dataset used for graph generation. It should contain at least the compound IDs, assay IDs, and the maximum phase reached by each compound.
- `data_loader.py`: Contains code to load the processed data from the CSV file `processed_data.csv` generated in `ChEMBL_data_visualisation`.
- `graph_construction.py`: Responsible for constructing the graph from the loaded data, adding nodes and edges based on compounds, assays, and their relationships.
- `graph_analysis.py`: Includes functions for analysing the graph, such as calculating the number of nodes and edges, and degree distribution.
- `graph_visualisation.py`: Provides functionality to visualise the largest connected component, highlighting the different types of nodes (compounds and assays) and the structure of the (sub)graph.
- `run_build_graph.py`: The main script that orchestrates the loading, construction, analysis, and visualisation of the graph.

- `graph_v2` folder: A second version of the graph, built using a differet input dataset.

### How to Run

To run the project and generate the graph along with its analysis and visualization, follow these steps:

1. Ensure you have Python installed on your system.
2. Install the necessary Python packages.
3. Navigate to the `graph` directory in your terminal or command prompt.
4. Run the `run_build_graph.py` script:
`python run_build_graph.py`
5. The script will load the data, construct the graph, perform basic analysis, and visualize the graph structure. Ensure `processed_data.csv` is in the correct format
and available in the `graph` directory for the script to function properly.






