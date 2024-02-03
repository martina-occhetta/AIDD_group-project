import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
import re

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

def topic_modeling_on_assay_descriptions_w_bert(assay_descriptions):
    """
    Hollistic view of the topic_modeling process using BERTopic:

    Embedding documents: This step involves converting the assay descriptions into numerical representations called embeddings. Embeddings capture the semantic meaning of the text by mapping it to a high-dimensional vector space.

    Reducing dimensionality of embeddings: After embedding the documents, the dimensionality of the embeddings is reduced to a lower-dimensional space. This is done to simplify the data and remove noise, while still preserving the important information.

    Clustering reduced embeddings into topics: The reduced embeddings are then clustered together based on their similarity. This helps in grouping similar assay descriptions together and forming topics.

    Tokenization of topics: Once the topics are formed, they are tokenized into individual words or phrases. Tokenization breaks down the topics into smaller units for further analysis.

    Weight tokens: Each token within a topic is assigned a weight based on its importance or relevance within the topic. This helps in identifying the key terms or concepts within each topic.

    Represent topics with one or multiple representations: Finally, the topics are represented using one or multiple representations. This can include summarizing the topics with a few representative words or phrases, or using more complex representations such as word clouds or visualizations.
    """
    vectorizer_model = CountVectorizer(stop_words="english")
    topic_model = BERTopic(vectorizer_model=vectorizer_model)

    topics, probabilities = topic_model.fit_transform(assay_descriptions)
    return topics, probabilities


def preprocessing(assay_df):
    assay_df['descriptions_processed'] = \
    assay_df['description'].map(lambda x: re.sub('[,\.!?]', '', x))
    # Convert the titles to lowercase
    assay_df['descriptions_processed'] = assay_df['descriptions_processed'].map(lambda x: x.lower())
    return assay_df

def topic_modeling_on_assay_descriptions_w_lda(assay_df):
    
    assay_df = preprocessing(assay_df)
    return

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
