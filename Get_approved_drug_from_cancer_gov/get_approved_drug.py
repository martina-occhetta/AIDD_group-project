import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_approved_drug(source_url, query):
    page = requests.get(source_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # 1. Find all the subtypes based on the query
    found_info = {}
    for each_subtype in soup.find_all(name="h2"):
        each_subtype_string = each_subtype.get_text().lower()
        if query in each_subtype_string:
            found_info[each_subtype_string] = each_subtype.find_next_sibling()
        else:
            pass

    # 2. Look at the matched subtypes
    # found_info.keys()

    # 3. Extract the information and the drug list
    key_name = [each for each in found_info.keys() if 'drugs approved' in each]
    # print(key_name[0])
    approved_drugs = found_info[key_name[0]].get_text()
    approved_drugs_list = approved_drugs.split('\n')[:-1]
    # print(approved_drugs_list[0:5])

    # 4. Extract the URL for the drug information
    a_tags = found_info[key_name[0]].find_all(name="a")
    root_url = "https://www.cancer.gov"
    approved_drugs_info_url = []
    for tag in a_tags:
        if not tag.get('href').startswith(root_url):
            approved_drugs_info_url.append(root_url + tag.get('href'))
        else:
            approved_drugs_info_url.append(tag.get('href'))

    # 5. Create a dataframe
    approved_drugs_df = pd.DataFrame([approved_drugs_list, approved_drugs_info_url]).T
    approved_drugs_df.columns = ['drug_name', 'resource_url']
    approved_drugs_df.drop_duplicates(subset="resource_url", inplace=True)
    
    return approved_drugs_df