#!/usr/bin/env python
# coding: utf-8

# In[29]:


# # WG Homelessness statistics

from gssutils import *
import pandas as pd
import numpy as np
import json
import glob

infoFileName = 'info.json'
info    = json.load(open(infoFileName))
scraper = Scraper(seed=infoFileName)
cubes   = Cubes(infoFileName)
scraper


# In[30]:


distro = scraper.distribution(title=lambda x: "Dataset" in x)
distro


# In[31]:


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
        raise Exception(f"New Datamakers found in {col} but not transformed in pipeline")

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

df.rename({'Measure_ItemName_ENG': 'Measure', 'Area_AltCode1' : 'Geography'}, inplace=True, axis=1)

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

df['Period_Code'].cat.rename_categories(lambda x: {True: f"government-quarter/{x[:4]}-20{x[4:-2]}/Q{x[-1:]}", False: f"government-year/{x[:4]}-20{x[-3:-1]}"}.get("Q" in x), inplace=True)
df.rename({'Period_Code': 'Period'}, inplace=True)

# # Outcomes
# This field contains up to three bits of information
# * The outcome of the intervention (client behaviour)
# * Whether the household was eligible or ineligible (duty)
# * The specific duty under which the household is eligible for intervention (grounds for duty)
#
# This codelist is manually created. The dictionary has the following format:
# ```
# Outcomes_ItemName_ENG (value): (client-behaviour, duty, grounds-for-duty)
# ```

outcome = {
'Unsuccessfully relieved - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Unsuccessfully relieved','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Number of outcomes - Eligible, homeless, subject to duty to help to secure (Section 73)': ('DROP','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Assistance Refused - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Assistance Refused','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Assistance Refused - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Assistance Refused','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Assistance Refused - Eligible, unintentionally homeless and in priority need (Section 75)': ('Assistance Refused','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Eligible, but not homeless or threatened with homelessness': (np.nan,'Eligible','not homeless or threatened with homelessness'),
'Ineligible households': (np.nan,'Ineligible',np.nan),
'Non co-operation - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Non co-operation','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Non co-operation - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Non co-operation','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Non co-operation - Eligible, unintentionally homeless and in priority need (Section 75)': ('Non co-operation','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Unsuccessful prevention - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Unsuccessful prevention','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Number of outcomes - Eligible, homeless but not in priority need': (np.nan,'Eligible','homeless but not in priority need'),
'Number of outcomes - Eligible, homeless and in a priority need but intentionally so': (np.nan,'Eligible','homeless and in a priority need but intentionally so'),
'Number of outcomes - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('DROP','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Number of outcomes - Eligible, unintentionally homeless and in priority need (Section 75)': ('DROP','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Other Reasons - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Other Reasons','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Other Reasons - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Other Reasons','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Other Reasons - Eligible, unintentionally homeless and in priority need (Section 75)': ('Other Reasons','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Positively discharged - Eligible, unintentionally homeless and in priority need (Section 75)': ('Positively discharged','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Successful prevention - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Successful prevention','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Successfully relieved - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Successfully relieved','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Total Outcomes': ('DROP',np.nan,np.nan),
'Total prevention / Relief': ('DROP',np.nan,np.nan),
'Application withdrawn due to loss of contact  - Eligible, unintentionally homeless and in priority need (Section 75)': ('Application withdrawn due to loss of contact ','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Application withdrawn due to loss of contact  - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Application withdrawn due to loss of contact ','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Application withdrawn due to loss of contact  - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Application withdrawn due to loss of contact ','Eligible','homeless, subject to duty to help to secure (Section 73)'),
'Application Withdrawn  - Eligible, unintentionally homeless and in priority need (Section 75)': ('Application Withdrawn','Eligible','unintentionally homeless and in priority need (Section 75)'),
'Application Withdrawn  - Eligible, threatened with homelessness, prevention assistance provided (Section 66)': ('Application Withdrawn','Eligible','threatened with homelessness, prevention assistance provided (Section 66)'),
'Application Withdrawn  - Eligible, homeless, subject to duty to help to secure (Section 73)': ('Application Withdrawn','Eligible','homeless, subject to duty to help to secure (Section 73)')
}
outcome_df = pd.DataFrame(outcome).T.reset_index()
outcome_df.columns = (['outcome','client-behaviour', 'duty', 'grounds-for-duty'])
for col in outcome_df.columns:
    outcome_df[col] = outcome_df[col].astype('category')
df = df.merge(outcome_df, left_on='Outcomes_ItemName_ENG', right_on='outcome')
df.drop(['Outcomes_ItemName_ENG', 'outcome'], inplace=True, axis=1)
del outcome, outcome_df

# drop the summary values from the dataset, end users can summarise themselves
df = df.drop(df[df['client-behaviour'] == 'DROP'].index)

# Clean up the Value column
df['Value'] = df['Value'].astype(int)
df.loc[df['Value'] == -999999999, 'Marker'] = 'suppressed'
df.loc[df['Value'] == -999999999, 'Value'] = ''


# In[32]:


for col in df.columns:
    if col not in ['Value', 'Geography', 'Period_Code']:
        df[col] = df[col].astype('category')
        df[col].cat.rename_categories(lambda x: pathify(x), inplace=True)


# In[33]:


# Fix the Household column
df.rename({'Household_ItemName_ENG': 'household-type'}, axis=1, inplace=True)
df['household-type'].cat.rename_categories({'total': 'all-household'}, inplace=True)

df = df.rename(columns = {'household-type' : 'Household Type',
                          'Period_Code' : 'Period',
                          'client-behaviour' : 'Client Behaviour',
                          'duty' : 'Duty',
                          'grounds-for-duty' : 'Grounds for Duty'})

df['Value'] = df.apply(lambda x: int(x['Value']) if x['Marker'] == '' else x['Value'], axis = 1)

df['Grounds for Duty'] = df['Grounds for Duty'].cat.add_categories('not-applicable').fillna('not-applicable')
df['Client Behaviour'] = df['Client Behaviour'].cat.add_categories('all').fillna('all')

df = df[['Period', 'Geography', 'Household Type', 'Client Behaviour', 'Duty', 'Grounds for Duty', 'Value', 'Marker']]
df


# In[34]:


cubes.add_cube(scraper, df, scraper.title)


# In[35]:


cubes.output_all()


# In[35]:




