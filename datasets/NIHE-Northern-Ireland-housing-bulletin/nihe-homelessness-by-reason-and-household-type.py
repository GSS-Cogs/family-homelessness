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

    if 'T2_1' in tab.name:

        cell = tab.filter(contains_string('Reason')) - tab.filter(contains_string('Homeless'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = cell.shift(0,2).expand(DOWN).is_not_blank() - remove

        reason = cell.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        year = cell.shift(0,2).expand(DOWN).filter(contains_string('201')) - remove

        observations = period.fill(RIGHT).is_not_blank()

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(reason, 'Reason for Homelessness', DIRECTLY, ABOVE),
                HDimConst('Household Composition', 'All'),
                HDimConst('Household Homeless Status', 'Presenting'),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Unit', 'Count'),
                HDim(year, 'Year', CLOSEST, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    elif 'T2_2' in tab.name:

        cell = tab.filter(contains_string('Household Type')) - tab.filter(contains_string('Households Presenting'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = cell.shift(0,2).expand(DOWN).is_not_blank() - remove

        compositionGen = cell.shift(RIGHT).expand(RIGHT).is_not_blank()

        compositionAge = cell.shift(1,1).expand(RIGHT).is_not_blank()

        year = cell.shift(0,2).expand(DOWN).filter(contains_string('201')) - remove

        observations = period.fill(RIGHT).is_not_blank()

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Reason for Homelessness', 'All'),
                HDim(compositionGen, 'Household Composition Gender', CLOSEST, LEFT),
                HDim(compositionAge, 'Household Composition Age', CLOSEST, LEFT),
                HDimConst('Household Homeless Status', 'Presenting'),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Unit', 'Count'),
                HDim(year, 'Year', CLOSEST, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidy = tidy_sheet.topandas()

        tidy['Household Composition'] = tidy['Household Composition Gender'] + ' ' + tidy['Household Composition Age']

        tidy = tidy.drop(['Household Composition Gender', 'Household Composition Age'], axis=1)

        tidied_sheets.append(tidy)

    elif 'T2_3' in tab.name:

        cell = tab.filter(contains_string('Reason')) - tab.filter(contains_string('Homeless Households'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = cell.shift(0,2).expand(DOWN).is_not_blank() - remove

        reason = cell.shift(RIGHT).expand(RIGHT).is_not_blank() - remove

        year = cell.shift(0,2).expand(DOWN).filter(contains_string('201')) - remove

        observations = period.fill(RIGHT).is_not_blank() - tab.filter(contains_string('Live')).expand(DOWN).expand(RIGHT)

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDim(reason, 'Reason for Homelessness', DIRECTLY, ABOVE),
                HDimConst('Household Composition', 'All'),
                HDimConst('Household Homeless Status', 'Accepted as Full Duty'),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Unit', 'Count'),
                HDim(year, 'Year', CLOSEST, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

        #The next two parts of this loop are to pick up columns Y and Z with different column values, this is a very long way to do it but it works.

        cell = tab.filter(contains_string('Full Duty Applicants')) - tab.filter(contains_string('Discharged Full Duty Applicants')) - tab.filter(contains_string('Homeless Households'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = tab.filter('2010-2011').expand(DOWN).is_not_blank() - remove

        year = tab.filter('2010-2011').shift(0,1).expand(DOWN).filter(contains_string('201')) - remove

        observations = cell.fill(DOWN).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Reason for Homelessness', 'All'),
                HDimConst('Household Composition', 'All'),
                HDimConst('Household Homeless Status', 'Live Full Duty'),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Unit', 'Count'),
                HDim(year, 'Year', CLOSEST, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())


        cell = tab.filter(contains_string('Discharged Full Duty Applicants'))

        remove = tab.filter(contains_string('Source:')).expand(LEFT).expand(DOWN).expand(RIGHT)

        period = tab.filter('2010-2011').expand(DOWN).is_not_blank() - remove

        year = tab.filter('2010-2011').shift(0,1).expand(DOWN).filter(contains_string('201')) - remove

        observations = cell.fill(DOWN).is_not_blank() - remove

        dimensions = [
                HDim(period, 'Period', DIRECTLY, LEFT),
                HDimConst('Reason for Homelessness', 'All'),
                HDimConst('Household Composition', 'All'),
                HDimConst('Household Homeless Status', 'Discharged Full Duty'),
                HDimConst('Measure Type', 'Houses'),
                HDimConst('Unit', 'Count'),
                HDim(year, 'Year', CLOSEST, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname="Preview.html")

        tidied_sheets.append(tidy_sheet.topandas())

    else:

        continue


# In[14]:


df = pd.concat(tidied_sheets, ignore_index = True, sort = False).fillna('')

df['OBS'] = df.apply(lambda x: str(x['OBS']).replace('', '19') if 'l' in x['DATAMARKER'] else x['OBS'], axis = 1)
df['DATAMARKER'] = df.apply(lambda x: str(x['DATAMARKER']).replace('l', '') if 'l' in x['DATAMARKER'] else x['DATAMARKER'], axis = 1)
df['DATAMARKER'] = df.apply(lambda x: 'Accepted during Quarter' if 'Duty' in x['Household Homeless Status'] else x['DATAMARKER'], axis = 1)

df['Period'] = df['Year'] + ' ' + df['Period']

df['Household Composition'] = df.apply(lambda x: str(x['Household Composition']).replace('females', 'Female'), axis = 1)
df['Household Composition'] = df.apply(lambda x: str(x['Household Composition']).replace('males', 'Male'), axis = 1)

df = df.drop(['Year'], axis=1)

df['Period'] = df.apply(lambda x: str(x['Period']).replace('(R)', '') if '(R)' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df['Period'].map(lambda x: 'government-year/' + left(x, 9) if left(right(x, 4),2) == '20' else x)
df['Period'] = df['Period'].map(lambda x: left(x, 5) + '20' + right(x, len(x) - 5) if '-201' not in x and 'government' not in x else x)
df['Period'] = df['Period'].map(lambda x: 'government-quarter/' + left(x, 9) + '/Q' + left(right(x, 7), 3) if 'government-year/' not in x and 'Total' not in x else x)
df['Period'] = df['Period'].map(lambda x: 'government-year/' + left(x, len(x) - 6) if 'Total' in x else x)

df['Period'] = df.apply(lambda x: str(x['Period']).replace('Apr', '1') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Jul', '2') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Oct', '3') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)
df['Period'] = df.apply(lambda x: str(x['Period']).replace('Jan', '4') if 'government-quarter' in x['Period'] else x['Period'], axis = 1)

df = df.replace({'Reason for Homelessness' : {
    'Accommodation not reasonable5' : 'Accommodation not reasonable',
    'Intimidation4' : 'Intimidation'},
                'DATAMARKER' : {
    '..' : 'Breakdown not available'},
                'Household Composition' : {
    'Couples Total' : 'Couples',
    'Families Total' : 'Families',
    'Pensioner Households Total' : 'Pensioner Households',
    'Total Total' : 'Total',
    'Undefined Total' : 'Undefined'}})

df.rename(columns={'OBS' : 'Value',
                   'DATAMARKER' : 'Marker'}, inplace=True)

df.head()


# In[15]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[16]:


tidy = df[['Period','Reason for Homelessness', 'Household Composition','Household Homeless Status','Value','Measure Type','Unit','Marker']]

for column in tidy:
    if column in ('Marker', 'Development Type', 'Building Stage', 'Housing Type'):
        tidy[column] = tidy[column].map(lambda x: pathify(x))

tidy.head(25)


# In[17]:


scraper.dataset.title = 'NIHE Homelessness by Reason and Household Type'
scraper.dataset.comment = """
Jul - Sep 2011, Oct - Dec 2011 and Jan - Mar 2012 homeless figures are not available on a quarterly basis due to the introduction of a new Housing Management System in July 2011.
Following the introduction of the new Housing Management System, no data on reason for presentation is available for 3,731 cases during the period Jul 2011 - Mar 2012 and 835 cases during the period Apr - Jun 2012. This is due to the merging of two systems, involving data migration and keying variations.
For the period Jul - Sep 2012 onwards data migration is no longer an issue.  Keying variations will account for a few of the no data on reason for presentation, but the majority relate to three possible outcomes, where the case has been rejected (applicant does not meet the statutory homeless criteria), cancelled (homelessness application registered in error) or concluded (applicant withdraws their homelessness application or where there has been no further contact from the applicant).
The intimidation category includes those intimidated due to anti-social behaviour, paramilitarism, sectarianism, racial abuse, sexual orientation or disability.  The category has been renamed from 'intimidation (civil disturbance)' to 'intimidation' however the data definition has not changed.
New breakdown categories for Accommodation not Reasonable (ANR) were introduced midway through Q1 2018. Therefore a significant number of cases relating to Q1 2018 cannot entirely be broken down by sub category, and as a result are presented as "Accomodation not reasonable - Generic".
Due to the live nature of the NIHE reporting system, which extracts data from the live system, all categories may be subject to change and adjustment as each quarterly report is download.
As a result of statistical disclosure control, data for "bomb /fire damage (civil disturbance)" now falls into the "Other" category.
In 2016/17 the mid-year introduction of an additional field in HMS for staff to record presenting reason had an impact on the specification of statistical reports.  This resulted in some data issues at year end which included an increase in the 'no data' category. Reports will be monitored going forward.
Until the final quarter 2011, the table was entitled “Homeless Households Awarded Priority Status by Reason”. The name of the table has been changed to “Homeless Households Accepted as Full Duty Applicants by Reason” to better reflect the terminology used the new Housing Management System (HMS). The two terms are essentially the same, but  because of changes in management procedures and the greater range of outcome decision options (e.g. ‘prevention’) recorded by the new HMS, data from July 2011 are not directly comparable with previous figures. See Appendix 1 for further details.
Figures for the period Apr 2010 to Jun 2011 include those Homeless Households accepted as Full Duty Applicants who were subsequently discharged. The Housing Executive can discharge its duty in one of three ways: by rehousing of the applicant in the social or private sector, by offering the applicant three reasonable offers of accommodation which are all refused or if the applicant rehouses him/herself and is no longer interested. Note that it is not possible to provide a breakdown of discharged Full Applicants into these three subgroups.
Following the introduction of the new Housing Management System discharged Full Duty Applicants were not included in figures for July 2011 onwards in reports published prior to the Jan - Mar 2013 bulletin.  Figures for 2012-13 onwards now include those Full Applicants who were subsequently discharged. It has not been possible to revise figures for the last 3 quarters of 2011-12 and the overall total for that year due to the introduction of the new HMS and keying variations. See Appendix 1 for further details.
Figures for Live Full Duty Applicants are based on the status of households accepted during the quarter only; they do not represent the overall total of the Live Full Duty Applicant cases.
At the end of each financial year, figures are updated due to end of year reporting. Those applicants who applied for FDA status in one quarter but were not accepted until a subsequent quarter are picked up in the end of year report.
In Q4 2017-18, there has been an adjustment in acceptances removing 9 from the annual total.  This is due to the Derry/Londonderry flood.  Cases were "accepted" in quarter 2 due to the flood but remedial work meant that they were able to return to their properties and the acceptances were cancelled.
New breakdown categories for Accommodation not Reasonable (ANR) were introduced midway through Q1 2018. Therefore a significant number of cases relating to Q1 2018 cannot entirely be broken down by sub category, and as a result are presented as ANR.
Due to introduction of  new breakdown subcategories, there is a nil return for generic ANR  from Q2 2018.
As a result of statistical disclosure control, numerous "Intimidation" sub-categories have been combined in January-March 2019 release.
"""


# In[18]:


out = Path('out')
out.mkdir(exist_ok=True)

title = pathify('NIHE Homelessness by Reason and Household Type')

tidy.drop_duplicates().to_csv(out / f'{title}.csv', index = False)

scraper.dataset.family = 'homelessness'
scraper.dataset.theme = THEME['housing-planning-local-services']
scraper.dataset.license = 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'

with open(out / f'{title}.csv-metadata.trig', 'wb') as metadata:
    metadata.write(scraper.generate_trig())

#csvw = CSVWMetadata('https://gss-cogs.github.io/family-homelessness/reference/')
#csvw.create(out / 'observations.csv', out / 'observations.csv-schema.json')

