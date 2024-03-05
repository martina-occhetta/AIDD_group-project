import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from Levenshtein import distance as levenshtein_distance
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from math import sqrt



def convert_embeddings(assay_dataframe):

    import itertools

    # pandas cannot recognise embeddings column entries as arrays, instead reads entire array as string, have to convert back
    assay_dataframe['embeddings'].replace('\[','', regex=True, inplace=True)
    assay_dataframe['embeddings'].replace('\]','', regex=True, inplace=True)
    assay_dataframe['embeddings'].replace('\n','', regex=True, inplace=True)
    assay_dataframe['embeddings'] = assay_dataframe['embeddings'].str.strip()
    assay_dataframe['embeddings'] = assay_dataframe['embeddings'].str.split(' ')

    # loops to remove empty elements from embeddings and converts embeddings to np array
    new_embeddings = []
    for embedding_list in assay_dataframe['embeddings'].values:
        # using lambda function
        embedding_list_ = list(itertools.filterfalse(lambda x: x == '', embedding_list))
        # convert list to np array
        embedding_array = np.array(embedding_list_)
        # cast elements to float
        embedding_array = embedding_array.astype(float) 
        # append to list of arrays
        new_embeddings.append(embedding_array)

    # swap in reformatted embeddings
    assay_dataframe['embeddings'] = new_embeddings

    return assay_dataframe


def generate_subset_filters(filters_1,filters_2):
    
    assay_filters_list = []
    for category in filters_1:
        for assay_type in filters_2:
            assay_filters = [category,assay_type]
            assay_filters_list.append(assay_filters)
    
    return assay_filters_list


def create_subset_dict_2(assay_data, assay_type, subset_col, disease_cell_types = None):
    
    # subset by BAO Format for specific assay type
    assay_data_subset = assay_data[assay_data["BAO Format"]==assay_type]
    # find all organisms/cell type
    category_list = assay_data_subset[subset_col].unique()
    # additional filter for disease-relevant organisms/cell types
    if disease_cell_types != None:
        category_list = list(set(category_list).intersection(disease_cell_types))
    # find all assay types (functional, toxicity, etc.)
    assay_type_list = assay_data_subset["Assay Type"].unique()
    
    assay_filters_list = generate_subset_filters(category_list,assay_type_list)

    # create a dictionary where each dataframe is associated with respective organism/cell type
    subset_dict = {}
    for assay_filters in assay_filters_list:
        # assign category and assay_type
        category = assay_filters[0]
        assay_type = assay_filters[1]
        # create key for dictionary
        subset_key = f"{category}_{assay_type}"
        # filter dataframe based on filter conditions to find subset of dataframe and add to dictionary with subset_key as dictionary key
        subset_dict[subset_key] = assay_data_subset[(assay_data_subset[subset_col]==category) & (assay_data_subset["Assay Type"]==assay_type)]
        
    return subset_dict


def calculate_embeddings_distance(assay_data):
    
    # store IDs for matrix column and index
    similarity_cols = assay_data['ChEMBL ID'].to_list()
    similarity_index = assay_data['ChEMBL ID'].to_list()
    # extract embeddings column
    embeddings_list = assay_data.embeddings
    
    # set number of IDs to calculate cosine similarity for
    n = len(embeddings_list)
    # create list to store all lists of embedding similarities
    similarity_frame = []

    # iterate over list of embeddings, assign embedding as embedding_a
    # NOTE!!!: This takes some time, have to calculate consine similarities for n_embeddings^2 
    for count, embedding_a in enumerate(embeddings_list[:n],1):
        # create list to store all embedding cosine similarities for embedding_a
        similarity_list = []
        # iterate over list of embeddings, assign embedding as embedding_b, for compariosn
        for embedding_b in embeddings_list[:n]:
            # Reshape the arrays to match the expected input shape of cosine_similarity
            embedding_a = embedding_a.reshape(1, -1)
            embedding_b = embedding_b.reshape(1, -1)
            # Calculate cosine similarity
            similarity = np.mean(np.absolute(cosine_similarity(embedding_a.reshape(-1, 1),embedding_b.reshape(-1, 1))))
            # append value to list
            similarity_list.append(similarity)
        # append similarity list for embedding_a to list of lists
        similarity_frame.append(similarity_list)
        # print count if multiple of 100
        if count % 100 == 0:
            print(f"Iteration {count}")
            
    # create cosine similarity matrix
    cosine_similarity_matrix = pd.DataFrame(similarity_frame,columns=similarity_cols[:n],index=similarity_index[:n])
    
    return cosine_similarity_matrix


def calculate_descriptions_distance(assay_data):
    
    # store IDs for matrix column and index
    similarity_cols = assay_data['ChEMBL ID'].to_list()
    similarity_index = assay_data['ChEMBL ID'].to_list()
    # extract embeddings column
    embeddings_list = assay_data.Description
    
    # set number of IDs to calculate cosine similarity for
    n = len(embeddings_list)
    # create list to store all lists of embedding similarities
    similarity_frame = []

    # iterate over list of embeddings, assign embedding as embedding_a
    # NOTE!!!: This takes some time, have to calculate consine similarities for n_embeddings^2 
    for count, embedding_a in enumerate(embeddings_list[:n],1):
        # create list to store all embedding cosine similarities for embedding_a
        similarity_list = []
        # iterate over list of embeddings, assign embedding as embedding_b, for compariosn
        for embedding_b in embeddings_list[:n]:
            # Calculate cosine similarity
            similarity = levenshtein_distance(embedding_a, embedding_b)
            # append value to list
            similarity_list.append(similarity)
        # append similarity list for embedding_a to list of lists
        similarity_frame.append(similarity_list)
        # print count if multiple of 100
        if count % 100 == 0:
            print(f"Iteration {count}")
            
    # create cosine similarity matrix
    cosine_similarity_matrix = pd.DataFrame(similarity_frame,columns=similarity_cols[:n],index=similarity_index[:n])
    
    return cosine_similarity_matrix


def assign_clusters(subset_dict, threshold_exponent = 0.75):
    
    assay_data_with_clusters = []
    category_list = list(subset_dict.keys())
    max_cluster = 0

    for category in category_list:
        # print name of subset category
        print(f"\n{category}")
        # assign subset from dictionary
        assay_data_subset = subset_dict[category]
        # check if matrix has a length less than 2, if not, move to next loop
        if len(assay_data_subset) < 2:
            # assign single cluster value to clusters array
            clusters = np.array([1])
            # shift cluster number based on higher cluster number from last subset
            clusters = clusters + max_cluster
            # add cluster labels as a column
            assay_data_subset['embedding_cluster'] = clusters
            # add dataframes to list storing all assay information with assigned clusters
            assay_data_with_clusters.append(assay_data_subset)
            # find highest cluster number to shift first position of next set of clusters
            max_cluster = np.max(clusters)
            # move to next loop
            continue
        # create similarity matrix from assay description embeddings
        cosine_similarity_matrix = calculate_embeddings_distance(assay_data_subset)
        print("Calculating pairwise cosine similarities")
        # find clusters using heirachical clustering
        clusters = find_clusters(cosine_similarity_matrix, threshold_exponent) # float can be changed to retrieve more stringent (lower value) or relaxed clusters (higher value)
        # shift cluster number based on higher cluster number from last subset
        clusters = clusters + max_cluster
        # add cluster labels as a column # 
        assay_data_subset['embedding_cluster'] = clusters
        # add dataframes to list storing all assay information with assigned clusters
        assay_data_with_clusters.append(assay_data_subset)
        # find highest cluster number to shift first position of next set of clusters
        max_cluster = np.max(clusters)

    return assay_data_with_clusters


def find_clusters(similarity_matrix,threshold_exponent):
    # Hierarchical clustering
    d = sch.distance.pdist(similarity_matrix)
    L = sch.linkage(d, method='complete')
    t = len(similarity_matrix) ** threshold_exponent
    print(f"n = {len(similarity_matrix)}")
    print(f"t = {t}")

    clusters = sch.fcluster(L, t, 'maxclust')
    
    return clusters


def assign_clusters_2(subset_dict, threshold_multiplier = 0.15):
    """For groups of clusters with are harder to separate"""
    assay_data_with_clusters = []
    category_list = list(subset_dict.keys())
    max_cluster = 0

    for category in category_list:
        # print name of subset category
        print(f"\n{category}")
        # assign subset from dictionary
        assay_data_subset = subset_dict[category]
        # check if matrix has a length less than 2, if not, move to next loop
        if len(assay_data_subset) < 2:
            # assign single cluster value to clusters array
            clusters = np.array([1])
            # shift cluster number based on higher cluster number from last subset
            clusters = clusters + max_cluster
            # add cluster labels as a column
            assay_data_subset['embedding_cluster'] = clusters
            # add dataframes to list storing all assay information with assigned clusters
            assay_data_with_clusters.append(assay_data_subset)
            # find highest cluster number to shift first position of next set of clusters
            max_cluster = np.max(clusters)
            # move to next loop
            continue
        # create similarity matrix from assay description embeddings
        cosine_similarity_matrix = calculate_descriptions_distance(assay_data_subset)
        print("Calculating pairwise Levenshtein distances")
        # find clusters using heirachical clustering
        clusters = find_clusters_2(cosine_similarity_matrix, threshold_multiplier) # float can be changed to retrieve more stringent (lower value) or relaxed clusters (higher value)
        # shift cluster number based on higher cluster number from last subset
        clusters = clusters + max_cluster
        # add cluster labels as a column # 
        assay_data_subset['embedding_cluster'] = clusters
        # add dataframes to list storing all assay information with assigned clusters
        assay_data_with_clusters.append(assay_data_subset)
        # find highest cluster number to shift first position of next set of clusters
        max_cluster = np.max(clusters)

    return assay_data_with_clusters


def find_clusters_2(similarity_matrix, threshold_multiplier):
    """For groups of clusters with are harders to separate"""
    # Hierarchical clustering
    d = sch.distance.pdist(similarity_matrix)
    L = sch.linkage(d, method='complete')
    t = threshold_multiplier*d.max()

    print(f"dmax = {d.max()}")
    print(f"dmin = {d.min()}")
    print(f"threshold multiplier = {threshold_multiplier}")
    print(f"t = {t}")

    # 0.15 can be modified to retrieve more stringent (lower value) or relaxed clusters (higher value)
    clusters = sch.fcluster(L, t, 'distance')
    
    return clusters


def add_drugs_and_targets(assay_data_clustered):

    # import file with assay to drug and target relationships
    AML_relationships = pd.read_csv("acute_myeloid_leukemia_approved_drugs_assay_target_chembl_id_relationship.csv")
    # only keep rows with assays in clustered data
    AML_relationships_ = AML_relationships[AML_relationships['assay_chembl_id'].isin(assay_data_clustered["ChEMBL ID"])]
    # remove rows from duplicate assay IDs
    assay_data_clustered = assay_data_clustered.drop_duplicates(subset="ChEMBL ID")
    # loop using assay IDs from relationships csv, pick up rows for each id in
    assay_data_list = []
    for assay_id in AML_relationships_.assay_chembl_id:
        assay_data = assay_data_clustered[assay_data_clustered["ChEMBL ID"]==assay_id]
        assay_data_list.append(assay_data)
    # create dataframe from list of dataframe rows
    assay_data_clustered_ = pd.concat(assay_data_list)
    # reset index for both dataframes
    assay_data_clustered_ = assay_data_clustered_.reset_index(drop=True)
    AML_relationships_ = AML_relationships_.reset_index(drop=True)
    # add columns from relationships dataframe to clustered assay dataframe
    assay_data_clustered_["parent_compound_chembl_id"] = AML_relationships_["parent_compound_chembl_id"]
    assay_data_clustered_["target_chembl_id"] = AML_relationships_["target_chembl_id"]
    assay_data_clustered_["check_assay_chembl_id"] = AML_relationships_["assay_chembl_id"]
    # check if IDs have mapped correctly
    assert len(assay_data_clustered_) == sum(assay_data_clustered_["check_assay_chembl_id"] == assay_data_clustered_["ChEMBL ID"])
    
    return assay_data_clustered_


