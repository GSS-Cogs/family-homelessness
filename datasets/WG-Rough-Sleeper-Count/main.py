#!/usr/bin/env python
# coding: utf-8

# In[27]:


# # WG Rough Sleeper Count


# In[28]:


import pandas as pd
import numpy as np
import json

from gssutils import *


# In[29]:


infoFileName = 'info.json'
info    = json.load(open(infoFileName))
scraper = Scraper(seed=infoFileName)
cubes   = Cubes(infoFileName)
scraper.dataset.family = info['families']
distro = scraper.distribution(latest=True, title='Dataset')
distro._mediaType = 'application/json'


# In[30]:


df = distro.as_pandas()

df.head()


# In[31]:


# # Quick check on what columns we need to keep
# for c in df.columns:
#     print(df[c].value_counts())

# df.columns

# Clearing all blank strings
df = df.replace(r'^\s*$', np.nan, regex=True)

# Throw an error if item notes which we don't expect have any values
# df['Household_ItemNotes_ENG'].count()
for col in ['Year_ItemNotes_ENG', 'Measure_ItemNotes_ENG']:
    if df[col].count() != 0:
        print(col, df[col].count())
        raise Exception(f"New Datamakers found in {col} but not transformed in pipeline")

# Likely not required or dupliate
drop_list = ['Area_Code', # Not required
             'Area_ItemName_ENG', # Not required
             'Area_SortOrder', # Not required
             'Area_Hierarchy', # Not required
             'Measure_SortOrder', # Not required
             #'Measure_Code', # Note required
             'Measure_ItemNotes_ENG', # All blanks
             #'Year_Code', # Not required
             'Year_SortOrder', # Not required
             'Year_ItemNotes_ENG', # All blanks
             'RowKey', # Not required
             'PartitionKey'] # Not required
df.drop(drop_list, inplace=True, axis=1)

df.head()


# In[32]:


# For everything which isn't the Data column, it's categorical so...
for col in df.columns:
    if col != 'Data':
        df[col] = df[col].astype('category')

# Data is the value, and is a count of people so...
df['Value'] = df['Data'].astype(int)
df.drop('Data', inplace=True, axis=1)


# In[33]:


# Geographies!
#df['Geography'] = df['Area_AltCode1'].apply(lambda x: f"http://statistics.data.gov.uk/id/statistical-geography/{x}")


# In[34]:


# Marker (For the geography though it applies to values as well)
# Stored as a path now but there are some whitespace issues, which are fixed by splitting on spaces, and then rejoining
df['Marker'] = df['Area_ItemNotes_ENG'].apply(lambda x: pathify(" ".join(x.split())))
df.drop('Area_ItemNotes_ENG', inplace=True, axis=1)

# Measure
df.rename({'Measure_ItemName_ENG': 'Measure', 'Year_ItemName_ENG': 'Period', 'Area_AltCode1' : 'Area'}, inplace=True, axis=1)

df.head()


# In[35]:


df['Period'] = df.apply(lambda x: x['Period'] + str(x['Measure_Code']) if x['Measure_Code'] in [1, 4] else x['Period'], axis = 1)

periodMeasure = {'2015-161' : 'gregorian-interval/2015-11-25T23:00:00/P4H',
                 '2016-171' : 'gregorian-interval/2016-11-03T22:00:00/P7H',
                 '2017-181' : 'gregorian-interval/2017-11-09T22:00:00/P7H',
                 '2018-191' : 'gregorian-interval/2018-11-08T22:00:00/P7H',
                 '2019-201' : 'gregorian-interval/2019-11-08T22:00:00/P7H',
                 '2015-16' : 'gregorian-day/2015-11-25',
                 '2016-17' : 'gregorian-day/2016-11-03',
                 '2017-18' : 'gregorian-day/2017-11-09',
                 '2018-19' : 'gregorian-day/2018-11-08',
                 '2019-20' : 'gregorian-day/2019-11-08',
                 '2015-164' : 'gregorian-interval/2015-11-02/P2W',
                 '2016-174' : 'gregorian-interval/2016-11-10/P2W',
                 '2017-184' : 'gregorian-interval/2017-11-15/P2W',
                 '2018-194' : 'gregorian-interval/2018-11-16/P2W',
                 '2019-204' : 'gregorian-interval/2019-11-16/P2W'}

df = df.replace({'Period' : periodMeasure})

df


# In[36]:


#Below would turn the Total Available Beds, and Total Beds measures into Attributes of the Other 2 Measures.
#Rather than delete it, if we decide to go this way its still here

"""dfAttribute1 = df.loc[df['Measure_Code'].isin([2])]
dfAttribute2 = df.loc[df['Measure_Code'].isin([3])]

dfAttribute1 = dfAttribute1.rename(columns = {'Value' : 'Total Emergency Beds'})

dfAttribute1 = dfAttribute1[['Area', 'Year_Code', 'Total Emergency Beds']]

dfAttribute2 = dfAttribute2.rename(columns = {'Value' : 'Available Emergency Beds'})

dfAttribute2 = dfAttribute2[['Area', 'Year_Code', 'Available Emergency Beds']]

dfAttribute2

df = df.loc[df['Measure_Code'].isin([1, 4])]

dfJoin1 = pd.merge(df, dfAttribute1, how="left", on=['Year_Code', 'Area'])
dfJoin2 = pd.merge(dfJoin1, dfAttribute2, how="left", on=['Year_Code', 'Area'])

dfJoin2.drop_duplicates().to_csv('join.csv', index = False)

df = dfJoin2"""


# In[37]:


# For the periods
#df['Period'] = df['Period'].apply(lambda x: 'government-year/{}-{}'.format(x[:4], '20'+x[-2:]))

# Measures
df['Measure'] = df['Measure'].apply(lambda x: pathify(x))

df['Measure Type'] = df.apply(lambda x: 'estimated-count' if 'estimated' in x['Measure'] else 'count', axis = 1)
df['Measure Type'] = df.apply(lambda x: 'total' if 'emergency' in x['Measure'] else x['Measure Type'], axis = 1)
#This is not ideal as it is still technically a count, but as Unit is currently not included in validation (due to matching up during RDF phase) this will have to do instead
df['Unit'] = df['Measure']

df = df.replace({'Unit' : {'total-count-of-rough-sleepers' : 'rough-sleepers',
                              'total-number-of-emergency-bed-spaces' : 'emergency-bed-spaces',
                              'number-which-were-available-on-the-night-of-the-count' : 'available-bed-spaces',
                              'estimated-number-of-rough-sleepers' : 'rough-sleepers'}})

df = df.rename(columns={'Marker' : 'Notes'})
#the only markers in the dataset are more applicably assigned as an attribute to the observation

#df = df[['Period', 'Area', 'Total Emergency Beds', 'Available Emergency Beds', 'Value', 'Measure Type', 'Unit', 'Notes']]

df = df[['Period', 'Area', 'Value', 'Measure Type', 'Unit', 'Notes']]

df


# In[38]:


comments = """
This information shows the number of rough sleepers in local authority areas. The data is collected to gain a better understanding of the scale and trends in rough sleeping over time to inform local and national policy.The total counts of rough sleepers are single night snapshots. The estimated count is based on data collected over a two week period with assistance from the voluntary sector, faith groups, local businesses/residents, health and substance misuse agencies, and the police.In 2015-16, the count took place between the hours of 11pm on the 25th November and 3am on the 26th November 2015.In 2016-17, the count took place between the hours of 10pm on the 3rd November and 5am on the 4th November 2016.In 2017-18, the count took place between the hours of 10pm on the 9th of November and 5am on the 10th of November 2017.In 2018-19, the count took place between the hours of 10pm on the 8th of November and 5am on the 9th of November 2018.For the estimated number of people sleeping rough, data was collected over a two week period.In 2015-16, data was collected between the 2nd November and 15th November 2015.In 2016-17, data was collected between the 10th October and the 23rd October 2016.In 2017-18, data was collected between the 15th October and the 28th October 2017.In 2018-19, data was collected between the 16th October and the 29th October 2018.
Timing Methodology of for 2019-2020 has not been included as of most recent update, therefore Period measurements have been brought forward from the previous year.
2017-18 data is not directly comparable with 2016-17 data and similarly 2016-17 data is not directly comparable with 2015-16 data due to timing differences.
"""
scraper.dataset.comment = comments

# Add dataframe is in the cube
cubes.add_cube(scraper, df, scraper.title)


# In[39]:


# Write cube
cubes.output_all()


# In[39]:




