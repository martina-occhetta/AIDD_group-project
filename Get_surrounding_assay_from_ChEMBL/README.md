Important files:
* `acute_myeloid_leukemia_approved_drugs_with_chembl_id.csv`: compound-based csv with `drug name`, `resource url`, `parent compound chembl id`, `compound synonyms chembl id`, `assay chembl id`, `target chembl id`.   
* `acute_myeloid_leukemia_approved_drugs_assay_target_chembl_id_relationship.csv`: this csv show all the compounds-assays-targets relationship in `acute_myeloid_leukemia_approved_drugs_with_chembl_id.csv`. 

More assays' information:    
* The zip files in `assay_infos_zip_backup` were downloaded manually from chembl website. Each chembl id represents an approved drug's parent compound. For each compound, all surronding assays (including compound synonyms' assays) are stored in a file with its `parent compound chembl id` as the filename.   
* `assay_infos_filed_by_compound` is a folder with assays' informations, decompressed from `assay_infos_zip_backup`.   
* The files in `assay_infos_filed_by_compound_using_api` has similar information like those in `assay_infos_filed_by_compound` but directly access the data using chembl api. The column name is different from the files in `assay_infos_filed_by_compound`.