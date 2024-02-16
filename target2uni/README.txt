Hello everyone!!

So, this folder contains one notebook and one csv file. you do not need to run the notebook, but if you want to do this, get the csv file from Get_surrounding_assay_from_ChEMBL folder, and the file name is 'acute_myeloid_leukemia_acceptable_approved_drugs_with_chembl_id.csv'. (god this is so looooooong), all the target ids and drug names are extracted from this csv file.

About the csv file, it contains 14 columns, as 7 pairs, because we have 7 drugs, and each pair is named after DRUG's chembl id, not assay id! And we have XXX_target_id column, this is the ASSAY TARGET chembl ids of the drug, and XXX_target_uni_ids contains the UNIPROT ids of the assay targets.

when you see something like 'no_uni_id!' this means this assay target does NOT have any uniprot ids.