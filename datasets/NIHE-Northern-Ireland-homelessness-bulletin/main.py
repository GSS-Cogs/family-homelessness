#!/usr/bin/env python
# coding: utf-8

# In[743]:


from gssutils import *
from databaker.framework import *
import json
import pandas as pd
import numpy as np
import glob
from pathlib import Path
import pyexcel
import messytables
from io import BytesIO
from ntpath import basename
import copy
import urllib.request
import ssl


# In[744]:


pd.set_option('display.float_format', lambda x: '%.0f' % x)


# In[745]:


info = json.load(open('info.json'))
landingPage = info['landingPage']
landingPage


# In[746]:


scraper = Scraper(seed='info.json')
scraper

distribution = scraper.distribution(latest=True)
distribution

from pandas import ExcelWriter

ssl._create_default_https_context = ssl._create_unverified_context

xls = pd.ExcelFile(distribution.downloadURL)
with ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer, sheet, index=False)
    writer.save()
tabs = loadxlstabs("data.xls")


def period_format(x):
    if 'g-H1' in x:
        return 'government-half' + '/' + x.split(':')[0] + '/' + 'H1'
    elif 'g-H2' in x:
        return 'government-half' + '/' + x.split(':')[0] + '/' + 'H2'
    elif 'g-Q1' in x:
        return 'government-quarter' + '/' + x.split(':')[0] + '/' + 'Q1'
    elif 'c-H1' in x:
        return 'half' + '/' + x.split(':')[0] + '-' + 'H1'
    elif 'c-H2' in x:
        return 'half' + '/' + x.split(':')[0] + '-' + 'H2'
    elif 'g-year' in x:
        return 'government-year' + '/' + x.split(':')[0]

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]


# In[747]:


tab_names = [tab.name for tab in tabs]
pres_start = tab_names.index('1_1')  # presentation start index
accept_start = tab_names.index('2_1')  # acceptance start index
temp_start = tab_names.index('3_1')  # tempprary accommodation start index
temp_end = tab_names.index('3_5') + 1  # tempprary accommodation end index

(pres_start, accept_start, temp_start, temp_end)


# In[748]:


presentations_tabs = tabs[pres_start: accept_start]
acceptance_tabs = tabs[accept_start: temp_start]
accommodation_tabs = tabs[temp_start: temp_end]

trace = TransformTrace()


# In[749]:


tidied_presentation = []

for tab in presentations_tabs:
    title = 'NIHE Homelessness Presentations'
    scraper.dataset.title = title

    if tab.name in ['1_1', '1_1A', '1_1B', '1_1C', '1_1D', '1_5']:

        print(tab.name)

        cell = tab.excel_ref('A2')
        reason = cell.fill(RIGHT).is_not_blank()

        if tab.name == '1_5':
            footnote = reason.fill(DOWN).filter('Source:NIHE').expand(LEFT).expand(DOWN)
        else:
            footnote = reason.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)

        remove_total = tab.excel_ref('A').filter('Total')

        quarter = cell.fill(DOWN).regex('[^0-9]+') - remove_total - footnote
        year = cell.fill(DOWN).is_not_blank() - remove_total - quarter - footnote

        observations = reason.fill(DOWN).is_not_blank() - footnote

        if tab.name == '1_1':
            reason_title = 'Reason for Homelessness'
        elif tab.name == '1_1A':
            reason_title = 'Accommodation not Reasonable breakdown'
        elif tab.name == '1_1B':
            reason_title = 'Intimidation breakdown'
        elif tab.name == '1_1C':
            reason_title = 'Loss of rented Accommodation reason'
        elif tab.name == '1_1D':
            reason_title = 'Release from facilities breakdown'
        elif tab.name == '1_5':
            reason_title = 'Legislative test Outcome'
        dimensions = [
            HDimConst('Measure Type', 'Household'),
            HDimConst('Unit', 'Count'),
            HDimConst('ONS Geography code', "N07000001"),
            HDim(year, 'Period', CLOSEST, UP),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(reason, reason_title, DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        tidied_presentation.append(table)

    elif tab.name == '1_2':
        print(tab.name)

        cell = tab.excel_ref('A2')

        age = tab.excel_ref('B3').expand(RIGHT) - tab.excel_ref('O3').expand(RIGHT)
        household = age.shift(UP)
        backupHC = age.shift(0, -2)

        footnote = household.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        total = tab.excel_ref('A').filter('Total')
        quarter = tab.excel_ref('A4').expand(DOWN).regex('[^0-9]+') - total - footnote
        year = cell.fill(DOWN).is_not_blank().is_not_blank() - total - quarter - footnote
        yearAlt = tab.excel_ref('A4').expand(DOWN).regex('[0-9]') - footnote

        observations = tab.excel_ref('B5').expand(DOWN).expand(RIGHT).is_not_blank() - footnote
        observations1 = year.fill(RIGHT).is_not_blank()
        dimensions = [
            HDimConst('Measure Type', 'Household'),
            HDimConst('Unit', 'Count'),
            HDimConst('ONS Geography code', "N07000001"),
            HDim(year, 'Period', CLOSEST, ABOVE),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(household, 'Household Composition', CLOSEST, LEFT),
            HDim(age, 'Age Group', DIRECTLY, ABOVE),
            HDim(backupHC, 'Backup HC', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        table = table.replace({'Backup HC' : {'Unnamed: 1' : 'Single males', 'Unnamed: 2' : 'Single males', 'Unnamed: 3' : 'Single males', 'Unnamed: 4' : 'Single males',
                                             'Unnamed: 5' : 'Single females', 'Unnamed: 6' : 'Single females', 'Unnamed: 7' : 'Single females', 'Unnamed: 8' : 'Single females'}})

        table['Household Composition'] = table.apply(lambda x: x['Backup HC'] if 'Unnamed' not in x['Backup HC'] else x['Household Composition'], axis = 1)

        table = table.drop(columns = ['Backup HC'])

        #This is a real scuffed way to do this but I cannot remember the way we sorted it before and this works so screw it

        table['Household Composition'] = table['Household Composition'].astype(str) + ' ' + table['Age Group'].astype(
            str).replace(r'\(.*\)', ' ')
        table.drop(['Age Group'], axis=1, inplace=True)
        tidied_presentation.append(table)

    elif tab.name == '1_3':
        print(tab.name)

        presenters = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
        quarter = presenters.shift(UP).is_not_blank()
        year = quarter.shift(UP).is_not_blank()
        footnote = presenters.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        location = tab.excel_ref('A5').expand(DOWN).is_not_blank() - footnote

        observations = presenters.fill(DOWN).is_not_blank() - footnote
        dimensions = [
            HDimConst('Measure Type', 'Household'),
            HDimConst('Unit', 'Count'),
            HDim(year, 'Period', CLOSEST, LEFT),
            HDim(quarter, 'Quarter', CLOSEST, LEFT),
            HDim(presenters, 'Homeless Presenters', DIRECTLY, ABOVE),
            HDim(location, 'ONS Geography code', DIRECTLY, LEFT)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        table.loc[(table['Homeless Presenters'] == 'Total presenter'), 'Unit'] = 'Count'
        table.loc[(table['Homeless Presenters'] == 'Presenters per 1,000 population'), 'Unit'] = 'Per 1,000 population'
        table.drop(['Homeless Presenters'], axis=1, inplace=True)

        table.to_csv('table 1_3.csv')

        tidied_presentation.append(table)


    elif tab.name == '1_4':
        print(tab.name)

        year = tab.excel_ref('B2').expand(RIGHT).is_not_blank()
        quarter = tab.excel_ref('B3').expand(RIGHT).is_not_blank()

        footnote = quarter.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        assessment = tab.excel_ref('A4').expand(DOWN).is_not_blank() - footnote
        observations = quarter.fill(DOWN).is_not_blank() - footnote

        dimensions = [
            HDimConst('Measure Type', 'Household'),
            HDimConst('Unit', 'Count'),
            HDimConst('ONS Geography code', "N07000001"),
            HDim(year, 'Period', DIRECTLY, ABOVE),
            HDim(quarter, 'Quarter', DIRECTLY, ABOVE),
            HDim(assessment, 'Assessment Decision', DIRECTLY, LEFT),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        tidied_presentation.append(table)


    elif tab.name == '1_6':
        print(tab.name)

        footnote = tab.excel_ref('B').filter('Source: NIHE').expand(LEFT).expand(DOWN)
        year = tab.excel_ref('A3').expand(DOWN).is_not_blank() - footnote
        presenters = tab.excel_ref('B2')
        observations = presenters.fill(DOWN) - footnote

        dimensions = [
            HDimConst('Measure Type', 'Household'),
            HDimConst('Unit', 'Count'),
            HDimConst('ONS Geography code', "N07000001"),
            HDim(year, 'Period', DIRECTLY, LEFT),
            HDim(presenters, 'Repeat Homeless Presentations', DIRECTLY, ABOVE)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        tidied_presentation.append(table)

df = pd.concat(tidied_presentation).fillna('')

df['Period'] = df['Period'].str.replace('\.0', '')
df['Period'] = df['Period'].str.replace(r'\(.*\).*', '')
df['Period'] = df['Period'].str.rstrip()
df['Quarter'] = df['Quarter'].str.replace(r'\(.*\).*', '')
df['Quarter'] = df['Quarter'].str.rstrip('123 ')

df = df.replace({'Quarter':
                     {'Apr-Sep': 'g-H1',
                      'April-September': 'g-H1',
                      'Oct-Mar': 'g-H2',
                      'October-March': 'g-H2',
                      'Apr-Jun': 'g-Q1',
                      'Jan-Jun': 'c-H1',
                      'January-June': 'c-H1',
                      'Jul-Dec': 'c-H2',
                      'July-December': 'c-H2',
                      'Jul-Dec³': 'c-H2',
                      '': 'g-year'
                      }})

df['Period'] = df['Period'] + ':' + df['Quarter']
df['Period'] = df['Period'].apply(period_format)
df.drop(['Quarter'], axis=1, inplace=True)

df = df.replace({'ONS Geography code':
                     {'Antrim and Newtownabbey': 'N09000001',
                      'Ards and North Down': 'N09000011',
                      'Armagh City, Banbridge and Craigavon': 'N09000002',
                      'Belfast': 'N09000003',
                      'Causeway Coast and Glens': 'N09000004',
                      'Derry City and Strabane': 'N09000005',
                      'Fermanagh and Omagh': 'N09000006',
                      'Lisburn and Castlereagh': 'N09000007',
                      'Mid and East Antrim': 'N09000008',
                      'Mid Ulster': 'N06000010',
                      'Newry, Mourne and Down': 'N09000010',
                      'Northern Ireland': 'N92000002'
                      }})

df.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)

df = df[['Period', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation breakdown',
         'Loss of rented Accommodation reason', 'Release from facilities breakdown', 'Household Composition',
         'ONS Geography code', 'Assessment Decision', 'Legislative test Outcome', 'Repeat Homeless Presentations',
         'Measure Type', 'Unit', 'Value', 'Marker']]

bulletin_df = df

def process_tab():
    get_ipython().run_line_magic('run', '-i "NIHE-northern-ireland-housing-statistics"')
    return tidy

stats_df = process_tab()

stats_df["Measure Type"] = 'count'
stats_df  = df[["Period", "Homelessness Reason", "House_Hold_Type", "Outcome", "Age", "Measure Type", "Unit", "Value", "MARKER"]]

stats_df = stats_df.rename(columns={"Homelessness Reason" : "Reason for Homelessness", "Outcome" : "Assessment Decision", "House_Hold_Type" : "Household Composition", "MARKER" : "Marker"})

stats_df


# In[750]:


bulletin_df[["Measure Type", "Unit"]] = bulletin_df[["Unit", "Measure Type"]]

bulletin_df


# In[751]:


df = pd.concat([bulletin_df, stats_df], sort = False)

df = df[['Period', 'Age', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation breakdown',
         'Loss of rented Accommodation reason', 'Release from facilities breakdown', 'Household Composition',
         'ONS Geography code', 'Assessment Decision', 'Legislative test Outcome', 'Repeat Homeless Presentations',
         'Measure Type', 'Unit', 'Value', 'Marker']]

df['Age'] = df['Age'].str.replace(' ', '').fillna('All')
df['Reason for Homelessness'] = df['Reason for Homelessness'].str.strip()
df = df.fillna('')

df = df.rename(columns={"ONS Geography code" : "ONS Geography Code",
                        'Accommodation not Reasonable breakdown' : 'Accommodation Not Reasonable Breakdown',
                        'Intimidation breakdown' : 'Intimidation Breakdown',
                        'Loss of rented Accommodation reason' : 'Reason for Loss of Rented Accommodation',
                        'Release from facilities breakdown' : 'Release from Facilities Breakdown',
                        'Legislative test Outcome' : 'Legislative Test Outcome',
                        'Age' : 'Age Group'})

df = df.replace({'Age' : {'nan' : 'All',},
                 'Household Composition' : {'nan' : 'All'},
                 'Assessment Decision' : {'nan' : 'All'},
                 'Measure Type' : {'Per 1,000 population' : 'count per 1000 population'},
                 'ONS Geography Code' : {'' : 'N92000002'},
                 'Value' : {'nan' : ''},
                 'Marker' : {'*' : 'Suppressed',
                             '-' : 'None'}})

df['Value'] = df.apply(lambda x: int(x['Value']) if x['Marker'] == '' else x['Value'], axis = 1)

COLUMNS_TO_PATHIFY = ['Measure Type', 'Unit', 'Marker']

for col in df.columns.values.tolist():
	if col not in COLUMNS_TO_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

df['Age Group'] = df.apply(lambda x: mid(x['Household Composition'], 13, 5) if 'yrs' in x['Household Composition'] and 'fe' not in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df.apply(lambda x: mid(x['Household Composition'], 15, 5) if 'yrs' in x['Household Composition'] and 'fe' in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df.apply(lambda x: 'total' if 'total' in x['Household Composition'] and 'male' in x['Household Composition'] else x['Age Group'], axis = 1)

df = df.replace({'Household Composition' : {'Families¹ ' : 'Families',
                                            'Pensioner  households' : 'Pensioners',
                                            'Single females 16-17 yrs' : 'Single Females',
                                            'Single females 18-25 yrs' : 'Single Females',
                                            'Single females 26-59 yrs' : 'Single Females',
                                            'Single females Total'     : 'Single Females',
                                            'Single females' : 'Single Females',
                                            'Single males 16-17 yrs' : 'Single Males',
                                            'Single males 18-25 yrs' : 'Single Males',
                                            'Single males 26-59 yrs' : 'Single Males',
                                            'Single males Total'     : 'Single Males',
                                            'Single males' : 'Single Males',
                                            'Total ' : 'All'},
                 'Age Group' : {'all' : 'All'}})

df['Reason for Homelessness'] = df['Reason for Homelessness'].str.replace('/' , ' ').str.replace('\\' , ' ')

df = df.replace({'Reason for Homelessness' : {  'Accommodation not reasonable' : 'Accommodation not Reasonable', 
                                                'Accomodation not reasonable' : 'Accommodation not Reasonable', 
                                                'Bomb fire damage (Civil disturbance)' : 'Bomb/Fire damage (Civil Disturbance)',
                                                'Bomb fire damage (civil disturbance)' : 'Bomb/Fire damage (Civil Disturbance)',
                                                'Bomb fire damage (civil disturbance)' : 'Bomb/Fire damage (Civil Disturbance)',
                                                'Discharged full duty applicants' : 'Discharged Full Duty Applicants', 
                                                'Domestic violence' : 'Domestic Violence',
                                                'Fire flood other emergency' : 'Fire/Flood/Other Emergency', 
                                                'Fire flood other emergency' : 'Fire/Flood/Other Emergency', 
                                                'Intimidation4' : 'Intimidation', 
                                                'Intimidation6' : 'Intimidation', 
                                                'Live full duty applicants' : 'Live Full Duty Applicants', 
                                                'Loss of rented accommodation' : 'Loss of Rented Accommodation',
                                                'Marital   relationship breakdown' : 'Marital/Relationship breakdown', 
                                                'Marital relationship breakdown' : 'Marital/Relationship breakdown', 
                                                'Mortgage default' : 'Mortgage Default', 
                                                'Neighbourhood harassment' : 'Neighbourhood Harassment',
                                                'No Data on reason for presentation' : 'No Data on Reason for Presentation',
                                                'No accommodation in Northern Ireland' : 'No Accommodation in Northern Ireland',
                                                'No accomodation in Northern Ireland' : 'No Accommodation in Northern Ireland',
                                                'No data on reason for presentation' : 'No Data on Reason for Presentation', 
                                                'Other reasons' : 'Other',
                                                'Release from hospital prison other institution' : 'Release from Hospital Prison or Other Institution',
                                                'Release from hospital prison other institution' : 'Release from Hospital Prison or Other Institution',
                                                'Sharing breakdown family dispute' : 'Sharing Breakdown/Family Dispute', 
                                                'Sharing breakdown  family dispute' : 'Sharing Breakdown/Family Dispute', 
                                                'Total' : 'All'},
                     'Accommodation Not Reasonable Breakdown' : {'Accomodation not reasonable: Generic1' : 'Accommodation not Reasonable: Generic', 
                                                'Total' : 'All'},
                     'Intimidation Breakdown' : {'Intidimidation:Anti-social behaviour' : 'Intidimidation: Anti-Social behaviour',
                                                 'Total' : 'All'},
                     'Reason for Loss of Rented Accommodation' : {
                                                 'LOPRA: fitness/ repairs' : 'LOPRA: Fitness/Repairs', 
                                                 'LOPRA: landlord dispute' : 'LOPRA: Landlord Dispute',
                                                 'LOPRA: other' : 'LOPRA: Other',
                                                 'LOPRA: property sale' : 'LOPRA: Property Sale',
                                                 'LOPRA²: affordability' : 'LOPRA: Affordability',
                                                 'Loss of HA accomodation: anti-social behaviour' : 'Loss of HA Accommodation: Anti-Social Behaviour',
                                                 'Loss of HA accomodation: other' : 'Loss of HA Accommodation: Other',
                                                 'Loss of HA³ accomodation: arrears' : 'Loss of HA Accommodation: Arrears',
                                                 'Loss of NIHE accomodation: other' : 'Loss of NIHE Accommodation: Other',
                                                 'Loss of NIHE⁴ accomodation: arrears' : 'Loss of NIHE Accommodation: Arrears',
                                                 'Loss of rented accommodation¹ ': 'Loss of Rented Accommodation',
                                                 'Total' : 'All'}})

df['Reason for Homelessness'] = df.apply(lambda x: 'Accommodation not Reasonable' if (x['Reason for Homelessness'] == '') and (x['Accommodation Not Reasonable Breakdown'] != '') else x['Reason for Homelessness'], axis = 1)
df['Reason for Homelessness'] = df.apply(lambda x: 'Intimidation' if (x['Reason for Homelessness'] == '') and (x['Intimidation Breakdown'] != '') else x['Reason for Homelessness'], axis = 1)
df['Reason for Homelessness'] = df.apply(lambda x: 'Release from Hospital Prison or Other Institution' if (x['Reason for Homelessness'] == '') and (x['Release from Facilities Breakdown'] != '') else x['Reason for Homelessness'], axis = 1)

COLUMNS_TO_NOT_NA = ['Reason for Homelessness', 'Household Composition', 'Priority Need Category', 'Housing Assessment Outcome', 'Marker', 'Value']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_NA:
		continue
	else:
         df[col] = df[col].replace("", "NA")


for col in df.columns.values.tolist():
	if col in ['Marker', 'Value']:
		continue
	else:
         df[col] = df[col].replace("", "All")
         df[col] = df[col].replace("Total", "All")

df


# In[752]:


scraper = Scraper(seed='info.json')

scraper.dataset.license = "".join([x.strip().replace('"', '') for x in scraper.dataset.license.split(" ")])

scraper.dataset.title = "NIHE - Homelessness Presentations"
scraper.dataset.comment = 'The Northern Ireland Homelessness bulletin is a biannual publication which contains information on a range of areas relating to homelessness. The report is currently divided into three sections which are: Homeless Presenters; Homeless Acceptances; and Temporary Accommodation.'

df.to_csv(pathify(scraper.dataset.title) + '-observations.csv', index=False)

catalog_metadata = scraper.as_csvqb_catalog_metadata()
catalog_metadata.to_json_file(pathify(scraper.dataset.title) + '-catalog-metadata.json')


# In[753]:


tidied_acceptance = []

for tab in acceptance_tabs:
    title = 'NIHE Homelessness Acceptances'
    scraper.dataset.title = title

    if tab.name == '2_1':
        print(tab.name)

        cell = tab.excel_ref('A2')
        reason = cell.fill(RIGHT) - tab.excel_ref('R2').expand(RIGHT)

        footnote = cell.fill(RIGHT).fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        observations = tab.excel_ref('B5').expand(RIGHT).expand(DOWN).is_not_blank() - footnote
        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote

        status = reason.shift(0, 1).expand(RIGHT)

        reason_override = {}
        for x in reason:
            if xypath.contrib.excel.excel_location(x) in ['P2', 'Q2']:
                reason_override[x.value] = 'Status of Household'

        reason_title = 'Reason for Homelessness'

        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDimConst('Assessment Decision', 'Accepted'),
            HDimConst('ONS Geography Code', "N07000001"),
            HDim(year, 'Period', CLOSEST, UP),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(status, 'Status', DIRECTLY, ABOVE),
            HDim(reason, reason_title, DIRECTLY, ABOVE, cellvalueoverride=reason_override)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        table['Reason for Homelessness'] = (table['Reason for Homelessness'] + ' ' + table['Status']).str.strip()
        table = table.drop(columns=['Status'])
        tidied_acceptance.append(table)

    if tab.name in ['2_1A', '2_1B', '2_1C', '2_5', '2_6']:
        print(tab.name)

        cell = tab.excel_ref('A2')

        if tab.name in ['2_1A', '2_1B', '2_1C']:
            reason = cell.fill(RIGHT).is_not_blank()
            footnote = reason.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
            observations = reason.fill(DOWN).is_not_blank() - footnote
        elif tab.name in ['2_5', '2_6']:
            reason = cell.fill(RIGHT).is_not_blank()
            footnote = reason.fill(DOWN).filter('Source:NIHE').expand(LEFT).expand(DOWN)
            observations = reason.fill(DOWN).is_not_blank() - footnote

        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote

        if tab.name == '2_1A':
            reason_title = 'Accommodation not Reasonable breakdown'
        elif tab.name == '2_1B':
            reason_title = 'Intimidation breakdown'
        elif tab.name == '2_1C':
            reason_title = 'Release from facilities breakdown'
        elif tab.name == '2_5':
            reason_title = 'Priority need Category'
        elif tab.name == '2_6':
            reason_title = 'Housing Assessment Outcome'

        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDimConst('Assessment Decision', 'Accepted'),
            HDimConst('ONS Geography Code', "N07000001"),
            HDim(year, 'Period', CLOSEST, UP),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(reason, reason_title, DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        tidied_acceptance.append(table)

    elif tab.name == '2_2':
        print(tab.name)

        cell = tab.excel_ref('A2')

        age = tab.excel_ref('B3').expand(RIGHT) - tab.excel_ref('O3').expand(RIGHT)
        household = age.shift(UP)
        backupHC = age.shift(0, -2)

        footnote = household.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        total = tab.excel_ref('A').filter('Total')
        quarter = tab.excel_ref('A4').expand(DOWN).regex('[^0-9]+') - total - footnote
        year = cell.fill(DOWN).is_not_blank().is_not_blank() - total - quarter - footnote

        observations = tab.excel_ref('B5').expand(DOWN).expand(RIGHT).is_not_blank() - footnote
        observations_alt = year.fill(RIGHT).is_not_blank()

        dimensions = [
            HDimConst('Measure Type', 'Household'),
            HDimConst('Unit', 'Count'),
            HDimConst('Assessment Decision', 'Accepted'),
            HDimConst('ONS Geography Code', "N07000001"),
            HDim(year, 'Period', CLOSEST, ABOVE),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(household, 'Household Composition', DIRECTLY, ABOVE),
            HDim(age, 'Age', DIRECTLY, ABOVE),
            HDim(backupHC, "Backup HC", DIRECTLY, ABOVE)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        table = table.replace({'Backup HC' : {'Unnamed: 1' : 'Single males', 'Unnamed: 2' : 'Single males', 'Unnamed: 3' : 'Single males', 'Unnamed: 4' : 'Single males',
                                             'Unnamed: 5' : 'Single females', 'Unnamed: 6' : 'Single females', 'Unnamed: 7' : 'Single females', 'Unnamed: 8' : 'Single females'}})

        table['Household Composition'] = table.apply(lambda x: x['Backup HC'] if 'Unnamed' not in x['Backup HC'] else x['Household Composition'], axis = 1)

        table = table.drop(columns = ['Backup HC'])

        table['Household Composition'] = table['Household Composition'].astype(str) + ' ' + table['Age'].astype(
            str).replace(r'\(.*\).*', '')
        table.drop(columns='Age', inplace=True)
        tidied_acceptance.append(table)

    elif tab.name == '2_3':
        print(tab.name)

        year = tab.excel_ref('A2').fill(RIGHT).is_not_blank()
        quarter = year.shift(DOWN)
        footnote = year.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        location = tab.excel_ref('A2').fill(DOWN).is_not_blank() - footnote

        observations = quarter.fill(DOWN).is_not_blank() - footnote
        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDimConst('Assessment Decision', 'Accepted'),
            HDim(year, 'Period', DIRECTLY, ABOVE),
            HDim(quarter, 'Quarter', DIRECTLY, ABOVE),
            HDim(location, 'ONS Geography Code', DIRECTLY, LEFT)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        tidied_acceptance.append(table)

    elif tab.name == '2_4':
        print(tab.name)

        year = tab.excel_ref('B2').expand(RIGHT).is_not_blank()

        footnote = year.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        location = tab.excel_ref('A2').fill(DOWN).is_not_blank() - footnote
        observations = year.fill(DOWN).is_not_blank() - footnote

        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDimConst('Assessment Decision', 'Discharged'),
            HDim(year, 'Period', DIRECTLY, ABOVE),
            HDim(location, 'ONS Geography Code', DIRECTLY, LEFT)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        tidied_acceptance.append(table)

    elif tab.name == '2_7':
        print(tab.name)

        quarter = tab.excel_ref('B3').expand(RIGHT).is_not_blank()
        year = quarter.shift(UP)
        footnote = quarter.fill(DOWN).filter('Source:NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        age_category = tab.excel_ref('A3').fill(DOWN).is_not_blank() - footnote

        observations = quarter.fill(DOWN).is_not_blank() - footnote

        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDimConst('Assessment Decision', 'Accepted'),
            HDim(age_category, 'Age Group', DIRECTLY, LEFT),
            HDim(year, 'Period', DIRECTLY, ABOVE),
            HDim(quarter, 'Quarter', DIRECTLY, ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        tidied_acceptance.append(table)

df = pd.concat(tidied_acceptance).fillna('')

df['Period'] = df['Period'].str.replace('\.0', '')
df['Period'] = df['Period'].str.replace(r'\(.*\).*', '')
df['Period'] = df['Period'].str.rstrip()
df['Quarter'] = df['Quarter'].str.replace(r'\(.*\).*', '')
df['Quarter'] = df['Quarter'].str.rstrip('123 ')
df['Period'] = df['Period'].str.replace('/' , '-20')

df = df.replace({'Quarter':
                     {'Apr-Sep': 'g-H1',
                      'Oct-Mar': 'g-H2',
                      'Apr-Jun': 'g-Q1',
                      'Apr-Jun ': 'g-Q1',
                      'Jan-Jun': 'c-H1',
                      'Jul-Dec': 'c-H2',
                      'Jul-Dec³': 'c-H2',
                      '': 'g-year'
                      }})

df['Period'] = df['Period'] + ':' + df['Quarter']
df['Period'] = df['Period'].apply(period_format)
df.drop(['Quarter'], axis=1, inplace=True)

df = df.replace({'ONS Geography Code':
                     {'Antrim and Newtownabbey': 'N09000001',
                      'Ards and North Down': 'N09000011',
                      'Armagh City, Banbridge and Craigavon': 'N09000002',
                      'Belfast': 'N09000003',
                      'Causeway Coast and Glens': 'N09000004',
                      'Derry City and Strabane': 'N09000005',
                      'Fermanagh and Omagh': 'N09000006',
                      'Lisburn and Castlereagh': 'N09000007',
                      'Mid and East Antrim': 'N09000008',
                      'Mid Ulster': 'N06000010',
                      'Newry, Mourne and Down': 'N09000010',
                      'Northern Ireland': 'N07000001'
                      }})

df.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)

df[["Measure Type", "Unit"]] = df[["Unit", "Measure Type"]]

df = df.replace({'ONS Geography Code' : {'' : 'N92000002'},
                 'Value' : {'nan' : ''},
                 'Marker' : {'*' : 'Suppressed',
                             '-' : 'None'}})

COLUMNS_TO_PATHIFY = ['Measure Type', 'Unit', 'Marker']

for col in df.columns.values.tolist():
	if col not in COLUMNS_TO_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

df = df.rename(columns={'Accommodation not Reasonable breakdown' : 'Accommodation Not Reasonable Breakdown',
                        'Intimidation breakdown' : 'Intimidation Breakdown',
                        'Release from facilities breakdown' : 'Release from Facilities Breakdown',
                        'Priority need Category' : 'Priority Need Category'})

df['Age Group'] = df.apply(lambda x: mid(x['Household Composition'], 13, 5) if 'yrs' in x['Household Composition'] and 'fe' not in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df.apply(lambda x: mid(x['Household Composition'], 15, 5) if 'yrs' in x['Household Composition'] and 'fe' in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df.apply(lambda x: 'total' if 'total' in x['Household Composition'] and 'male' in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df['Age Group'].replace('', 'All')

df['Value'] = df.apply(lambda x: int(x['Value']) if x['Marker'] == '' else x['Value'], axis = 1)

df = df.replace({'Household Composition' : {'Families¹ ' : 'Families',
                                            'Pensioner  households' : 'Pensioners',
                                            'Single females 16-17 yrs' : 'Single Females',
                                            'Single females 18-25 yrs' : 'Single Females',
                                            'Single females 26-59 yrs' : 'Single Females',
                                            'Single females Total'     : 'Single Females',
                                            'Single females'           : 'Single Females',
                                            'Single males 16-17 yrs' : 'Single Males',
                                            'Single males 18-25 yrs' : 'Single Males',
                                            'Single males 26-59 yrs' : 'Single Males',
                                            'Single males Total'     : 'Single Males',
                                            'Single males' : 'Single Males'}})

df = df[['Period', 'Reason for Homelessness', 'Accommodation Not Reasonable Breakdown', 'Intimidation Breakdown',
         'Release from Facilities Breakdown', 'Household Composition', 'ONS Geography Code', 'Priority Need Category',
         'Housing Assessment Outcome', 'Age Group', 'Assessment Decision', 'Measure Type', 'Unit', 'Value', 'Marker']]

df['Reason for Homelessness'] = df.apply(lambda x: 'Accommodation not Reasonable' if (x['Reason for Homelessness'] == '') and (x['Accommodation Not Reasonable Breakdown'] != '') else x['Reason for Homelessness'], axis = 1)
df['Reason for Homelessness'] = df.apply(lambda x: 'Intimidation' if (x['Reason for Homelessness'] == '') and (x['Intimidation Breakdown'] != '') else x['Reason for Homelessness'], axis = 1)
df['Reason for Homelessness'] = df.apply(lambda x: 'Release from Hospital Prison or Other Institution' if (x['Reason for Homelessness'] == '') and (x['Release from Facilities Breakdown'] != '') else x['Reason for Homelessness'], axis = 1)

df['Reason for Homelessness'] = df['Reason for Homelessness'].str.replace('/' , ' ').str.replace('\\' , ' ')

df = df.replace({'Reason for Homelessness' : {  'Accommodation not reasonable' : 'Accommodation not Reasonable', 
                                                'Accomodation not reasonable' : 'Accommodation not Reasonable', 
                                                'Bomb fire damage (Civil disturbance)' : 'Bomb/Fire damage (Civil Disturbance)',
                                                'Bomb fire damage (civil disturbance)' : 'Bomb/Fire damage (Civil Disturbance)',
                                                'Bomb fire damage (civil disturbance)' : 'Bomb/Fire damage (Civil Disturbance)',
                                                'Discharged full duty applicants' : 'Discharged Full Duty Applicants', 
                                                'Domestic violence' : 'Domestic Violence',
                                                'Fire flood other emergency' : 'Fire/Flood/Other Emergency', 
                                                'Fire flood other emergency' : 'Fire/Flood/Other Emergency', 
                                                'Intimidation4' : 'Intimidation', 
                                                'Intimidation6' : 'Intimidation', 
                                                'Live full duty applicants' : 'Live Full Duty Applicants', 
                                                'Loss of rented accommodation' : 'Loss of Rented Accommodation',
                                                'Marital   relationship breakdown' : 'Marital/Relationship breakdown', 
                                                'Marital relationship breakdown' : 'Marital/Relationship breakdown', 
                                                'Mortgage default' : 'Mortgage Default', 
                                                'Neighbourhood harassment' : 'Neighbourhood Harassment',
                                                'No Data on reason for presentation' : 'No Data on Reason for Presentation',
                                                'No accommodation in Northern Ireland' : 'No Accommodation in Northern Ireland',
                                                'No accomodation in Northern Ireland' : 'No Accommodation in Northern Ireland',
                                                'No data on reason for presentation' : 'No Data on Reason for Presentation', 
                                                'Other reasons' : 'Other',
                                                'Release from hospital prison other institution' : 'Release from Hospital Prison or Other Institution',
                                                'Release from hospital prison other institution' : 'Release from Hospital Prison or Other Institution',
                                                'Sharing breakdown family dispute' : 'Sharing Breakdown/Family Dispute', 
                                                'Sharing breakdown  family dispute' : 'Sharing Breakdown/Family Dispute'},
                     'Accommodation Not Reasonable Breakdown' : {'Accomodation not reasonable: Generic1' : 'Accommodation not Reasonable: Generic'},
                     'Intimidation Breakdown' : {'Intidimidation:Anti-social behaviour' : 'Intidimidation: Anti-Social behaviour'}})

COLUMNS_TO_NOT_NA = ['Reason for Homelessness', 'Household Composition', 'Priority Need Category', 'Housing Assessment Outcome', 'Marker', 'Value']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_NA:
		continue
	else:
         df[col] = df[col].replace("", "NA")


for col in df.columns.values.tolist():
	if col in ['Marker', 'Value']:
		continue
	else:
         df[col] = df[col].replace("", "All")
         df[col] = df[col].replace("Total", "All")
         df[col] = df[col].replace("Total ", "All")

df


# In[754]:


scraper.dataset.license = "".join([x.strip().replace('"', '') for x in scraper.dataset.license.split(" ")])

scraper.dataset.title = 'NIHE - Homelessness Acceptances'
scraper.dataset.comment = 'The Northern Ireland Homelessness bulletin is a biannual publication which contains information on a range of areas relating to homelessness. The report is currently divided into three sections which are: Homeless Presenters; Homeless Acceptances; and Temporary Accommodation.'

df.to_csv(pathify(scraper.dataset.title) + '-observations.csv', index=False)

catalog_metadata = scraper.as_csvqb_catalog_metadata()
catalog_metadata.to_json_file(pathify(scraper.dataset.title) + '-catalog-metadata.json')


# In[755]:


tidied_accomodation = []

for tab in accommodation_tabs:
    title = 'NIHE - Temporary Accommodation'
    scraper.dataset.title = title

    if tab.name == '3_1':
        print(tab.name)

        cell = tab.excel_ref('A2')
        age = tab.excel_ref('B3').expand(RIGHT) - tab.excel_ref('O3').expand(RIGHT)
        household = age.shift(UP)
        backupHC = age.shift(0, -2)

        footnote = household.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        observations = age.fill(DOWN).is_not_blank() - footnote

        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote

        dimensions = [
            HDimConst('Measure Type', 'Placements'),
            HDimConst('Unit', 'Count'),
            HDim(year, 'Period', CLOSEST, ABOVE),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(household, 'Household Composition', CLOSEST, LEFT),
            HDim(age, 'Age', DIRECTLY, ABOVE),
            HDim(backupHC, 'Backup HC', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        table = table.replace({'Backup HC' : {'Unnamed: 1' : 'Single males', 'Unnamed: 2' : 'Single males', 'Unnamed: 3' : 'Single males', 'Unnamed: 4' : 'Single males',
                                             'Unnamed: 5' : 'Single females', 'Unnamed: 6' : 'Single females', 'Unnamed: 7' : 'Single females', 'Unnamed: 8' : 'Single females'}})

        table['Household Composition'] = table.apply(lambda x: x['Backup HC'] if 'Unnamed' not in x['Backup HC'] else x['Household Composition'], axis = 1)

        table = table.drop(columns = ['Backup HC'])

        table['Household Composition'] = table['Household Composition'].astype(str) + ' ' + table['Age'].astype(str)
        table.drop(columns='Age', inplace=True)
        tidied_accomodation.append(table)

    elif tab.name == '3_2':
        print(tab.name)

        cell = tab.excel_ref('A2')
        description = cell.fill(RIGHT).is_not_blank()
        description_title = 'Accommodation Type'
        footnote = description.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        observations = description.fill(DOWN).is_not_blank() - footnote

        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote

        dimensions = [
            HDimConst('Measure Type', 'Placements'),
            HDimConst('Unit', 'Count'),
            HDim(year, 'Period', CLOSEST, UP),
            HDim(quarter, 'Quarter', DIRECTLY, LEFT),
            HDim(description, 'Accommodation Type', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        tidied_accomodation.append(table)

    elif tab.name == '3_3':
        print(tab.name)
        
        cell = tab.excel_ref('A2')
        description = cell.fill(RIGHT).is_not_blank()
        footnote = description.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        total = tab.excel_ref('A').filter('Total')
        year = cell.fill(DOWN).is_not_blank() - footnote - total

        observations = description.fill(DOWN).is_not_blank() - footnote

        dimensions = [
            HDimConst('Measure Type', 'Children'),
            HDimConst('Unit', 'Count'),
            HDim(year, 'Period', CLOSEST, ABOVE),
            HDim(description, 'Accommodation Type', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        table['Period'] = table['Period'].str.replace('\.0', '')
        table['Period'] = table['Period'].str.replace(r'\(.*\).*', '')
        table['Quarter'] = table['Period'].map(lambda x: x[:3])
        table['Period'] = table['Period'].map(lambda x: x[-4:])

        tidied_accomodation.append(table)

    elif tab.name == '3_4':
        print(tab.name)
        
        cell = tab.excel_ref('A2')
        year = cell.fill(RIGHT).is_not_blank()
        footnote = year.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        age = cell.fill(DOWN).is_not_blank() - footnote

        observations = year.fill(DOWN).is_not_blank() - footnote

        dimensions = [
            HDimConst('Measure Type', 'Children'),
            HDimConst('Unit', 'Count'),
            HDim(age, 'Age Group', DIRECTLY, LEFT),
            HDim(year, 'Period', DIRECTLY, ABOVE)
        ]

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()
        table['Period'] = table['Period'].str.replace('\.0', '')
        table['Period'] = table['Period'].str.replace(r'\(.*\).*', '')
        table['Quarter'] = table['Period'].map(lambda x: x[:3])
        table['Period'] = table['Period'].map(lambda x: x[-4:])

        tidied_accomodation.append(table)

    elif tab.name == '3_5':
        print(tab.name)
        
        cell = tab.excel_ref('A2')

        length_of_stay = tab.excel_ref('C2').expand(RIGHT).is_not_blank()
        footnote = length_of_stay.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        accommodation = tab.excel_ref('B3').expand(DOWN) - footnote

        total = tab.excel_ref('A').filter('Total')

        remove_quarter = cell.fill(DOWN).regex('[^0-9]+') - total - footnote
        quarter_values = [x.value for x in remove_quarter]
        remove_year = cell.fill(DOWN).regex('[0-9]+') - footnote
        year_values = [x.value for x in remove_year]
        newYear = tab.filter("empty")

        def filterFunc(iterable):
            if left(str(iterable.value), 2) == '20':
                return True
            else:
                return False

        year = accommodation.fill(LEFT).filter(filterFunc)
        quarter = accommodation.fill(LEFT).is_not_blank() - year - tab.filter('Total')

        observations = length_of_stay.fill(DOWN).is_not_blank() - tab.excel_ref("A27").expand(RIGHT).expand(DOWN)

        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDim(length_of_stay, 'Length of Stay', DIRECTLY, ABOVE),
            HDim(year, 'Period',  WITHIN(above = 2, below = 3), LEFT),
            HDim(quarter, 'Quarter', WITHIN(above = 1, below = 4), LEFT),
            HDim(accommodation, 'Accommodation Type', DIRECTLY, LEFT)
        ]

        dimensions[3].engine.starting_offset = 3
        dimensions[3].engine.ending_offset = 2

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " Preview.html")
        table = tidy_sheet.topandas()

        tidied_accomodation.append(table)

        year = accommodation.fill(LEFT).filter(filterFunc) | tab.excel_ref("A49")
        quarter = accommodation.fill(LEFT).is_not_blank() - year - tab.filter('Total') | tab.excel_ref("A50")

        year_override = {}
        quarter_override = {}
        for y in year:
            if xypath.contrib.excel.excel_location(y) in ['A49', 'A50']:
                year_override[y.value] = '2022.0'
                quarter_override[y.value] = 'Feb'

        observations = length_of_stay.fill(DOWN).is_not_blank() - tab.excel_ref("A26").expand(RIGHT).expand(UP) - footnote

        dimensions = [
            HDimConst('Measure Type', 'Households'),
            HDimConst('Unit', 'Count'),
            HDim(length_of_stay, 'Length of Stay', DIRECTLY, ABOVE),
            HDim(year, 'Period',  WITHIN(above = 2, below = 5), LEFT, cellvalueoverride=year_override),
            HDim(quarter, 'Quarter', WITHIN(above = 1, below = 6), LEFT, cellvalueoverride=quarter_override),
            HDim(accommodation, 'Accommodation Type', DIRECTLY, LEFT)
        ]

        dimensions[3].engine.starting_offset = 5
        dimensions[3].engine.ending_offset = 2

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname=tab.name + " 2 Preview.html")
        table = tidy_sheet.topandas()
        
        tidied_accomodation.append(table)


# In[756]:


df = pd.concat(tidied_accomodation).fillna('')

df['Period'] = df['Period'].str.replace('\.0', '')
df['Period'] = df['Period'].str.replace(r'\(.*\).*', '')
df['Period'] = df['Period'].str.rstrip()
df['Quarter'] = df['Quarter'].str.replace(r'\(.*\).*', '')
df['Quarter'] = df['Quarter'].str.rstrip('123 ')

df = df.replace({'Quarter':
                     {'Apr-Sep': 'g-H1',
                      'Oct-Mar': 'g-H2',
                      'Apr-Jun': 'g-Q1',
                      'Apr-Jun ': 'g-Q1',
                      'Jan-Jun': 'c-H1',
                      'Jul-Dec': 'c-H2',
                      'Jul-Dec³': 'c-H2',
                      'Jan': 'c-H1',
                      'Jul': 'c-H2',
                      'Aug': 'c-H2',
                      'Feb': 'c-H1'
                      }})

df['Period'] = df['Period'] + ':' + df['Quarter']
df['Period'] = df['Period'].apply(period_format)
df.drop(['Quarter'], axis=1, inplace=True)

df.rename(columns={'OBS': 'Value', 'DATAMARKER': 'Marker'}, inplace=True)
df = df.replace({'Marker': {'*': 'Suppressed',
                            '-' : 'None'}})

df[["Measure Type", "Unit"]] = df[["Unit", "Measure Type"]]

df = df.replace({'Length of Stay' : {'1 to <2 Years' : '1-2 Years',
                                     '2 to <3 Years' : '2-3 Years',
                                     '3 to <4 years' : '3-4 Years',
                                     '4 to <5 Years' : '4-5 Years',
                                     '5 Years +' : '5 Plus Years',
                                     '6 Months to < 12 Months' : '6-12 Months',
                                     '< 6 Months' : 'Less than 6 Months'}})

COLUMNS_TO_PATHIFY = ['Measure Type', 'Unit', 'Marker']

for col in df.columns.values.tolist():
	if col not in COLUMNS_TO_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

df['Age Group'] = df.apply(lambda x: mid(x['Household Composition'], 13, 5) if 'yrs' in x['Household Composition'] and 'fe' not in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df.apply(lambda x: mid(x['Household Composition'], 15, 5) if 'yrs' in x['Household Composition'] and 'fe' in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df.apply(lambda x: 'total' if 'total' in x['Household Composition'] and 'male' in x['Household Composition'] else x['Age Group'], axis = 1)
df['Age Group'] = df['Age Group'].replace('', 'All')

df = df.replace({'Household Composition' : {'Families² ' : 'Families',
                                            'Pensioner households' : 'Pensioners',
                                            'Single females 16-17 yrs' : 'Single Females',
                                            'Single females 18-25 yrs' : 'Single Females',
                                            'Single females 26-59 yrs' : 'Single Females',
                                            'Single females Total'     : 'Single Females',
                                            'Single females'           : 'Single Females',
                                            'Single males 16-17 yrs' : 'Single Males',
                                            'Single males 18-25 yrs' : 'Single Males',
                                            'Single males 26-59 yrs' : 'Single Males',
                                            'Single males Total'     : 'Single Males',
                                            'Single males' : 'Single Males'},
                 'Accommodation Type' : {   'Hotel/B&B/leased property' : 'Hotel/B&B/Leased Property', 
                                            'Hotel\B&B' : 'Hotel/B&B', 
                                            'Leased property' : 'Leased Property',
                                            'NIHE hostels' : 'NIHE Hostels', 
                                            'Private single lets' : 'Private Single Lets', 
                                            'Voluntary sector hostels' : 'Voluntary Sector Hostels'}})

df = df[
    ['Period', 'Household Composition', 'Accommodation Type', 'Age Group', 'Length of Stay', 'Measure Type', 'Unit',
     'Value', 'Marker']]

scraper.dataset.license = "".join([x.strip().replace('"', '') for x in scraper.dataset.license.split(" ")])

for col in df.columns.values.tolist():
	if col in ['Marker', 'Value']:
		continue
	else:
         df[col] = df[col].replace("", "All")
         df[col] = df[col].replace("Total", "All")

df['Value'] = df.apply(lambda x: int(x['Value']) if x['Marker'] == '' else 0, axis = 1)

df['Age Group'] = df.apply(lambda x: x['Age Group'] + '-under-18' if ('All' in x['Age Group'] and 'children' in x['Unit']) or ('total' in x['Age Group'] and 'children' in x['Unit']) else x['Age Group'], axis = 1)

df['Unit'] = df.apply(lambda x: 'placements' if 'children' in x['Unit'] else x['Unit'], axis = 1)

df


# In[757]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[758]:


scraper.dataset.title = 'NIHE - Temporary Accommodation'
scraper.dataset.comment = 'The Northern Ireland Homelessness bulletin is a biannual publication which contains information on a range of areas relating to homelessness. The report is currently divided into three sections which are: Homeless Presenters; Homeless Acceptances; and Temporary Accommodation.'

df.to_csv(pathify(scraper.dataset.title) + '-observations.csv', index=False)

catalog_metadata = scraper.as_csvqb_catalog_metadata()
catalog_metadata.to_json_file(pathify(scraper.dataset.title) + '-catalog-metadata.json')

