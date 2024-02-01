import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_processed_data(filename):
    return pd.read_csv(filename)

def plot_assay_counts_by_stage(df):
    df_grouped = df.groupby('clinical_trial_stages')['assay_chembl_id'].nunique().reset_index()
    df_grouped.rename(columns={'assay_chembl_id': 'unique_assay_count'}, inplace=True)

    # Using matplotlib to create the bar plot
    plt.figure(figsize=(10, 6))  # Optional: Adjust figure size
    plt.bar(df_grouped['clinical_trial_stages'], df_grouped['unique_assay_count'])
    plt.title('Unique Assays Count by Clinical Trial Stage')
    plt.xlabel('Clinical Trial Stage')
    plt.ylabel('Unique Assay Count')
    plt.xticks(rotation=0)  # Optional: Rotate x-axis labels if they're lengthy
    plt.tight_layout()  # Optional: Adjust layout to not cut off labels
    plt.show()

def plot_compound_distribution(df):
    # Assuming 'compound_ids' column exists and you're counting its occurrences
    compound_counts = df['compound_ids'].value_counts()

    plt.figure(figsize=(10, 6))  # Optional: Adjust figure size
    plt.hist(compound_counts, bins=50)  # You can adjust the number of bins
    plt.title('Distribution of Compounds Across Assays')
    plt.xlabel('Number of Assays per Compound')
    plt.ylabel('Number of Compounds')
    #plt.ylim([0, 500])  # Optional: Adjust y-axis range
    plt.tight_layout()  
    plt.show()

def plot_assay_type_distribution(df):
    assay_type_counts = df['assay_type'].value_counts()
    plt.figure(figsize=(10, 6))
    assay_type_counts.plot(kind='bar')
    plt.title('Distribution of Assay Types')
    plt.xlabel('Assay Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_heatmap(df):
    df_filtered = df[~df['clinical_trial_stages'].isin([0, -1])]
    # Creating a pivot table for the heatmap
    heatmap_data = pd.pivot_table(df_filtered, values='assay_chembl_id', 
                                index='assay_type', 
                                columns='clinical_trial_stages', 
                                aggfunc='count', 
                                fill_value=0)

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu')
    plt.title('Heatmap of Assays by Clinical Trial Stage')
    plt.xlabel('Clinical Trial Stage')
    plt.ylabel('Assay Type')
    plt.show()

def main():
    df = load_processed_data('processed_data.csv')
    plot_assay_counts_by_stage(df)
    plot_compound_distribution(df)
    plot_assay_type_distribution(df)
    plot_heatmap(df)  # Only if heatmap data is available

if __name__ == "__main__":
    main()
