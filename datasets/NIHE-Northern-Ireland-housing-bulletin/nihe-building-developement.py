#!/usr/bin/env python
# coding: utf-8

# In[33]:


from gssutils import *
import json
import datetime
from pandas import ExcelWriter
import pandas as pd
from pathlib import Path

def right(s, amount):
    return s[-amount:]

def left(s, amount):
    return s[:amount]

year = int(right(str(datetime.datetime.now().year),4)) - 1
print(year)


info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[34]:


scraper = Scraper('https://www.communities-ni.gov.uk/publications/topic/8182?search=%22Northern+Ireland+Housing+Bulletin%22&Search-exposed-form=Go&sort_by=field_published_date')
scraper

# The URL was changed from the landing page taken from the info.json since the scraper is not made to use it.
# Could go back and edit the scraper but kinda seems like a pain in the ass considering the landing page is non-specific to the dataset.


# In[35]:


dist = scraper.distributions[0]
dist


# In[36]:


xls = pd.ExcelFile(dist.downloadURL, engine="odf")

with ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet)
    writer.save()

tabs = loadxlstabs("data.xls")


# In[37]:


tidied_sheets = []

for tab in tabs:

    if 'T1_1' in tab.name or 'T1_2' in tab.name:

        cell = tab.filter(contains_string('Quarter / Year'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        devType = cell.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        if tab.name == 'T1_1':
            buildingStage = 'Starts'
        else:
            buildingStage = 'Completions'

        observations = period.fill(RIGHT).is_not_blank() - tab.filter('`')

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(devType, 'Development Type', DIRECTLY, ABOVE),
                HDimConst('Building Stage', buildingStage),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Housing Type', 'All'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    elif 'T1_3' in tab.name or 'T1_4' in tab.name:

        cell = tab.filter(contains_string('Type of Housing'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = cell.fill(RIGHT).is_not_blank() | cell.shift(1,1).expand(RIGHT).is_not_blank() - remove

        housingType = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        housingType2 = cell.shift(DOWN).shift(RIGHT).expand(DOWN).is_not_blank() - remove

        if tab.name == 'T1_3':
            buildingStage = 'Starts'
        else:
            buildingStage = 'Completions'

        observations = housingType2.fill(RIGHT).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, ABOVE),
                HDim(housingType, 'Housing Type', CLOSEST, ABOVE),
                HDim(housingType2, 'Housing Type 2', DIRECTLY, LEFT),
                HDimConst('Building Stage', buildingStage),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Development Type', 'Social Housing Development'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    else:

        continue


# In[38]:


df = pd.concat(tidied_sheets, ignore_index = True, sort = False).fillna('')

df['Period'] = df['Period'].map(lambda x: 'government-year/' + left(x, 4) if left(x, 2) == '20' else x)
df['Period'] = df['Period'].map(lambda x: x + '-' + str(int(right(x, 4)) +  1) if 'government-year' in x else x)

df['Period'] = df['Period'].map(lambda x: 'government-quarter/' + right(x, 4) + '-' + str(int(right(x, 4)) + 1) + '/Q' + left(x, 3) + '' if 'government-year/' not in x and left(right(x, 4),2) == '20' else x)

df['Period'] = df.apply(lambda x: str(x['Period']).replace('Apr', '1') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Jul', '2') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Oct', '3') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Jan', '4') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)

df['Housing Type'] = df['Housing Type'] + ' ' + df['Housing Type 2']

df = df.drop(['Housing Type 2'], axis=1)

df = df.replace({'Development Type' : {
    'TotalNew DwellingStarts' : 'Total',
    'TotalNew DwellingCompletions' : 'Total'},
                'Housing Type' : {
    'Shared Sub-total' : 'Shared Total',
    'Self-Contained Sub-total' : 'Self-Contained Total',
    'Self-Contained Totals' : 'Totals'},
                'Period' : {
    'Apr-Jun' : 'government-quarter/2019-2020/Q1',
    'Jul-Sep' : 'government-quarter/2019-2020/Q2',
    'Oct-Dec' : 'government-quarter/2019-2020/Q3'}})

df.rename(columns={'OBS' : 'Value'}, inplace=True)

df.head()


# In[39]:



from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[40]:



tidy = df[['Period','Development Type', 'Building Stage','Housing Type','Value','Measure Type','Unit']]

for column in tidy:
    if column in ('Marker', 'Development Type', 'Building Stage', 'Housing Type'):
        tidy[column] = tidy[column].map(lambda x: pathify(x))

tidy.head(25)


# In[41]:


scraper.dataset.title = 'NIHE - Building Development'
scraper.dataset.comment = """
The date of a new dwelling start is the date on which the first building control inspection takes place.
The figures only include applications for new dwellings received by Building Control in NI.
The figures include domestic apartments and dwellings as defined by Building Control purpose group.
Figures will be revised on an annual basis to capture Building Control applications received outside of the quarter.
The date of a new dwelling completion is the date on which the building control completion inspection takes place.
The Housing Executive no longer builds new dwellings. This has been the case since 2001-02. Occasionally it may still replace on Housing Executive new builds will no longer be available.
Housing Association new social housing dwelling starts are recorded when housing associations confirm the start on-site of new build/rehabilitation/re-improvement units, or the purchase of Off-the-Shelf units, for social housing.
The formal definitions of all scheme types can be found in the Housing Association Guide at: https://www.communities-ni.gov.uk/scheme-types
Housing Association new social housing dwelling completions are recorded when housing associations confirm the completion of new build/rehabilitation/re-improvement units, or the purchase of Off-the-Shelf units, for social housing.
"""


# In[41]:





# In[42]:


out = Path('out')
out.mkdir(exist_ok=True)

title = pathify('NIHE - Building Development')

tidy.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

scraper.dataset.family = 'homelessness'
scraper.dataset.theme = THEME['housing-planning-local-services']
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-homelessness/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

