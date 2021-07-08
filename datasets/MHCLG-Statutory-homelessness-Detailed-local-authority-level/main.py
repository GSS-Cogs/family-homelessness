# +
from gssutils import *
import json
from io import BytesIO
import pyexcel
import messytables
import pandas as pd

df = pd.DataFrame()
cubes = Cubes("info.json")

scraper = Scraper(seed="info.json")
scraper.distributions = [x for x in scraper.distributions if "Detailed local authority level tables:" in x.title]
original_tabs = scraper.distribution(latest=True, mediaType=ODS)
# -

# Conversion of ODS to XLS
with original_tabs.open() as ods_obj:
    excel_obj = BytesIO()
    book = pyexcel.get_book(file_type = 'ods', file_content = ods_obj, library = 'pyexcel-ods3')
    old_tab_names = book.sheet_names()
    
    for old_tab in old_tab_names:
        if len(old_tab) > 31:
            new_tab_names = book.sheet_names()
            find_index = new_tab_names.index(old_tab)
            book.remove_sheet(book.sheet_names()[find_index])
            
    book.save_to_memory(file_type = 'xls', stream = excel_obj)
    tableset = messytables.excel.XLSTableSet(fileobj = excel_obj)
    tabs = list(xypath.loader.get_sheets(tableset, "*"))

# +
"""
Transformation for tabs - 'A1','A2P','A2R_','A3','A4P','A4R','A5P','A5R','A7', which will be held in an output called :
Households initially assessed as threatened with homelessness (owed prevention duty) or homeless (owed relief duty)
"""
data_01_title = 'MHCLG Homelessness - Households initially assessed as threatened with homelessness (owed prevention duty) or homeless (owed relief duty)'
tabs_names_to_process_01 = ['A1','A2P','A2R_','A3','A4P','A4R','A5P','A5R','A7']
tidied_sheets = []
for tab_name in tabs_names_to_process_01:
    # Raise an exception if one of our required tabs is missing.
    if tab_name not in [x.name for x in tabs]:
        raise ValueError(f'Aborting. A tab named {tab_name} required but not found')
    # Select the tab in question.
    tab = [x for x in tabs if x.name == tab_name][0]
    
    #Standard extraction across all tabs.
    tab_name = tab.name
    remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
    period = tab.excel_ref('A1')
    ons_geo_code = period.fill(DOWN).is_not_blank() - remove_notes
    observations = ons_geo_code.shift(2,0).expand(RIGHT).is_not_blank()
    
    row2 = tab.excel_ref('E2').expand(RIGHT)
    row3 = tab.excel_ref('E3').expand(RIGHT)    
    row4 = tab.excel_ref('E4').expand(RIGHT)
    row5 = tab.excel_ref('E5').expand(RIGHT)
    row6 = tab.excel_ref('E6').expand(RIGHT)

    if tab_name == 'A1':
        dimensions = [
            HDim(row3,'row3',DIRECTLY, ABOVE),
            HDim(row4,'row4',CLOSEST, LEFT),
            HDim(row5,'row5',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name) #used for post ptocessing
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['assessment_duty_type'] = df['row3'] + df['row4'] + df['row5']
        df.drop(['row3', 'row4', 'row5'], axis=1, inplace=True)
        df['assessment_duty_type'] = df['assessment_duty_type'].replace(r'\s+|\\n', ' ', regex=True)
        
         #replacement of values done as per transformation style guide
        tmp_1 = {'Total initial assessments1,2':'Total Initial Assessments', 
        'Assessed as owed a dutyTotal owed a prevention or relief duty':'Total owed a prevention of relief duty',
        'Threatened with homelessness within 56 days - Prevention duty owed':'Threatened with homelessness within 56 days',
        'Of which:due to service of valid Section 21 Notice3':'Due to service of valid Section 21 Notice', 
        'Homeless - Relief duty owed4':'Homeless',
        'Not homeless nor threatened with homelessness within 56 days - no duty owed':'Not homeless nor threatened with homelessness within 56 days',
        'Number of households in area4 (000s)':'Number of Households in area (000s)',
        'Households assessed as threatened with homelessness per (000s)':'Households assessed as threatened with homelessness per(000s)',
        'Households assessed as homeless per (000s)':'Households assessed as homeless per(000s)'}
        df['Initial Circumstance Assessment'] = df['assessment_duty_type'].replace(tmp_1)

        df.drop(['assessment_duty_type'], axis=1, inplace=True)

        #replacement of values done as per transformation style guide
        temp_2 = {'Total Initial Assessments':'N/A',
        'Total owed a prevention of relief duty':'Relief', 
        'Threatened with homelessness within 56 days':'Prevention',
        'Due to service of valid Section 21 Notice':'Prevention',
        'Homeless':'Relief',
        'Not homeless nor threatened with homelessness within 56 days':'No duty owed',
        'Number of Households in area (000s)':'All', 
        'Households assessed as threatened with homelessness per(000s)':'N/A',
        'Households assessed as homeless per(000s)':'N/A'}
        df['Duty Type'] = df['Initial Circumstance Assessment'].replace(temp_2)
        df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
        tidied_sheets.append(df)
        
    elif tab_name in ['A2P', 'A2R_']:
        row4 = tab.excel_ref('E4').expand(RIGHT).is_not_blank() - tab.excel_ref('E4').expand(RIGHT).filter(contains_string("Of which:")) | tab.excel_ref('E4') 
        dimensions = [
            HDim(row3,'row3',DIRECTLY,ABOVE),
            HDim(row4,'row4',CLOSEST,LEFT),
            HDim(row5,'row5',DIRECTLY,ABOVE),
            HDim(row6,'row6',DIRECTLY,ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['row6'] = df['row6'].replace(r'\s+|\\n', ' ', regex=True)

        g3 = "End of assured shorthold (AST) private rented tenancy, due to.. "
        i5 = "Rent arrears, due to.. "
        ab3 = 'End of social rented tenancy, due to..'
        ag3 = 'Eviction from supported housing, due to..'
        temp =  {'End of assured shorthold (AST) private rented tenancy, due to.. Rent arrears, due to.. ':'',
                'Rent arrears, due to..':'',
                'Of which:' : ''}
        
        #row 6 post processing 
        df['row6'] = g3 + i5 + df['row6'] 
        df['row6'] = df['row6'].replace(temp)
        #row 3 post processing 
        df['row3'] = df['row3'].map(lambda x: '' if ', due to..' in x else x )
        #row 4 post processing 
        df['row4'] = df['row4'].replace(r'\s+|\\n', ' ', regex=True)
        df['row4'] = df['row4'].replace(temp)
        df.loc[df["row6"] == '','row6'] = df["row4"] 
        df['row4'] = df['row4'].map(lambda x: ab3 if 'social' in x else (ag3 if 'supported' in x else x))
        #row 5 post processing 
        df['row5'] = df['row5'].replace(temp)
        df['row5'] = df['row4'] + " " + df['row5']
        #Brining values in columns together and removing what is no longer needed. 
        df['row6'] = df['row3'] + df['row6']
        del df['row3']
        del df['row4']
        del df['row5']
        
        df.rename(columns={'row6' : 'Reason for loss or threat of loss of home'}, inplace=True)
        df["Period"]= df["Period"].str.split(", ", n = 4, expand = True)[3]
        tidied_sheets.append(df)
    elif tab_name in ['A3']:
        dimensions = [
            HDim(row2,'row2',DIRECTLY,ABOVE),
            HDim(row3,'row3',DIRECTLY,ABOVE),
            HDim(row4,'row4',DIRECTLY,ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['row2'] = df['row2'].map(lambda x: '' if 'households' in x else  x)
        df['row3'] = df['row3'].map(lambda x: '' if x == 'Households with one or more support needs owed duty1,2' else  x)
        temp =  {'1.0':'Households with one support need',
                '2.0':'Households with two support needs',
                '3+' : 'Households with three or more support needs'}
        df['row4'] = df['row4'].replace(temp)
        df['Support needs of household'] = df['row2'] + df['row3'] + df['row4'] 
        del df['row2']
        del df['row3']
        del df['row4']
        df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
        tidied_sheets.append(df)
        
    elif tab_name in ['A4P', 'A4R']: 
        row3 = tab.excel_ref("E3").expand(RIGHT).is_not_blank()
        dimensions = [
            HDim(row3,'row3',CLOSEST, LEFT),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(row5,'row5',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['row3'] = df['row3'].replace(r'\s+|\\n', ' ', regex=True)
        df['row4'] = df['row4'].replace(r'\s+|\\n', ' ', regex=True)
        df['row5'] = df['row5'].replace(r'\s+|\\n', ' ', regex=True)

        temp =  {'Of which:' : ''}
        df['row4'] = df['row4'].replace(temp)
        df['Accomodation type'] = df['row3'] + ' ' + df['row5']
        df['Accomodation type'] = df['row4'] + ' ' + df['Accomodation type']
        df['Accomodation type'] = df['Accomodation type'].str.lstrip()
        del df['row3']
        del df['row4']
        del df['row5']
        df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
        tidied_sheets.append(df)
    elif tab_name in ['A5P' , 'A5R']:
        row3 = tab.excel_ref("E3").expand(RIGHT).is_not_blank()
        remove_cells = ['F6', 'I6', 'K6', 'M6', 'P6', 'R6', 'T6', 'W6', 'Y6', 'AA6', 'AC6', 'AE6']
        for cell in remove_cells :
            observations = observations - tab.excel_ref(cell).expand(DOWN)
        dimensions = [
            HDim(row3,'row3',CLOSEST, LEFT),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['row3'] = df['row3'].str.lstrip('Single ')
        temp =  {'Male':'Single male ',
                'Female':'Single female ',
                'Other / gender not known' : 'Single other / gender not known '}
        df['row4'] = df['row4'].replace(temp)
        df['Household composition'] = df['row4'] + df['row3']
        del df['row3']
        del df['row4']
        df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
        tidied_sheets.append(df)
    elif tab_name in ['A7'] :
        row3 = tab.excel_ref("E3").expand(RIGHT).is_not_blank()
        observations = tab.excel_ref('E6').expand(RIGHT).expand(DOWN).is_not_blank() - tab.excel_ref('E7').expand(RIGHT) - tab.excel_ref('W6').expand(DOWN).expand(RIGHT)
        dimensions = [
            HDim(row3,'row3',CLOSEST, LEFT),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(row5,'row5',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['row5'] = df['row5'].replace(r'\s+|\\n', ' ', regex=True)
        df['Referral Public Body'] = df['row4'] + ' ' + df['row5']
        df['Referral Public Body'] = df['Referral Public Body'].str.lstrip()
        df['Referral Public Body'] = df['row3'] + ' ' +  df['Referral Public Body']
        temp =  {'Households referred by a public body under the Duty to Refer2 Total households referred under the Duty to Refer2 ':'Total households referred under the Duty to Refer2'}
        df['Referral Public Body'] = df['Referral Public Body'].replace(temp)
        df['Referral Public Body'] = df['Referral Public Body'].str.lstrip()
        del df['row3']
        del df['row4']
        del df['row5']
        df["Period"]= df["Period"].str.split(", ", n = 3, expand = True)[2]
        tidied_sheets.append(df)
    else :
        continue
df = pd.concat(tidied_sheets, sort=True)
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

#Initial Circumstance Assessment
df['Initial Circumstance Assessment'] = df['Initial Circumstance Assessment'].fillna('all')
#Reason for loss or threat of loss of homes
df['Reason for loss or threat of loss of home'] = df['Reason for loss or threat of loss of home'].fillna('all')
#Duty Type 
df.loc[((df.Tab == 'A2P') | (df.Tab == 'A4P') | (df.Tab == 'A5P')), 'Duty Type'] = 'Prevention'
df.loc[((df.Tab == 'A2R_')| (df.Tab == 'A4R') | (df.Tab == 'A5R')), 'Duty Type'] = 'Relief'
df.loc[((df.Tab == 'A3') | (df.Tab == 'A7')), 'Duty Type'] = 'all'
#Support needs of household
df['Support needs of household'] = df['Support needs of household'].fillna('all')
#Accommodation Type 
df['Accomodation type'] = df['Accomodation type'].fillna('all')
#Household Composition 
df['Household composition'] = df['Household composition'].fillna('all')
#Referral Public Body
df['Referral Public Body'] = df['Referral Public Body'].fillna('n/a')
#Eligibility for Homelessness Status
df['Eligibility for Homelessness Status'] = 'all'
#Measure Type  
df['Measure Type'] = 'Households'
#Unit 
df['Unit'] = 'count'
del df['Tab']

#Marker column 
df = df.replace({'Marker' : {
    '..': 'incomplete or no data received from the local authority',
    '-' : 'Support need breakdowns have been suppressed for local authorities with fewer than 5 households with support needs.'}})
df_01 = df
del df
cubes.add_cube(scraper, df_01, data_01_title)

# +
"""
Transformation for tabs - , which will be held in an output called :
MHCLG Homelessness - Age, Ethnicity, Employment Status and Sexual Identification of main applicant owed a prevention or relief duty by Local Authority.
"""
data_02_title = 'MHCLG Homelessness - Age, Ethnicity, Employment Status and Sexual Identification of main applicant owed a prevention or relief duty by Local Authority.'
tabs_names_to_process_02 = ['A6_', 'A8', 'A10', 'A12']
tidied_sheets_2 = []
for tab_name in tabs_names_to_process_02:
    # Raise an exception if one of our required tabs is missing.
    if tab_name not in [x.name for x in tabs]:
        raise ValueError(f'Aborting. A tab named {tab_name} required but not found')
    # Select the tab in question.
    tab = [x for x in tabs if x.name == tab_name][0]
    
    #Standard extraction across all tabs.
    tab_name = tab.name
    period = tab.excel_ref('A1')
    remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
    ons_geo_code = period.fill(DOWN).is_not_blank() - remove_notes
    remove_percentage = tab.filter(contains_string("%")).expand(DOWN)
    remove_rest_of_england_row = tab.filter(contains_string("Rest of England")).expand(RIGHT)
    
    if tab_name in ['A6_'] :
        age = tab.excel_ref('A3').expand(RIGHT).is_not_blank()
        observations = age.fill(DOWN).is_not_blank() - remove_percentage - remove_rest_of_england_row - remove_notes
        dimensions = [
            HDim(age,'Age',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        tidied_sheets_2.append(df)
    elif tab_name in ['A8'] :
        ethnicity = tab.excel_ref('E3').expand(RIGHT).is_not_blank()
        ethnic_group = tab.excel_ref('E4').expand(RIGHT).is_not_blank() | tab.excel_ref('E3') | tab.excel_ref('BG3')
        observations = ethnic_group.fill(DOWN).is_not_blank() - remove_percentage - remove_rest_of_england_row - remove_notes
        dimensions = [
            HDim(ethnicity,'Ethnicity',CLOSEST, LEFT),
            HDim(ethnic_group,'Ethnic Group',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        tidied_sheets_2.append(df)
    elif tab_name in ['A10'] :
        employ_status = tab.excel_ref('E3').expand(RIGHT).is_not_blank()
        observations = employ_status.fill(DOWN).is_not_blank() - remove_rest_of_england_row - remove_notes
        dimensions = [
            HDim(employ_status,'Employment Status',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        tidied_sheets_2.append(df)
    elif tab_name in ['A12'] :
        sexual_ident = tab.excel_ref('B2').expand(RIGHT).is_not_blank()
        observations = sexual_ident.fill(DOWN).is_not_blank() - remove_rest_of_england_row - remove_notes
        dimensions = [
            HDim(sexual_ident,'Sexual Identification',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        tidied_sheets_2.append(df)
    else :
        continue
df = pd.concat(tidied_sheets_2, sort=True)
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
#age
df['Age'] = df['Age'].fillna('total')
#Ethnicity
df['Ethnicity'] = df['Ethnicity'].fillna('total')
#Ethnic Group
df['Ethnic Group'] = df['Ethnic Group'].fillna('total')
#Employment Status
df['Employment Status'] = df['Employment Status'].fillna('total')
#Sexual Identification
df['Sexual Identification'] = df['Sexual Identification'].fillna('total')
#Duty Type
df['Duty Type'] = 'all'
#Measure Type  
df['Measure Type'] = 'Applicant'
#Unit 
df['Unit'] = 'count'
del df['Tab']
#Marker column 

df = df.replace({'Marker' : {
    '..': 'incomplete or no data received from the local authority',
    '-' : 'Sexual Identity breakdowns have been suppressed for local authorities with fewer than 5 households assessed as owed a duty.'}})

df_02 = df
del df
cubes.add_cube(scraper, df_02, data_02_title)

# +
"""
Transformation for tabs - , which will be held in an output called :
MHCLG Homelessness - Households whose Prevention or Relief duty ended by reason and accommodation type
"""
data_03_title = 'MHCLG Homelessness - Households whose Prevention or Relief duty ended by reason and accommodation type'
tabs_names_to_process_03 = ['P1', 'P2', 'R1', 'R2']
tidied_sheets_3 = []

#Period, ONS Geography, Reason Duty ended, Duty Type, Accommodation Type, Measure Type, Unit

for tab_name in tabs_names_to_process_03:
    # Raise an exception if one of our required tabs is missing.
    if tab_name not in [x.name for x in tabs]:
        raise ValueError(f'Aborting. A tab named {tab_name} required but not found')
    # Select the tab in question.
    tab = [x for x in tabs if x.name == tab_name][0]
    
    #Standard extraction across all tabs.
    remove_rest_of_england_row = tab.filter(contains_string("Rest of England")).expand(RIGHT)
    tab_name = tab.name
    period = tab.excel_ref('A1')
    remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
    ons_geo_code = period.fill(DOWN).is_not_blank() - remove_notes
    
    row3 = tab.excel_ref('C3').expand(RIGHT) 
    row4 = tab.excel_ref('C4').expand(RIGHT) 
    row5 = tab.excel_ref('C5').expand(RIGHT)
    
    temp =  {'Total PRS':'Total ',
             'Total SRS' :'Total ',
            'Of which:' : ''}
    
    if tab_name in ['P1'] :
        row3 = tab.excel_ref('C3').expand(RIGHT).is_not_blank()
        observations = row4.fill(DOWN).is_not_blank() - remove_rest_of_england_row
        dimensions = [
            HDim(row3,'row3',CLOSEST, LEFT),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['Reason Duty ended'] = df['row3'] + ' ' + df['row4']
        df['Reason Duty ended'] = df['Reason Duty ended'].str.rstrip()
        del df['row3']
        del df['row4']
        df['Duty Type'] = 'Prevention'
        tidied_sheets_3.append(df)
    if tab_name in ['P2'] :
        observations = row5.fill(DOWN).is_not_blank() - remove_notes - remove_rest_of_england_row
        dimensions = [
            HDim(row3,'row3',DIRECTLY, ABOVE),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(row5,'row5',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas() 
        df['row4'] = df['row4'].replace(temp)
        df['row5'] = df['row5'].replace(r'\s+|\\n', ' ', regex=True)
        df['row3'] = df['row3'].replace(r'\s+|\\n', ' ', regex=True)
        df['Accommodation Type'] = df['row4'] + df['row3'] + ' ' + df['row5']
        del df['row3']
        del df['row4']
        del df['row5']
        df['Accommodation Type'] = df['Accommodation Type'].str.strip()
        df['Duty Type'] = 'Prevention'
        tidied_sheets_3.append(df)
    elif tab_name in  ['R1'] :
        observations = row3.fill(DOWN).is_not_blank() - remove_rest_of_england_row
        dimensions = [
            HDim(row3,'Reason Duty ended',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas() 
        df['Duty Type'] = 'Relief'
        tidied_sheets_3.append(df)
    elif tab_name in ['R2']:
        observations = row5.fill(DOWN).is_not_blank() - remove_notes - remove_rest_of_england_row
        dimensions = [
            HDim(row3,'row3',DIRECTLY, ABOVE),
            HDim(row5,'row5',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas() 
        df['row5'] = df['row5'].replace(temp)
        df['row3'] = df['row3'].replace(r'\s+|\\n', ' ', regex=True)
        df['Accommodation Type'] = df['row5'] + df['row3']
        del df['row3']
        del df['row5']
        tidied_sheets_3.append(df)
    else: 
        continue
        
df = pd.concat(tidied_sheets_3, sort=True)
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True) 
df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
#Reason Duty ended
df['Reason Duty ended'] = df['Reason Duty ended'].fillna('all')
#Accommodation Type
df['Accommodation Type'] = df['Accommodation Type'].fillna('all')
#Measure Type  
df['Measure Type'] = 'Households'
#Unit 
df['Unit'] = 'count'

del df['Tab']
#Marker column .. incomplete or no data received from the local authority
df = df.replace({'Marker' : {
    '..': 'incomplete or no data received from the local authority'}})
df_03 = df
del df
cubes.add_cube(scraper, df_03, data_03_title)

# +
"""
Transformation for tabs - , which will be held in an output called :
MHCLG Homelessness - Households assessed, following relief duty end, as unintentionally homeless and priority need (owed main duty)

"""
data_04_title = 'MHCLG Homelessness - Households assessed, following relief duty end, as unintentionally homeless and priority need (owed main duty)'
tabs_names_to_process_04 = ['MD1', 'MD2', 'MD3']
tidied_sheets_04 = []

#Period, ONS Geography, Decision on Duty owed, Reason for duty end, Priority Need, Measure, Unit

for tab_name in tabs_names_to_process_04:
    # Raise an exception if one of our required tabs is missing.
    if tab_name not in [x.name for x in tabs]:
        raise ValueError(f'Aborting. A tab named {tab_name} required but not found')
    # Select the tab in question.
    tab = [x for x in tabs if x.name == tab_name][0]
    
    #Standard extraction across all tabs.
    tab_name = tab.name
    period = tab.excel_ref('A1')
    remove_rest_of_england_row = tab.filter(contains_string("Rest of England")).expand(RIGHT)
    remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
    ons_geo_code = period.fill(DOWN).is_not_blank() - remove_notes
    row3 = tab.excel_ref('E3').expand(RIGHT)
    row4 = tab.excel_ref('E4').expand(RIGHT)
    
    if tab_name in ['MD1'] :
        observations = row3.fill(DOWN).is_not_blank() - remove_notes - remove_rest_of_england_row
        dimensions = [
            HDim(row3,'Decision after Relief duty ended',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas() 
        df['Unit'] = 'count'
        tidied_sheets_04.append(df)
    elif tab_name in ['MD2'] :
        observations = row4.fill(DOWN).is_not_blank() - remove_notes - remove_rest_of_england_row
        dimensions = [
            HDim(row3,'row3',DIRECTLY, ABOVE),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas() 
        df['Reason for duty end'] = df['row4'] + '' + df['row3']
        del df['row3']
        del df['row4']
        df['Unit'] = 'count'
        tidied_sheets_04.append(df)
    elif tab_name in ['MD3'] : 
        observations = row4.fill(DOWN).is_not_blank() - tab.excel_ref('A335').expand(RIGHT).expand(DOWN) - remove_rest_of_england_row 
        remove_cells = ['F6', 'H6', 'J6', 'L6', 'O6', 'Q6', 'S6', 'U6', 'W6', 'Y6', 'AA6', 'AD6']
        for cell in remove_cells :
            observations = observations - tab.excel_ref(cell).expand(DOWN)
        dimensions = [
            HDim(row3,'row3',DIRECTLY, ABOVE),
            HDim(row4,'row4',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        
        df = tidy_sheet.topandas() 
        df['row3'] = df['row3'].replace(r'\s+|\\n', ' ', regex=True)
        df['row4'] = df['row4'].replace(r'\s+|\\n', ' ', regex=True)
        temp =  {'Total vulnerable households':'Total'}
        df['row4'] = df['row4'].replace(temp)
        df['Priority Need'] = df['row3'] + ' ' + df['row4']
        del df['row3']
        del df['row4']
        df['Unit'] = 'count'
        tidied_sheets_04.append(df)
        
        #perccentages TO DO 
        observation_percentages = row4.fill(DOWN).is_not_blank() - observations - remove_rest_of_england_row -  tab.excel_ref('A335').expand(RIGHT).expand(DOWN)
    else :
        continue 
    

df = pd.concat(tidied_sheets_04, sort=True)
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True) 
df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]  

#Reason for duty end
df['Reason for duty end'] = df['Reason for duty end'].fillna('all')
#Decision after Relief duty ended
df['Decision after Relief duty ended'] = df['Decision after Relief duty ended'].fillna('all')
#Priority Need
df['Priority Need'] = df['Priority Need'].fillna('all')
#Measure Type  
df['Measure Type'] = 'Households'

del df['Tab']
#Marker column .. incomplete or no data received from the local authority
df = df.replace({'Marker' : {
    '..': 'incomplete or no data received from the local authority',
    '-' : 'Priority need breakdowns suppressed for local authorities with fewer than 5 households owed a main duty, to prevent disclosure'}})
df_04 = df
del df
cubes.add_cube(scraper, df_04, data_04_title)

# +
"""
Transformation for tabs - , which will be held in an output called :
MHCLG Homelessness - Households in temporary accommodation by household composition and accommodation type
"""
data_05_title = 'MHCLG Homelessness - Households in temporary accommodation by household composition and accommodation type'
tabs_names_to_process_05 = ['TA1' , 'TA2']
tidied_sheets_05 = []
#Period, ONS Geography, Accommodation Type, Household Composition , Measure Type, Unit

for tab_name in tabs_names_to_process_05:
    # Raise an exception if one of our required tabs is missing.
    if tab_name not in [x.name for x in tabs]:
        raise ValueError(f'Aborting. A tab named {tab_name} required but not found')
    # Select the tab in question.
    tab = [x for x in tabs if x.name == tab_name][0]

    #Standard extraction across all tabs.
    tab_name = tab.name
    period = tab.excel_ref('A1')
    remove_rest_of_england_row = tab.filter(contains_string("Rest of England")).expand(RIGHT)
    remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
    ons_geo_code = period.fill(DOWN).is_not_blank() - remove_notes
    row2 = tab.excel_ref('E2').expand(RIGHT)
    row3 = tab.excel_ref('E3').expand(RIGHT)
    row5 = tab.excel_ref('E5').expand(RIGHT)
    row6 = tab.excel_ref('E6').expand(RIGHT)
    
    if tab_name in ['TA1'] :
        observations = row3.fill(DOWN).is_not_blank() - remove_rest_of_england_row - remove_notes
        dimensions = [
            HDim(row2,'row2',DIRECTLY, ABOVE),
            HDim(row3,'row3',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas() 
        f1=(df['row3'] =='')
        df.loc[f1,'row3'] = df['row2']
        
        f2=(df['row2'] == df['row3'])
        df.loc[f2,'row2'] = ''
        
        temp =  {'':'N/A'}
        df['row3'] = df['row3'].replace(temp)
        df['row2'] = df['row2'].replace(temp)
        df.rename(columns={'row2' : 'Accommodation Type', 'row3' : 'Household Composition'}, inplace=True)
        tidied_sheets_05.append(df)
        
    elif tab_name in ['TA2'] :
        observations = row6.fill(DOWN).is_not_blank() - remove_rest_of_england_row - remove_notes 
        remove_cells = ['F8', 'H8', 'K8', 'M8', 'O8', 'R8', 'T8', 'V8', 'Y8']
        for cell in remove_cells :
            observations = observations - tab.excel_ref(cell).expand(DOWN)
        dimensions = [
            HDim(row5,'row5',DIRECTLY, ABOVE),
            HDim(row6,'row6',DIRECTLY, ABOVE),
            HDim(ons_geo_code,'ONS Geography code',DIRECTLY, LEFT),
            HDim(period,'Period',CLOSEST, LEFT),
            HDimConst("Tab", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        df = tidy_sheet.topandas()
        df['Accommodation Type'] = 'all'
        df['Household Composition'] = df['row5'] + ' ' + df['row6']
        del df['row5']
        del df['row6']
        df['Household Composition'] = df['Household Composition'].str.strip()
        tidied_sheets_05.append(df)
    else : 
        continue
        
df = pd.concat(tidied_sheets_05, sort=True)
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True) 
df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]  
df['Unit'] = 'count'
df['Measure Type'] = 'Households'

del df['Tab']
#Marker column .. incomplete or no data received from the local authority
df = df.replace({'Marker' : {
    '..': 'Missing or incomplete data provided by local authority',
    '-' : 'Household type breakdowns for local authorities with fewer than 5 households in TA have been suppressed.'}})
df_05 = df
del df
cubes.add_cube(scraper, df_05, data_05_title)

# +
#outputting just the csv's for now for benefit of DM. 

destinationFolder = Path('out')
destinationFolder.mkdir(exist_ok=True, parents=True)
df_01.drop_duplicates().to_csv(destinationFolder / (data_01_title + '.csv'), index = False)
df_02.drop_duplicates().to_csv(destinationFolder / (data_02_title + '.csv'), index = False)
df_03.drop_duplicates().to_csv(destinationFolder / (data_03_title + '.csv'), index = False)
df_04.drop_duplicates().to_csv(destinationFolder / (data_04_title + '.csv'), index = False)
df_05.drop_duplicates().to_csv(destinationFolder / (data_05_title + '.csv'), index = False)
