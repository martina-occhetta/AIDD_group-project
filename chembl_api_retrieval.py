from chembl_webresource_client.new_client import new_client


# random playaround codes
available_resources = [resource for resource in dir(new_client) if not resource.startswith('_')]
print(available_resources)

# Get a list of all activities filtered by IC50 for a given target
target = new_client.target
activity = new_client.activity
herg = target.filter(pref_name__iexact='hERG').only('target_chembl_id')[0]
herg_activities = activity.filter(target_chembl_id=herg['target_chembl_id']).filter(standard_type="IC50")

# Get a list of all assays 
assay = new_client.assay
res = assay.filter(description__icontains='inhibit', assay_type='A')



# research question and how to answer it
# 1. What are the compounds tested for this disease?
# unsure how to find directly what compounds are associated with what disease, 
# but you can look into an assay cascade and search for a assay for the disease, and the compounds tested for that assay

# 2. What are the bioactivity value for these compounds within the assay cascade?

# 3. When comparing the compounds that passed or failed the assay, what are the differences in their chemical properties?



