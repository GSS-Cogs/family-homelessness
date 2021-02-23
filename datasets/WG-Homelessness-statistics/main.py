# # WG Homelessness statistics 

from gssutils import * 
import pandas as pd
import numpy as np
import json 

infoFileName = 'info.json'
info    = json.load(open(infoFileName))
scraper = Scraper(seed=infoFileName)
cubes   = Cubes(infoFileName)
scraper.dataset.family = info['families']
distro = scraper.distribution(latest=True)
distro._mediaType = 'application/json'

df = distro.as_pandas()

df.head()

# Clearing all blank strings
df = df.replace(r'^\s*$', np.nan, regex=True)

# For everything which isn't the Data column, it's categorical so...
for col in df.columns:
    if col != 'Data':
        df[col] = df[col].astype('category')

# Quick check on what columns we need to keep
for c in df.columns:
    print(df[c].value_counts())

df.columns

# Throw an error if item notes which we don't expect have any values
# df['Household_ItemNotes_ENG'].count()
for col in ['Household_ItemNotes_ENG', 'Period_ItemNotes_ENG']:
    if df[col].count() != 0:
        print(col, df[col].count())
        raise Exception('New Datamakers not transformed')

# Likely not required or dupliate
drop_list = [
    'Area_Code', # Not required
    'Area_ItemName_ENG', # All blank
    'Area_SortOrder', # Not required
    'Area_Hierarchy', # Not required
    'Area_ItemNotes_ENG', # Emergency bed availability in Swansea not applicable for this dataset
    'Outcomes_Code', # Not required
    'Outcomes_SortOrder', # Not required
    'Outcomes_Hierarchy', # Not required
    'Outcomes_ItemNotes_ENG', # Only one value which isn't necessary as it is evident from data availability
    'Household_ItemNotes_ENG', 
    'Household_Code', # Not required
    'Household_SortOrder', # Not required
    'Household_ItemNotes_ENG', # All blank (checked in cell above - must be included otherwise)
    'Period_ItemName_ENG', # Not required
    'Period_SortOrder', # Not required
    'Period_ItemNotes_ENG', # All blank (checked in cell above - must be included otherwise)
    'RowKey', # Not required
    'PartitionKey' # Not required
]


df.drop(drop_list, inplace=True, axis=1)

# Data is the value, and is a count of people so...
df['Value'] = df['Data'].astype(int)
df.drop('Data', inplace=True, axis=1)

# Geographies!
df['Geography'] = df['Area_AltCode1'].apply(lambda x: "{}{}".format('http://statistics.data.gov.uk/id/statistical-geography/', x))
df.drop('Area_AltCode1', inplace=True, axis=1)

# Measure
df.rename({'Measure_ItemName_ENG': 'Measure'}, inplace=True, axis=1)
df.head()

# For periods
df['Period_Code'].cat.categories

# ### The periods require a bit more work. From the odata...
# ```
# {
#       "Data":-999999999.0,"Area_Code":"546","Area_ItemName_ENG":"Torfaen",
#       "Area_SortOrder":"24","Area_Hierarchy":"803","Area_ItemNotes_ENG":"",
#       "Area_AltCode1":"W06000020","Outcomes_Code":101.0,
#       "Outcomes_ItemName_ENG":"Ineligible households","Outcomes_SortOrder":"29",
#       "Outcomes_Hierarchy":160.0,"Outcomes_ItemNotes_ENG":"","Household_Code":"8",
#       "Household_ItemName_ENG":"Single person household","Household_SortOrder":"7",
#       "Household_ItemNotes_ENG":"","Period_Code":"201516Q3",
#       "Period_ItemName_ENG":"2015-16 October-December","Period_SortOrder":"7704",
#       "Period_ItemNotes_ENG":"","RowKey":"0000000000000172","PartitionKey":""
# }
# ```
#
# October-December is assigned a value of 201516Q3, which means these are government year and quarters not calendar years and quarters. If the value has a q in it it is a government quarter, otherwise a government year. Enter lambda functions with an anonymous dictionary

df['Period_Code'].cat.rename_categories(lambda x: {True: f"/id/government-quarter/{x[:4]}-Q{x[-1:]}", False: f"/id/government-year/{x[:4]}-{x[-3:-1]}"}.get("Q" in x), inplace=True)
df.rename({'Period_Code': 'Period'}, inplace=True)

df.head()

df['Outcomes_ItemName_ENG'].cat.rename_categories(lambda x: utils.pathify(x), inplace=True)

df.head()

# Add dataframe is in the cube
cubes.add_cube(scraper, df, scraper.title)


# Write cube
cubes.output_all()


