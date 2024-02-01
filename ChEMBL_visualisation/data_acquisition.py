from chembl_webresource_client.new_client import new_client
import pandas as pd

# Define function to fetch assay data
def fetch_assay_data():
    # Initialize the ChEMBL client
    assays = new_client.assay

    # Fetch assays related to cancer
    #cancer_assays = assays.filter(description__iregex='cancer|tumor').only(['assay_id', 'description', 'assay_type'])
    cancer_assays = assays.filter(description__iregex='anticancer').only(['assay_chembl_id','assay_organism','description'])


    # Convert to a DataFrame and return
    return pd.DataFrame(cancer_assays)

def fetch_compound_data(assay_id):
    activities = new_client.activity
    compound_activities = activities.filter(assay_chembl_id=assay_id).only(['molecule_chembl_id'])
    return [activity['molecule_chembl_id'] for activity in compound_activities]

def fetch_clinical_trial_stage(compound_id):
    drug = new_client.drug
    compound_info = drug.filter(molecule_chembl_id=compound_id).only(['molecule_chembl_id', 'development_phase'])
    return compound_info[0]['development_phase'] if compound_info else None

def main():
    assay_data = fetch_assay_data()

    # Initialize new columns
    assay_data['compound_ids'] = None
    assay_data['clinical_trial_stages'] = None

    for index, row in assay_data.iloc[0:5567].iterrows():
        compound_ids = fetch_compound_data(row['assay_chembl_id'])
        #print(compound_ids)
        # Check if compound_ids is not empty
        if compound_ids:
            stages = [fetch_clinical_trial_stage(cid) for cid in compound_ids]
            assay_data.at[index, 'compound_ids'] = ', '.join(compound_ids)
            assay_data.at[index, 'clinical_trial_stages'] = ', '.join([str(stage) for stage in stages])
        else:
            assay_data.at[index, 'compound_ids'] = 'None'
            assay_data.at[index, 'clinical_trial_stages'] = 'None'

    print(assay_data.head())


if __name__ == "__main__":
    main()
