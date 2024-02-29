This is a folder to cross-link the dataset from different sources with various information.

Input data:
* [opentarget-disease2target](../OT_disease_to_target/target_associated_with_AML_grouped_clean.csv): Disease-target association based on Open Targets. Also, the target is transformed into UniProt ID.    
* [chembl-drug-assay-target-relationship](../Get_surrounding_assay_from_ChEMBL/acute_myeloid_leukemia_approved_drugs_assay_target_chembl_id_relationship.csv): The relationship between (1) AML approved drugs (2) drug-dependent surrounding assays (3) corresponding targets.   
* [chembl-assay-target2uniprot](../target2uni/AML_accep_specific_uni_id_df.csv): This csv contains the relationship between `target ChEMBL ID` and `UniProt ID`.   
* [clustering-assays](../assay_clustering/AML_assays_clustered.csv): The csv contains the clustering group for each assays.   


Main script:
* [main.ipynb](main.ipynb): main data-processing script.
    * If the disease's target matches with te assay's target, the score of the assay's importance will be `+1`.   
    * If the assay can be assigned to an assay cluster, the score of the assay's importance will be `+1` due to the assay cluster's list excluding non-AML cell lines.
    * The records in the final relationship csv file are ranked by `assay importance`, `assay cluster`, and `open target overall score`.  
* [pd_process.py](pd_process.py): requirement functions for `main.ipynb`.


Output data:
* [AML_drugs_assay_target_disease_mapped_relationship_raw.csv](AML_drugs_assay_target_disease_mapped_relationship_raw.csv): raw curated data for the relationship.   
* [AML_drugs_assay_target_disease_mapped_relationship_tidy.csv](AML_drugs_assay_target_disease_mapped_relationship_tidy.csv): tidy curated data for the relationship (only necessary data for graph plot).   
* [AML_drugs_assay_target_disease_mapped_relationship_tidy_non_wide_used.csv](AML_drugs_assay_target_disease_mapped_relationship_tidy_non_wide_used.csv): a subset of `tidy` data above, and only retain the relationship with `specific` and `acceptable` drugs for AML.   
* [AML_drugs_assay_target_disease_mapped_relationship_tidy_assay_importance_2.csv](AML_drugs_assay_target_disease_mapped_relationship_tidy_assay_importance_2.csv): a subset of `tidy` data above, and only retain the relationship with `assay important == 2` drugs for AML.   