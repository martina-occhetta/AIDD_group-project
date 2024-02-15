# 2024 AIDD project - assay cascade
For a drug to reach the market it must be proved to be safe, effective and be value for money. Safety and efficacy are assessed in clinical trials, which are both time consuming and costly. Hence, in order to reduce the risks associated with conducting clinical trials, potential drugs are evaluated in a range of pre-clinical models. These can be animal models, organoids, cells or cell-free assays. The assays used earlier in the drug discovery process tend to be those with higher throughput and lower associated costs. This allows higher numbers of molecules to be assessed but with these assays being further removed from human disease biology, this potential lack of translatability introduces uncertainty in the decision-making process. If an assay used early in the development pipeline is not predictive of clinical outcome, it risks allowing the progression of molecules with limited chance of success in trials or alternatively eliminating potentially good drugs from further investigation.

The aim of this group project is to investigate the power of preclinical assays to predict clinical success in a specific disease area (`cancer`). In this study, we focused on `acute myeloid leukemia (AML)`. It is a fast-growing cancer in which too many myeloblasts (a type of immature white blood cell) are found in the bone marrow and blood ([cancer.gov](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/acute-myeloid-leukemia)). We started with the `approved drugs` for `AML` and aimed to `filter out the must-do assays` for `AML`. This will make scientists easier to pinpoint which assays should be done first and compare the activities with the previous studies. Furthermore, the automated workflow can be scaled up to investigate several types of cancers in the future.


## Overall workflow
Link the relationship between disease, assays (assay clusters), targets, drugs using a graph.

Data source relationship.
1. disease -> approved drugs (in cancer.gov)   
    > [Get_approved_drug_from_cancer_gov](./Get_approved_drug_from_cancer_gov): this is an automated script to get the approved for a specific cancer with inputs `source_url` (website link) and `query` (text-based pattern) from [cancer.gov](https://www.cancer.gov/about-cancer/treatment).     
2. approved drugs -> surrounding assays -> targets (in ChEMBL)
    > [Get_surrounding_assay_from_ChEMBL](./Get_surrounding_assay_from_ChEMBL): using ChEMBL API to get the assay surrounding each approved drugs for a specific disease.  
    > For each assay, ChEMBL has annotated with `target ChEMBL ID`.
3. assays -> assays clustering (become assay clusters)
    > [assay_clustering](./assay_clustering): due to the diversity of assays, the similar assays should be grouped together. In this study, we adopted `BioSentVec` to transform the text description into vector-based embeddings for calculating the similarity of the assays.
4. disease -> targets
    > [OT_disease_to_target](./OT_disease_to_target): using the data from [opentarget](https://platform.opentargets.org/) to get the associations between disease and target.  
5. graph generation and visualisation: linking the data across the types (disease, drug, target, assay). 
    > [ChEMBL_graph_generation](./ChEMBL_graph_generation/): generate graph representation.  
    > [ChEMBL_visualisation](./ChEMBL_visualisation/): visualise some cancer-related data to have a brief understanding of compound-drug relationship.  
