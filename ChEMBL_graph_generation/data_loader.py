import pandas as pd

def load_processed_data(filename):
    df_graph = pd.read_csv(filename)

    # Replace NaN/None values in 'clinical_trial_stages' column with 0
    df_graph['clinical_trial_stages'] = df_graph['clinical_trial_stages'].fillna(0)

    return df_graph
