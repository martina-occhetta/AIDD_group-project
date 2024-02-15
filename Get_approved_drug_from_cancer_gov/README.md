# Get the approved drugs directly from the website using Beautifulsoup4
`Get_approved_drug_using_beautisoap.ipynb` is the file to get the data from the website [Cancer.gov](https://www.cancer.gov). The main processing code is now moved to `get_approved_drug.py` file.  
* input: correct `url`, correct key word `query`
* output: a `*.csv` file about a list of approved drug.
## Read-to-use data

## Quick start

For example, let investigate the target disease `Acute Myeloid Leukemia (AML)`. The infomation can be accessed using a browser to this [website](https://www.cancer.gov/about-cancer/treatment/drugs/leukemia#4). Please indicate the correct url source to your [Get_approved_drug_using_beautisoap.ipynb](./Get_approved_drug_using_beautisoap.ipynb).


However, there are several subtypes of the `Leukemia` and our target disease (`AML`) is just one subtype of the `Leukemia`. Thus, please type key word about the specific subtype at `query` in your [Get_approved_drug_using_beautisoap.ipynb](./Get_approved_drug_using_beautisoap.ipynb).


```python
...
## 
url = "https://www.cancer.gov/about-cancer/treatment/drugs/leukemia#4"
## 
# for leukemia
query = "acute myeloid leukemia"; name = "acute myeloid leukemia"
url = "https://www.cancer.gov/about-cancer/treatment/drugs/leukemia#4"
...
##
approved_drugs_df = get_approved_drug(url, query)
```
To show the first few lines of the results:  
```python
approved_drugs_df.head()
```

Hopefully, you will get the `.csv` file in the folder `approved_drug_by_disease` by following codes.
```python
# Save the dataframe
approved_drugs_df.to_csv(f'./approved_drug_by_disease/{name.replace(" ", "_")}_approved_drugs.csv', index=False)
```


## Environment
If you using conda, use the following to install your environment.
```bash
conda install --yes --file requirements.txt
```