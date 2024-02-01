import pandas as pd

def load_data(filename):
    return pd.read_csv(filename)

def clean_data(df):
    # Handle missing values or placeholders like 'None'
    df['clinical_trial_stages'] = df['clinical_trial_stages'].replace({'None': None})
    df.dropna(subset=['compound_ids', 'clinical_trial_stages'], how='all', inplace=True)
    
    return df

def expand_data(df):
    rows = []
    for _, row in df.iterrows():
        # Check if compound_ids is a string to ensure it can be split
        compound_ids = row['compound_ids'].split(', ') if isinstance(row['compound_ids'], str) else []
        
        # Similarly, check for clinical_trial_stages
        stages = row['clinical_trial_stages'].split(', ') if isinstance(row['clinical_trial_stages'], str) else []
        
        # Ensure we have a stage for each compound_id; use None where stages are missing
        max_length = max(len(compound_ids), len(stages))
        compound_ids += [None] * (max_length - len(compound_ids))
        stages += [None] * (max_length - len(stages))

        for compound_id, stage in zip(compound_ids, stages):
            new_row = row.to_dict()
            new_row['compound_ids'] = compound_id
            # Convert 'None' string to actual None type for consistency
            new_row['clinical_trial_stages'] = stage if stage != 'None' else 0
            rows.append(new_row)
    
    new_df = pd.DataFrame(rows)
    return new_df


def process_data(filename):
    df = load_data(filename)
    df_clean = clean_data(df)
    df_expanded = expand_data(df_clean)
    
    # Save the processed and expanded data for visualization
    #df_expanded.to_csv('processed_data2.csv', index=False)
    return df_expanded


def main():
    # Define the path to your input data file
    input_filename = 'assay_data.csv'
    # Process the data
    processed_df = process_data(input_filename)
    # Define the path to save your processed data
    output_filename = 'processed_data.csv'
    processed_df.to_csv(output_filename, index=False)
    print(f"Data processed and saved to {output_filename}")

if __name__ == "__main__":
    main()
