# # WG Rough Sleeper Count 

# +
import pandas as pd
import numpy as np
import json 

from gssutils import * 
# -

infoFileName = 'info.json'
info    = json.load(open(infoFileName))
scraper = Scraper(seed=infoFileName)
cubes   = Cubes(infoFileName)
scraper.dataset.family = info['families']
distro = scraper.distribution(latest=True)
distro._mediaType = 'application/json'

df = distro.as_pandas()

df.head()

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
             'Measure_Code', # Note required
             'Measure_ItemNotes_ENG', # All blanks
             'Year_Code', # Not required
             'Year_SortOrder', # Not required
             'Year_ItemNotes_ENG', # All blanks
             'RowKey', # Not required
             'PartitionKey'] # Not required
df.drop(drop_list, inplace=True, axis=1)

df.head()

# For everything which isn't the Data column, it's categorical so...
for col in df.columns:
    if col != 'Data':
        df[col] = df[col].astype('category')

# Data is the value, and is a count of people so...
df['Value'] = df['Data'].astype(int)
df.drop('Data', inplace=True, axis=1)

# +
# Geographies!
df['Geography'] = df['Area_AltCode1'].apply(lambda x: f"http://statistics.data.gov.uk/id/statistical-geography/{x}")

df.drop('Area_AltCode1', inplace=True, axis=1)
# -

# Marker (For the geography though it applies to values as well)
# Stored as a path now but there are some whitespace issues, which are fixed by splitting on spaces, and then rejoining
df['Marker'] = df['Area_ItemNotes_ENG'].apply(lambda x: pathify(" ".join(x.split())))
df.drop('Area_ItemNotes_ENG', inplace=True, axis=1)

# Measure
df.rename({'Measure_ItemName_ENG': 'Measure', 'Year_ItemName_ENG': 'Period'}, inplace=True, axis=1)
df.head()

# From the metadata, which is incomplete so therefor not implemented
exact_count = {
    '2015-16': '/id/georgean-interval/2015-11-25T23:00:00/P4H',
    '2016-17': '/id/georgean-interval/2016-11-03T22:00:00/P7H',
    '2017-18': '/id/georgean-interval/2017-11-09T22:00:00/P7H',
    '2018-19': '/id/georgean-interval/2018-11-08T22:00:00/P7H'
}
estimates = {
    '2015-16': '/id/georgean-interval/2015-11-02/P2W',
    '2016-17': '/id/georgean-interval/2016-11-10/P2W',
    '2017-18': '/id/georgean-interval/2017-11-15/P2W',
    '2018-19': '/id/georgean-interval/2018-11-16/P2W'  
}

# For the periods
df['Period'] = df['Period'].apply(lambda x: '/id/government-year/{}-{}'.format(x[:4], '20'+x[-2:]))


# Measures
df['Measure'] = df['Measure'].apply(lambda x: pathify(x))

# Add dataframe is in the cube
cubes.add_cube(scraper, df, scraper.title)


# Write cube
cubes.output_all()


