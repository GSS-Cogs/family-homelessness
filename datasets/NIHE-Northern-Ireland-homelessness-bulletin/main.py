# -*- coding: utf-8 -*-
# # NIHE Northern Ireland homelessness bulletin 

# +
from gssutils import * 
from databaker.framework import *
import json
import pandas as pd
import numpy as np


import pyexcel
import messytables
from io import BytesIO
# -

cubes = Cubes('info.json')

pd.set_option('display.float_format', lambda x: '%.0f' % x)

# +

info = json.load(open('info.json')) 
dataURL = info['dataURL']
dataURL
# -

scraper = Scraper(seed='info.json') 
scraper 

distribution = scraper.distribution(latest=True)
distribution

from pandas import ExcelWriter
xls = pd.ExcelFile(distribution.downloadURL, engine="odf")
with ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        # pd.read_excel(xls, sheet).to_excel(writer,sheet, index_col=None)
        pd.read_excel(xls, sheet).to_excel(writer,sheet, index=False)
    writer.save()
tabs = loadxlstabs("data.xls")

# +
tab_names = [tab.name for tab in tabs]
pres_start = tab_names.index('1_1')   # presentation start index
accept_start = tab_names.index('2_1') # acceptance start index
temp_start = tab_names.index('3_1') # tempprary accommodation start index
temp_end = tab_names.index('3_5') + 1  # tempprary accommodation end index

(pres_start, accept_start, temp_start, temp_end)
# -

presentations_tabs = tabs[pres_start : accept_start]
acceptance_tabs = tabs[accept_start : temp_start]
accommodation_tabs = tabs[temp_start : temp_end]

trace = TransformTrace()

# +
for tab in presentations_tabs:
    title = 'NIHE Homelessness Presentations'
    scraper.dataset.title = title
    columns = ['Period', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation breakdown', 'Loss of rented Accommodation reason', 'Release from facilities breakdown', 'Household Composition', 'ONS Geography code', 'Assessment Decision', 'Legislative test Outcome', 'Repeat Homeless Presentations', 'Measure Type', 'Unit', 'Value', 'Marker']

    if tab.name in ['1_1', '1_1A', '1_1B', '1_1C', '1_1D', '1_5']:
        
        trace.start(title, tab, columns, distribution.downloadURL)
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
        # yearAlt = tab.excel_ref('A4').expand(DOWN).regex('[0-9]') - footnote

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
                    HDimConst('Measure Type','Household'),
                    HDimConst('Unit','Count'),  
                    HDimConst('ONS Geography code', "N07000001"),
                    HDim(year, 'Period', CLOSEST, UP), #CLOSEST,ABOVE
                    HDim(quarter, 'Quarter', DIRECTLY,LEFT),
                    HDim(reason, reason_title, DIRECTLY, ABOVE)         
        ]  
       
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table = table.drop(columns='Quarter')
        # table.drop(['Quarter'], axis =1, inplace=True)
        trace.store('combined_dataframe_presentation', table)
    

    elif tab.name == '1_2':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
           
        age = tab.excel_ref('B3').expand(RIGHT) - tab.excel_ref('O3').expand(RIGHT)
        household = age.shift(UP).is_not_blank()
        
        footnote = household.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        total = tab.excel_ref('A').filter('Total')
        quarter = tab.excel_ref('A4').expand(DOWN).regex('[^0-9]+') - total - footnote
        year = cell.fill(DOWN).is_not_blank().is_not_blank() - total - quarter - footnote
        yearAlt = tab.excel_ref('A4').expand(DOWN).regex('[0-9]') - footnote

        observations = tab.excel_ref('B5').expand(DOWN).expand(RIGHT).is_not_blank() - footnote
        observations1 = year.fill(RIGHT).is_not_blank()
        dimensions = [
                    HDimConst('Measure Type','Household'),
                    HDimConst('Unit','Count'),
                    HDimConst('ONS Geography code', "N07000001"),
                    HDim(year, 'Period', CLOSEST, ABOVE),
                    HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                    HDim(household,'Household Composition', CLOSEST, LEFT),
                    HDim(age, 'Age Group', DIRECTLY, ABOVE)               
        ]  
        
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()

        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        
        table['Household Composition'] = table['Household Composition'].astype(str) + ' ' + table['Age Group'].astype(str).replace(r'\(.*\)', ' ')
        table.drop(['Age Group'],axis=1, inplace=True)
        # table.drop(columns=['Quarter', 'Age Group'], inplace=True)
        trace.store('combined_dataframe_presentation', table)

    elif tab.name == '1_3':
        print(tab.name) 
        trace.start(title, tab, columns, distribution.downloadURL)
        
        presenters = tab.excel_ref('B4').expand(RIGHT).is_not_blank() 
        quarter = presenters.shift(UP).is_not_blank()
        year = quarter.shift(UP).is_not_blank()
        footnote = presenters.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        location = tab.excel_ref('A5').expand(DOWN).is_not_blank() - footnote
       
        observations = presenters.fill(DOWN).is_not_blank() - footnote
        dimensions = [
                    HDimConst('Measure Type','Household'),
                    HDimConst('Unit','Count'),    
                    HDim(year, 'Period', CLOSEST, LEFT), 
                    HDim(quarter, 'Quarter', CLOSEST, LEFT), 
                    HDim(presenters,'Homeless Presenters', DIRECTLY, ABOVE), 
                    HDim(location, 'ONS Geography code', DIRECTLY, LEFT)                                    
        ]  
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table = table.drop(columns='Quarter')
       
        table.loc[(table['Homeless Presenters'] == 'Total presenter'), 'Unit'] = 'Count'
        table.loc[(table['Homeless Presenters'] == 'Presenters per 1,000 population'), 'Unit'] = 'Per 1,000 population'
        table.drop(['Homeless Presenters'], axis=1, inplace=True)
        
        trace.store('combined_dataframe_presentation', table)

 
    elif tab.name == '1_4':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        
        year =  tab.excel_ref('B2').expand(RIGHT).is_not_blank()
        quarter = tab.excel_ref('B3').expand(RIGHT).is_not_blank()

        footnote = quarter.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        assessment = tab.excel_ref('A4').expand(DOWN).is_not_blank() - footnote
        observations = quarter.fill(DOWN).is_not_blank() - footnote
        
        dimensions = [
                    HDimConst('Measure Type','Household'),
                    HDimConst('Unit','Count'),
                    HDimConst('ONS Geography code', "N07000001"),
                    HDim(year, 'Period', DIRECTLY, ABOVE), 
                    HDim(quarter, 'Quarter', DIRECTLY, ABOVE),
                    HDim(assessment,'Assessment Decision', DIRECTLY, LEFT),
                ]  
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table.drop(['Quarter'], axis=1, inplace=True) 
        
        trace.store('combined_dataframe_presentation', table) 


    elif tab.name == '1_6':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        footnote = tab.excel_ref('B').filter('Source: NIHE').expand(LEFT).expand(DOWN)
        year =  tab.excel_ref('A3').expand(DOWN).is_not_blank() - footnote
        presenters = tab.excel_ref('B2')
        observations = presenters.fill(DOWN) - footnote
          
        dimensions = [
                    HDimConst('Measure Type','Household'),
                    HDimConst('Unit','Count'),
                    HDimConst('ONS Geography code', "N07000001"),
                    HDim(year, 'Period', DIRECTLY, LEFT), 
                    HDim(presenters,'Repeat Homeless Presentations', DIRECTLY, ABOVE)
                ]  
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        
        trace.store('combined_dataframe_presentation', table) 

df = trace.combine_and_trace(title, 'combined_dataframe_presentation').fillna('')

df['Period'] = df['Period'].str.replace('\.0', '')
df['Period'] = df['Period'].str.replace(r'\(.*\).*', '') 
df['Quarter'] = df['Quarter'].str.replace(r'\(.*\).*', '')
df['Quarter'] = df['Quarter'].str.rstrip('123 ')

df = df.replace({'Quarter':
{'Apr-Sep' : 'g-H1', 
'Oct-Mar' : 'g-H2',
'Apr-Jun': 'g-Q1' ,
'Apr-Jun ': 'g-Q1',
'Jan-Jun': 'c-H1',
'Jul-Dec' : 'c-H2', 
'Jul-Dec³' : 'c-H2',
'' : 'g-year'
}})

# next_table['Period'] = next_table['Period'].map(
#     lambda x: {
#         'Apr-Sep' : 'government-half/2018-2019/H1', 
#         'Oct-Mar' : 'government-half/2018-2019/H2',
#         'Apr-Jun': 'government-quarter/2018-2019/Q1' ,
#         'Jul-Dec': 'government-quarter/2018-2019/Q2',
#         'Jul-Dec³' : 'government-quarter/2018-2019/Q2', 
#        'Apr-Jun (Financial year Q1)²' : 'government-quarter/2018-2019/Q1' ,
#        'Apr-Jun (Financial year 2019 Q1)¹' : 'government-quarter/2018-2019/Q1', 

df = df.replace({'ONS Geography code': 
{'Antrim and Newtownabbey' : 'N09000001', 
'Ards and North Down' : 'N09000011',
'Armagh City, Banbridge and Craigavon': 'N09000002', 
'Belfast' : 'N09000003',
'Causeway Coast and Glens': 'N09000004', 
'Derry City and Strabane' : 'N09000005',
'Fermanagh and Omagh': 'N09000006', 
'Lisburn and Castlereagh': 'N09000007',
'Mid and East Antrim': 'N09000008', 
'Mid Ulster': 'N06000010', 
'Newry, Mourne and Down' : 'N09000010',
'Northern Ireland' : 'N07000001'
}})

df.rename(columns={'OBS':'Value', 'DATAMARKER':'Marker'}, inplace=True)
df = df.replace({'Value': {'' : '0'}})
df['Value'] = df['Value'].astype(float).round().astype(int)
df = df.replace({'Marker': {'*' : 'Statistical disclosure'}})

df = df.replace({
'Reason for Homelessness': {'' : 'All'}, 
'Accommodation not Reasonable breakdown' : {'' : 'All'},
'Intimidation breakdown': {'' : 'All'}, 
'Loss of rented Accommodation reason' : {'' : 'All'},
'Release from facilities breakdown' : {'' : 'All'},
'Household Composition': {'' : 'All'}, 
'Assessment Decision' : {'' : 'All'},
'Legislative test Outcome': {'' : 'All'}, 
'Repeat Homeless Presentations': {'' : 'All'},
})

df = df[['Period', 'Quarter', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation breakdown', 'Loss of rented Accommodation reason', 'Release from facilities breakdown', 'Household Composition', 'ONS Geography code', 'Assessment Decision', 'Legislative test Outcome', 'Repeat Homeless Presentations', 'Measure Type', 'Unit', 'Value','Marker']]

cubes.add_cube(scraper, df, scraper.dataset.title)
# -

df

# +
for tab in acceptance_tabs:
    title = 'NIHE Homelessness Acceptances'
    scraper.dataset.title = title
    columns = ['Period', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation breakdown', 'Release from facilities breakdown', 'Household Composition', 'ONS Geography code', 'Priority need Category', 'Housing Assessment Outcome', 'Age Bracket', 'Assessment Decision', 'Measure Type', 'Unit', 'Value', 'Marker']

    if tab.name == '2_1':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
        reason = cell.fill(RIGHT) - tab.excel_ref('R2').expand(RIGHT) 
        
        footnote = cell.fill(RIGHT).fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        observations = tab.excel_ref('B6').expand(RIGHT).expand(DOWN).is_not_blank() - footnote
        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote
        
        # reason_override = {}
        # for x in reason:
        #     if xypath.contrib.excel.excel_location(x) in 'P2':
        #         reason_override[x.value] = 'Status of Household Duty Discharged'
        #     elif xypath.contrib.excel.excel_location(x) == 'Q2':
        #         reason_override[x.value] = 'Status of Household Live full duty applicants'
    
        reason_title = 'Reason for Homelessness'

        dimensions = [
                        HDimConst('Measure Type','Households'),
                        HDimConst('Unit','Count'),  
                        HDimConst('Assessment Decision', 'Accepted'), 
                        HDimConst('ONS Geography code', "N07000001"),
                        HDim(year, 'Period', CLOSEST, UP), 
                        HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                        HDim(reason, reason_title, DIRECTLY, ABOVE)
                        # HDim(reason, reason_title, DIRECTLY, ABOVE, cellvalueoverride = reason_override)        
            ] 

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table = table.drop(columns='Quarter')
        trace.store('combined_dataframe_acceptance', table)
        
       
    if tab.name in ['2_1A', '2_1B', '2_1C', '2_5', '2_6']:
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
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
                    HDimConst('Measure Type','Households'),
                    HDimConst('Unit','Count'),  
                    HDimConst('Assessment Decision', 'Accepted'), 
                    HDimConst('ONS Geography code', "N07000001"),
                    HDim(year, 'Period', CLOSEST, UP), 
                    HDim(quarter, 'Quarter', DIRECTLY,LEFT), 
                    HDim(reason, reason_title, DIRECTLY, ABOVE)   
        ]              
    
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table = table.drop(columns='Quarter')
    
        trace.store('combined_dataframe_acceptance', table)
     
    elif tab.name == '2_2':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
        
        age = tab.excel_ref('B3').expand(RIGHT) - tab.excel_ref('O3').expand(RIGHT)
        household = age.shift(UP).is_not_blank()

        footnote = household.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        total = tab.excel_ref('A').filter('Total')
        quarter = tab.excel_ref('A4').expand(DOWN).regex('[^0-9]+') - total - footnote
        year = cell.fill(DOWN).is_not_blank().is_not_blank() - total - quarter - footnote

        observations = tab.excel_ref('B5').expand(DOWN).expand(RIGHT).is_not_blank() - footnote
        observations_alt = year.fill(RIGHT).is_not_blank()

        # household_override = {}
        # for x in household:
        #     if xypath.contrib.excel.excel_location(x) in ['C2', 'D2', 'E2']:
        #         household_override[x.value] = 'Single males'
        #     elif xypath.contrib.excel.excel_location(x) in ['G2', 'H2', 'I2']:
        #         household_override[x.value] = 'Single females'

        dimensions = [
                    HDimConst('Measure Type','Household'),
                    HDimConst('Unit','Count'),
                    HDimConst('Assessment Decision', 'Accepted'),
                    HDimConst('ONS Geography code', "N07000001"),
                    HDim(year, 'Period', CLOSEST, ABOVE), 
                    HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                    HDim(household,'Household Composition', CLOSEST, LEFT), 
                    HDim(age, 'Age', DIRECTLY, ABOVE)                                
        ]  
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        table['Household Composition'] = table['Household Composition'].astype(str) + ' ' + table['Age'].astype(str).replace(r'\(.*\).*', '')
        table.drop(columns='Age', inplace=True)
        trace.store('combined_dataframe_acceptance', table)
        
    elif tab.name == '2_3':
        print(tab.name) 
        trace.start(title, tab, columns, distribution.downloadURL)
          
        year = tab.excel_ref('A2').fill(RIGHT).is_not_blank()
        quarter = year.shift(DOWN)
        footnote = year.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        location = tab.excel_ref('A2').fill(DOWN).is_not_blank() - footnote 
       
        observations = quarter.fill(DOWN).is_not_blank() - footnote
        dimensions = [
                    HDimConst('Measure Type','Households'),
                    HDimConst('Unit','Count'), 
                    HDimConst('Assessment Decision', 'Accepted'),  
                    HDim(year, 'Period', DIRECTLY, ABOVE), 
                    HDim(quarter, 'Quarter', DIRECTLY, ABOVE),
                    HDim(location, 'ONS Geography code', DIRECTLY, LEFT) 
        ]  
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table.drop(['Quarter'], axis=1, inplace=True)
        trace.store('combined_dataframe_acceptance', table) 

    elif tab.name == '2_4':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        
        year =  tab.excel_ref('B2').expand(RIGHT).is_not_blank()
        
        footnote = year.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        location = tab.excel_ref('A2').fill(DOWN).is_not_blank() - footnote
        observations = year.fill(DOWN).is_not_blank() - footnote
        
        dimensions = [
                    HDimConst('Measure Type','Households'),
                    HDimConst('Unit','Count'),
                    HDimConst('Assessment Decision', 'Discharged'),
                    HDim(year, 'Period', DIRECTLY, ABOVE), 
                    HDim(location,'ONS Geography code', DIRECTLY, LEFT)
        ]  
        
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        trace.store('combined_dataframe_acceptance', table) 

    elif tab.name == '2_7':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        trace.start(title, tab, columns, distribution.downloadURL)
        quarter =  tab.excel_ref('B3').expand(RIGHT).is_not_blank()
        year = quarter.shift(UP)
        footnote = quarter.fill(DOWN).filter('Source:NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        age_category = tab.excel_ref('A3').fill(DOWN).is_not_blank() - footnote
        
        observations = quarter.fill(DOWN).is_not_blank() - footnote
        
        dimensions = [
                    HDimConst('Measure Type','Households'),
                    HDimConst('Unit','Count'),
                    HDimConst('Assessment Decision', 'Accepted'),
                    HDim(age_category, 'Age Bracket', DIRECTLY, LEFT),
                    HDim(year, 'Period', DIRECTLY, ABOVE), 
                    HDim(quarter,'Quarter', DIRECTLY,ABOVE),
        ]  
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table.drop(['Quarter'], axis=1, inplace=True)
        trace.store('combined_dataframe_acceptance', table) 

df = trace.combine_and_trace(title, 'combined_dataframe_acceptance').fillna('')

df['Period'] = df['Period'].str.replace('\.0', '')
df['Period'] = df['Period'].str.replace(r'\(.*\).*', '') 
df['Quarter'] = df['Quarter'].str.replace(r'\(.*\).*', '')
df['Quarter'] = df['Quarter'].str.rstrip('123 ')

df = df.replace({'Quarter':
{'Apr-Sep' : 'g-H1', 
'Oct-Mar' : 'g-H2',
'Apr-Jun': 'g-Q1' ,
'Apr-Jun ': 'g-Q1',
'Jan-Jun': 'c-H1',
'Jul-Dec' : 'c-H2', 
'Jul-Dec³' : 'c-H2',
'' : 'g-year'
}})

df = df.replace({'ONS Geography code': 
{'Antrim and Newtownabbey' : 'N09000001', 
'Ards and North Down' : 'N09000011',
'Armagh City, Banbridge and Craigavon': 'N09000002', 
'Belfast' : 'N09000003',
'Causeway Coast and Glens': 'N09000004', 
'Derry City and Strabane' : 'N09000005',
'Fermanagh and Omagh': 'N09000006', 
'Lisburn and Castlereagh': 'N09000007',
'Mid and East Antrim': 'N09000008', 
'Mid Ulster': 'N06000010', 
'Newry, Mourne and Down' : 'N09000010',
'Northern Ireland' : 'N07000001'
}})
    
df.rename(columns={'OBS':'Value', 'DATAMARKER':'Marker'}, inplace=True)
df = df.replace({'Value': {'' : '0'}})
df['Value'] = df['Value'].astype(float).round().astype(int)
df = df.replace({'Marker': {'*' : 'Statistical disclosure'}})

df = df.replace({
'Reason for Homelessness': {'' : 'All'}, 
'Accommodation not Reasonable breakdown' : {'' : 'All'},
'Intimidation breakdown': {'' : 'All'}, 
'Release from facilities breakdown' : {'' : 'All'},
'Household Composition': {'' : 'All'}, 
'Priority need Category' : {'' : 'All'},
'Housing Assessment Outcome': {'' : 'All'}, 
'Age Bracket': {'' : 'All'},
'Assessment Decision': {'' : 'All'},
})

df = df[['Period', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation breakdown', 'Release from facilities breakdown', 'Household Composition', 'ONS Geography code', 'Priority need Category', 'Housing Assessment Outcome', 'Age Bracket', 'Assessment Decision', 'Measure Type', 'Unit', 'Value', 'Marker']]

cubes.add_cube(scraper, df, scraper.dataset.title)


# -

def with_year_overrides(year_dimension):
    for cell in year_dimension.hbagset:
        # If a dimension cell is not year
        if cell.value not in year_values: #cell.regex('[0-9]+')   
            print('cell value:', cell.value, ' ', 'y cell value:', cell.y)
            
            # Is there a value two cells down? if so use that value
            cell_checked = [cell2 for cell2 in year_dimension.hbagset if cell2.y == cell.y+2 and cell2.value in year_values]
            if len(cell_checked) > 0:
                year_dimension.AddCellValueOverride(cell, cell_checked[0].value)
        
            # Is there a value one cell down? if so use that value
            cell_checked = [cell2 for cell2 in year_dimension.hbagset if cell2.y == cell.y+1 and cell2.value in year_values]
            if len(cell_checked) > 0:
                year_dimension.AddCellValueOverride(cell, cell_checked[0].value)

            # Is there a value one cell up? if so use that value
            cell_checked = [cell2 for cell2 in year_dimension.hbagset if cell2.y == cell.y-1 and cell2.value in year_values]
            if len(cell_checked) > 0:
                year_dimension.AddCellValueOverride(cell, cell_checked[0].value)

            # Is there a value two cells up? if so use that value
            cell_checked = [cell2 for cell2 in year_dimension.hbagset if cell2.y == cell.y-2 and cell2.value in year_values]
            if len(cell_checked) > 0:
                year_dimension.AddCellValueOverride(cell, cell_checked[0].value)
            
            # Is there a value three cells up? if so use that value
            cell_checked = [cell2 for cell2 in year_dimension.hbagset if cell2.y == cell.y-3 and cell2.value in year_values]
            if len(cell_checked) > 0:
                year_dimension.AddCellValueOverride(cell, cell_checked[0].value)
            
    return year_dimension


def with_month_overrides(month_dimension):
   
    for cell in month_dimension.hbagset:
        # If a dimension cell is blank
        if cell.value not in ['Jan', 'Jul']: #cell.regex('[0-9]+')   
            print(cell.value, ':cell value', '', cell.y, ':y cell value')
            
            # Is there a value one cell down? if so use that value
            cell_checked = [cell2 for cell2 in month_dimension.hbagset if cell2.y == cell.y+1 and cell2.value in ['Jan', 'Jul']]
            if len(cell_checked) > 0:
                month_dimension.AddCellValueOverride(cell, cell_checked[0].value)
        
            # Is there a value one cell up? if so use that value
            cell_checked = [cell2 for cell2 in month_dimension.hbagset if cell2.y == cell.y-1 and cell2.value in ['Jan', 'Jul']]
            if len(cell_checked) > 0:
                month_dimension.AddCellValueOverride(cell, cell_checked[0].value)

            # Is there a value two cells up? if so use that value
            cell_checked = [cell2 for cell2 in month_dimension.hbagset if cell2.y == cell.y-2 and cell2.value in ['Jan', 'Jul']]
            if len(cell_checked) > 0:
                month_dimension.AddCellValueOverride(cell, cell_checked[0].value)
            
            # Is there a value three cells up? if so use that value
            cell_checked = [cell2 for cell2 in month_dimension.hbagset if cell2.y == cell.y-3 and cell2.value in ['Jan', 'Jul']]
            if len(cell_checked) > 0:
                month_dimension.AddCellValueOverride(cell, cell_checked[0].value)

             # Is there a value four cells up? if so use that value
            cell_checked = [cell2 for cell2 in month_dimension.hbagset if cell2.y == cell.y-4 and cell2.value in ['Jan', 'Jul']]
            if len(cell_checked) > 0:
                month_dimension.AddCellValueOverride(cell, cell_checked[0].value)

    return month_dimension


# +
for tab in accommodation_tabs:
    title = 'NIHE - Temporary Accommodation'
    scraper.dataset.title = title
    columns = ['Period', 'Household Composition', 'Accommodation Type', 'Age Bracket', 'Length of Stay', 'Measure Type', 'Unit', 'Value', 'Marker']
    if tab.name == '3_1':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
        age = tab.excel_ref('B3').expand(RIGHT) - tab.excel_ref('O3').expand(RIGHT)
        household = age.shift(UP).is_not_blank()
        
        footnote = household.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN).is_not_blank()
        observations = age.fill(DOWN).is_not_blank() - footnote

        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote
        
        dimensions = [
                    HDimConst('Measure Type','Placements'),
                    HDimConst('Unit','Count'),
                    HDim(year, 'Period', CLOSEST, ABOVE), 
                    HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                    HDim(household,'Household Composition', CLOSEST, LEFT), 
                    HDim(age, 'Age', DIRECTLY, ABOVE)                                
        ] 

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '')
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        table['Household Composition'] = table['Household Composition'].astype(str) + ' ' + table['Age'].astype(str)
        table.drop(columns='Age', inplace=True)
        trace.store('combined_dataframe_accommodation', table) 

    elif tab.name == '3_2':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
        description = cell.fill(RIGHT).is_not_blank()
        description_title = 'Accommodation Type'
        footnote = description.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        observations = description.fill(DOWN).is_not_blank() - footnote 

        total = tab.excel_ref('A').filter('Total')
        quarter = cell.fill(DOWN).regex('[^0-9]+').is_not_blank() - total - footnote
        year = cell.fill(DOWN).is_not_blank() - total - quarter - footnote

        dimensions = [
                HDimConst('Measure Type','Placements'),
                HDimConst('Unit','Count'),  
                HDim(year, 'Period', CLOSEST, UP), 
                HDim(quarter, 'Quarter', DIRECTLY,LEFT),
                HDim(description, 'Accommodation Type', DIRECTLY, ABOVE)         
        ]  

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        # table['Period'] = table['Period'].str.replace('\.0', '') 
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
        # table.drop(['Quarter'], axis =1, inplace=True)
        trace.store('combined_dataframe_accommodation', table)   

    elif tab.name == '3_3':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
        description = cell.fill(RIGHT).is_not_blank()
        footnote = description.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        total = tab.excel_ref('A').filter('Total')
        year = cell.fill(DOWN).is_not_blank() - total - footnote

        observations = description.fill(DOWN).is_not_blank() - footnote 

        dimensions = [
                HDimConst('Measure Type','Children'),
                HDimConst('Unit','Count'),  
                HDim(year, 'Period', DIRECTLY,LEFT), 
                HDim(description, 'Accommodation Type', DIRECTLY, ABOVE)         
        ]  

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        table['Period'] = table['Period'].str.replace('\.0', '')
        table['Period'] = table['Period'].str.replace(r'\(.*\).*', '')  
        table['Quarter'] = table['Period'][:3]
        table['Period'] = table['Period'][-4:]
        
       
        trace.store('combined_dataframe_accommodation', table) 
        
    elif tab.name == '3_4':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')
        year = cell.fill(RIGHT).is_not_blank()
        footnote = year.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        age = cell.fill(DOWN).is_not_blank() - footnote
        
        observations = year.fill(DOWN).is_not_blank() - footnote
        
        dimensions = [
                HDimConst('Measure Type','Children'),
                HDimConst('Unit','Count'),  
                HDim(age, 'Age Bracket', DIRECTLY, LEFT), 
                HDim(year, 'Period', DIRECTLY, ABOVE)         
        ]  

        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        table['Period'] = table['Period'].str.replace('\.0', '') 
        table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') 
        table['Quarter'] = table['Period'][:3]
        table['Period'] = table['Period'][-4:]
        
        trace.store('combined_dataframe_accommodation', table) 
        
    elif tab.name == '3_5':
        print(tab.name)
        trace.start(title, tab, columns, distribution.downloadURL)
        cell = tab.excel_ref('A2')

        length_of_stay = tab.excel_ref('C2').expand(RIGHT).is_not_blank()
        footnote = length_of_stay.fill(DOWN).filter('Source: NIHE').expand(LEFT).expand(DOWN)
        accommodation = tab.excel_ref('B4').expand(DOWN) - footnote
        
        total = tab.excel_ref('A').filter('Total')
        
        remove_quarter = cell.fill(DOWN).regex('[^0-9]+') - total - footnote
        quarter_values = [x.value for x in remove_quarter]
        remove_year = cell.fill(DOWN).regex('[0-9]+') - footnote
        year_values = [x.value for x in remove_year]

        # quarter = accommodation.fill(LEFT).regex('[^0-9]+').is_not_blank()- total 
        # year = accommodation.fill(LEFT).is_not_blank() - remove_quarter -total 
        # year = accommodation.fill(LEFT)  - remove_quarter - total
        # quarter = accommodation.fill(LEFT) - remove_year - total

        year = accommodation.fill(LEFT)
        quarter = accommodation.fill(LEFT)
        
        # year_override = {}
        # for y_cell in year:
        #     if y_cell not in remove_year:
        #         year_override[y_cell.value] = ''

        # quarter_override = {}
        # for q_cell in quarter:
        #     if q_cell not in remove_quarter:
        #         quarter_override[q_cell.value] = ''


        observations = length_of_stay.fill(DOWN).is_not_blank() - footnote

        dimensions = [
                HDimConst('Measure Type','Households'),
                HDimConst('Unit','Count'),  
                HDim(length_of_stay, 'Length of Stay', DIRECTLY, ABOVE),
                HDim(year, 'Period', DIRECTLY, LEFT), 
                HDim(quarter, 'Quarter', DIRECTLY, LEFT),
                HDim(accommodation, 'Accommodation Type', DIRECTLY, LEFT)   
        ]  
        
        dimensions[3] = with_year_overrides(dimensions[3])
        dimensions[4] = with_month_overrides(dimensions[4])
        
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        table = tidy_sheet.topandas()
        print(table['Period'].unique())

        # table['Period'] = table['Period'].str.replace('\.0', '') 
        # table['Period'] = table['Period'].str.replace(r'\(.*\).*', '') + '/' + table['Quarter'].str.replace(r'\(.*\)+', '')
       
        trace.store('combined_dataframe_accommodation', table) 

df = trace.combine_and_trace(title, 'combined_dataframe_accommodation').fillna('')

df['Period'] = df['Period'].str.replace('\.0', '')
# df['Period'] = df['Period'].str.replace(r'\(.*\).*', '') 
# df['Quarter'] = df['Quarter'].str.replace(r'\(.*\).*', '')
# df['Quarter'] = df['Quarter'].str.rstrip('123 ')

df = df.replace({'Quarter':
{'Apr-Sep' : 'g-H1', 
'Oct-Mar' : 'g-H2',
'Apr-Jun': 'g-Q1' ,
'Apr-Jun ': 'g-Q1',
'Jan-Jun': 'c-H1',
'Jul-Dec' : 'c-H2', 
'Jul-Dec³' : 'c-H2',
'' : 'g-year'
}})

df.rename(columns={'OBS':'Value', 'DATAMARKER':'Marker'}, inplace=True)
df = df.replace({'Value': {'' : '0'}})
df['Value'] = df['Value'].astype(float).round().astype(int)
df = df.replace({'Marker': {'*' : 'Statistical disclosure'}})

df = df.replace({
'Accommodation Type': {'' : 'All'}, 
'Household Composition' : {'' : 'All'},
'Age Bracket': {'' : 'All'}, 
'Length of Stay' : {'' : 'All'}
})

df = df[['Period', 'Quarter', 'Household Composition', 'Accommodation Type', 'Age Bracket', 'Length of Stay', 'Measure Type', 'Unit', 'Value', 'Marker']]

cubes.add_cube(scraper, df, scraper.dataset.title)
# -

list(dimensions[3].hbagset)

cubes.output_all()


