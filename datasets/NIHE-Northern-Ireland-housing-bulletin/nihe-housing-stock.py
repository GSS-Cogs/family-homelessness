#!/usr/bin/env python
# coding: utf-8

# In[10]:


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


# In[11]:


scraper = Scraper('https://www.communities-ni.gov.uk/publications/topic/8182?search=%22Northern+Ireland+Housing+Bulletin%22&Search-exposed-form=Go&sort_by=field_published_date')
scraper

# The URL was changed from the landing page taken from the info.json since the scraper is not made to use it.
# Could go back and edit the scraper but kinda seems like a pain in the ass considering the landing page is non-specific to the dataset.


# In[12]:



xls = pd.ExcelFile(scraper.distributions[0].downloadURL, engine="odf")

with ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet)
    writer.save()

tabs = loadxlstabs("data.xls")


# In[13]:


tidied_sheets = []

for tab in tabs:

    if 'T3_1' in tab.name:

        cell = tab.filter(contains_string('Year'))

        remove = tab.filter(contains_string('SOURCE:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        year = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        quarter = cell.shift(1,1).expand(DOWN).is_not_blank() - remove

        housePriceIndex = cell.shift(2,0).expand(RIGHT).is_not_blank()

        observations = quarter.fill(RIGHT).is_not_blank()

        dimensions = [
                HDimConst('ONS Geography Code', 'N07000001'),
                HDim(year, 'Year', CLOSEST, ABOVE),
                HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                HDim(housePriceIndex, 'House Price and Index Values', DIRECTLY, ABOVE),
                HDimConst('Housing Type', 'All'),
                HDimConst('Housing Sector', 'All'),
                HDimConst('Measure Type', 'TEMP'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    elif 'T3_2' in tab.name:

        cell = tab.filter(contains_string('Year'))

        remove = tab.filter(contains_string('SOURCE:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        year = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        quarter = cell.shift(1,1).expand(DOWN).is_not_blank() - remove

        housingType = cell.shift(2,0).expand(RIGHT).is_not_blank()

        observations = quarter.fill(RIGHT).is_not_blank()

        dimensions = [
                HDimConst('ONS Geography Code', 'N07000001'),
                HDim(year, 'Year', CLOSEST, ABOVE),
                HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                HDimConst('House Price and Index Values', 'N/A'),
                HDim(housingType, 'Housing Type', DIRECTLY, ABOVE),
                HDimConst('Housing Sector', 'All'),
                HDimConst('Measure Type', 'Sales'),
                HDimConst('Unit', 'Count')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    elif 'T3_3' in tab.name:

        cell = tab.filter(contains_string('Index')).shift(LEFT)

        remove = tab.filter(contains_string('SOURCE:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        housingType = cell.shift(0,2).expand(DOWN).is_not_blank() - remove

        housePriceIndex = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        observations = housingType.fill(RIGHT).is_not_blank()

        dimensions = [
                HDimConst('ONS Geography Code', 'N07000001'),
                HDimConst('Year', '2019'),
                HDimConst('Quarter', 'Q1'),
                HDim(housePriceIndex, 'House Price and Index Values', DIRECTLY, ABOVE),
                HDim(housingType, 'Housing Type', DIRECTLY, LEFT),
                HDimConst('Housing Sector', 'All'),
                HDimConst('Measure Type', 'TEMP'),
                HDimConst('Unit', 'TEMP')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    elif 'T3_4' in tab.name:

        cell = tab.filter(contains_string('Quarter / Year'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        housePriceIndex = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        year = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        quarter = cell.shift(DOWN).expand(DOWN).is_not_blank() - remove

        observations = year.fill(RIGHT).is_not_blank()

        dimensions = [
                HDimConst('ONS Geography Code', 'N07000001'),
                HDim(year, 'Year', DIRECTLY, LEFT),
                HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                HDim(housePriceIndex, 'House Price and Index Values', DIRECTLY, ABOVE),
                HDimConst('Housing Type', 'All'),
                HDimConst('Housing Sector', 'All'),
                HDimConst('Measure Type', 'TEMP'),
                HDimConst('Unit', 'TEMP')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    elif 'T3_5' in tab.name:

        cell = tab.filter(contains_string('Local Government District'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        housingSector = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        housingSector2 = cell.shift(1, 2).expand(RIGHT).is_not_blank()

        area = cell.shift(0,2).expand(DOWN).is_not_blank() - remove

        observations = area.fill(RIGHT)#.is_not_blank()

        dimensions = [
                HDim(area, 'ONS Geography Code', DIRECTLY, LEFT),
                HDimConst('Year', '2019'),
                HDimConst('Quarter', 'Q2'),
                HDimConst('House Price and Index Values', 'N/A'),
                HDimConst('Housing Type', 'All'),
                HDim(housingSector, 'Housing Sector A', CLOSEST, LEFT),
                HDim(housingSector2, 'Housing Sector B', CLOSEST, LEFT),
                HDimConst('Measure Type', 'TEMP'),
                HDimConst('Unit', 'TEMP')
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidy = tidy_sheet.topandas()

        tidy['Housing Sector'] = tidy['Housing Sector A'] + ' ' + tidy['Housing Sector B']
        tidy = tidy.drop(['Housing Sector A', 'Housing Sector B'], axis=1)

        tidied_sheets.append(tidy)

    else:

        continue


# In[14]:


df = pd.concat(tidied_sheets, ignore_index = True, sort = False).fillna('')

df['Measure Type'] = df.apply(lambda x: 'Count' if 'Sales' in x['Housing Sector'] else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'GBP' if 'Average' in x['Housing Sector'] else x['Measure Type'], axis = 1)

df['Unit'] = df.apply(lambda x: 'Sales' if 'Sales' in x['Housing Sector'] else x['Unit'], axis = 1)
df['Unit'] = df.apply(lambda x: 'Average Price' if 'Average' in x['Housing Sector'] else x['Unit'], axis = 1)

df = df.replace({'House Price and Index Values' : {
    'NI House Price Index' : 'House Price Index',
    'NI Standardised House Price' : 'Standardised House Price',
    'Index(Quarter 4 2019)' : 'House Price Index',
    'Percentage Change on Previous Quarter' : 'Quarterly Change',
    'Percentage Change over 12 Months' : 'Annual Change',
    'Standardised Price(Quarter 4 2019)' : 'Standardised Price',
    'Number Of' : 'New Dwelling Sales',
    'Average' : 'New Dwellings Average Price'},
                'Housing Sector' : {
    'All Sectors Average Price' : 'All Sectors',
    'All Sectors Sales' : 'All Sectors',
    'Private Sector Average Price' : 'Private Sector',
    'Private Sector Sales' : 'Private Sector',
    'Public Sector Sales' : 'Public Sector',
    'Public Sector Average Price' : 'Public Sector'},
                'ONS Geography Code' : {
    'Antrim and Newtownabbey' : 'N09000001',
	'Ards and North Down' : 'N09000011',
	'Armagh City Banbridge and Craigavon' : 'N09000002',
	'Belfast' : 'N09000003',
	'Causeway Coast and Glens' : 'N09000004',
	'Derry City and Strabane' : 'N09000005',
	'Fermanagh and Omagh' : 'N09000006',
	'Lisburn and Castlereagh' : 'N09000007',
	'Mid and East Antrim' : 'N09000008',
	'Mid Ulster' : 'N06000010',
	'Newry Mourne and Down' : 'N09000010',
	'Northern Ireland' : 'N07000001'}})

df['Measure Type'] = df.apply(lambda x: 'Index' if 'House Price Index' in x['House Price and Index Values'] else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'GBP' if 'Standardised House Price' in x['House Price and Index Values'] else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'GBP' if 'Standardised Price' in x['House Price and Index Values'] else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'Percentage' if 'Change' in x['House Price and Index Values'] else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'Sales' if 'Sales' in x['House Price and Index Values'] else x['Measure Type'], axis = 1)
df['Measure Type'] = df.apply(lambda x: 'GBP' if 'Average' in x['House Price and Index Values'] else x['Measure Type'], axis = 1)

df['Unit'] = df.apply(lambda x: 'Index' if 'House Price Index' in x['House Price and Index Values'] else x['Unit'], axis = 1)
df['Unit'] = df.apply(lambda x: 'GBP' if 'Standardised House Price' in x['House Price and Index Values'] else x['Unit'], axis = 1)
df['Unit'] = df.apply(lambda x: 'GBP' if 'Standardised Price' in x['House Price and Index Values'] else x['Unit'], axis = 1)
df['Unit'] = df.apply(lambda x: 'Percent' if 'Change' in x['House Price and Index Values'] else x['Unit'], axis = 1)
df['Unit'] = df.apply(lambda x: 'Count' if 'Sales' in x['House Price and Index Values'] else x['Unit'], axis = 1)
df['Unit'] = df.apply(lambda x: 'Price' if 'Average' in x['House Price and Index Values'] else x['Unit'], axis = 1)

df['Period'] = df['Year'] + ' ' + df['Quarter']
df['Period'] = df.apply(lambda x: 'government-quarter/' + str(int(left(x['Period'], 4))) + '-' + str(int(left(x['Period'], 4)) + 1 ) + '/Q' + str(right(x['Period'], 1)) if 'Total' not in x['Quarter'] and 'Quarter' in x['Quarter'] else x['Period'] , axis = 1)
df['Period'] = df.apply(lambda x: 'government-quarter/' + str(int(left(x['Period'], 4))) + '-' + str(int(left(x['Period'], 4)) + 1 ) + '/Q' + str(right(x['Period'], 1)) if 'Q' in x['Quarter'] and 'government' not in x['Period'] else x['Period'] , axis = 1)
df['Period'] = df.apply(lambda x: 'government-year/' + left(x['Period'], 4) + '-' + str(int(left(x['Period'], 4)) + 1) if 'Total' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('(R)', ''), axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('(P)', ''), axis = 1)
df['Period'] = df.apply(lambda x: right(x['Period'], 4) + ' ' + left(x['Period'], 3) if 'Year' not in x['Period'] and 'government' not in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: 'government-quarter/' + str(int(left(x['Period'], 4))) + '-' + str(int(left(x['Period'], 4)) + 1 ) + '/Q' + right(x['Period'], 3) if 'Year' not in x['Period'] and 'government' not in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Apr', '1'), axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Jul', '2'), axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Oct', '3'), axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Jan', '4'), axis = 1)
df['Period'] = df.apply(lambda x: 'government-year/' + left(right(x['Period'], 7), 4) + '-20' + right(x['Period'], 2) if 'Year' in x['Period'] else x['Period'], axis = 1)

df['Marker'] = df.apply(lambda x: 'Not Applicable' if 'Public Sector' in x['Housing Sector'] and 'Average Price' in x['Unit'] else '', axis = 1)
df['OBS'] = df.apply(lambda x: 0 if 'Public Sector' in x['Housing Sector'] and 'Average Price' in x['Unit'] else x['OBS'], axis = 1)

df.rename(columns={'OBS' : 'Value'}, inplace=True)

df = df.drop(['Year', 'Quarter'], axis=1)

df.head()


# In[15]:



from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[16]:



tidy = df[['Period','ONS Geography Code', 'House Price and Index Values','Housing Type','Housing Sector','Value','Measure Type','Unit','Marker']]

for column in tidy:
    if column in ('Marker', 'House Price and Index Values', 'Housing Type', 'Housing Type','Housing Sector'):
        tidy[column] = tidy[column].map(lambda x: pathify(x))

tidy.head(25)


# In[17]:


scraper.dataset.title = 'NIHE - Housing Stock'
scraper.dataset.comment = """
Note - Percentage change figures are calculated using unrounded figures
Results for the most recent quarter are provisional and subject to revision as more up-to-date data become available.
Figures can also change as a result of planned methodological changes, human error or system failures. As users should use the most recent full time series rather than appending new data to any previous back Series
Prices rounded to nearest £ hundred.
New Dwelling Sales and Prices include houses, bungalows, flats and maisonettes.
The figures for provisional and revised quarters are sourced from information held on NHBC's Fusion system as at 31st December 2019.
Changes can occur between figures published at different times owing to changes in policies and cancellations.
Average prices for areas with a small number of sales have been suppressed.
From April – June 2014 Local Government Districts (LGD) have been assigned to new dwellings by matching the dwelling postcode with the Northern Ireland Central Postcode Directory. In previous quarters the LGD stored on the NHBC database was used. These LGDs were either provided by builders or determined manually by NHBC staff referencing maps on the internet. Matching with the Central Postcode Directory is considered to provide a more accurate breakdown by LGD.
The figures are sourced from information held on NHBC's Fusion system as at 31st December 2019.
Changes can occur between figures published at different times owing to changes in policies and cancellations.
Please note that in some cases, average price figures are based on a particularly small number of new dwelling sales.
"""


# In[18]:


out = Path('out')
out.mkdir(exist_ok=True)

title = pathify('NIHE - Housing Stock')

tidy.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

scraper.dataset.family = 'homelessness'
scraper.dataset.theme = THEME['housing-planning-local-services']
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-homelessness/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

