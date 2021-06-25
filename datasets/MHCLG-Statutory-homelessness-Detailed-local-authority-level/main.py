# +
# # MHCLG Statutory homelessness Detailed local authority-level 
# -

from gssutils import * 
import json 
import pandas as pd
import numpy as np 
from io import BytesIO
import pyexcel
import messytables

#  get all the distributions
trace = TransformTrace()
df = pd.DataFrame()
cubes = Cubes("info.json")
info = json.load(open('info.json')) 
metadata = Scraper(seed = "info.json") 
required = [x.title for x in metadata.distributions if "October to December 2020" in x.title]
assert len(required) == 1, 'Aborting more than 1 October to December 2020" source file found'


original_tabs = metadata.distribution(title = required[0])
original_tabs


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

datasetTitle = original_tabs.title
# datasetTitle
# print(type(tabs))
for tab in tabs:
    print(tab.name)

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A1']: #only transforming tab A1 for now
        trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
        remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
        temp_assessment_duty_type_1 = tab.filter("Total initial assessments1,2").assert_one().expand(RIGHT)
        temp_assessment_duty_type_2 = temp_assessment_duty_type_1.shift(DOWN).expand(RIGHT)            
        temp_assessment_duty_type_3 = temp_assessment_duty_type_2.shift(DOWN).expand(RIGHT)
        observations = temp_assessment_duty_type_3.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(RIGHT)
        ons_geo = unwanted.shift(LEFT)-unwanted
        period = temp_assessment_duty_type_1.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet_name = tab.name

        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(temp_assessment_duty_type_1,'temp_assessment_duty_type_1',DIRECTLY, ABOVE),
            HDim(temp_assessment_duty_type_2,'temp_assessment_duty_type_2',DIRECTLY, ABOVE),
            HDim(temp_assessment_duty_type_3,'temp_assessment_duty_type_3',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        #convert to pandas df
        df = tidy_sheet.topandas()
        #run individual post processing 
        df["Period"]= df["Period"].str.split(", ", n = 1, expand = True)[1]
        #Bring the 3 temp columns together - we will then decide the Duty Type Owed values based on them
        df['assessment_duty_type'] = df['temp_assessment_duty_type_1'] + df['temp_assessment_duty_type_2'] + df['temp_assessment_duty_type_3']

        #drop the other temp ones as no longer needed 
        df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)

        #Check the outputs of the temp column
        df['assessment_duty_type'].unique()

        # Below is how I matched the values up - I just took this info from the spec for tab A1

        # Initial Assessments                                                   Duty Type Owned
        # - Total Initial Assessments                                           - N/A
        # - Total owed a prevention of relief duty                              - Relief
        # - Threatened with homelessness within 56 days                         - Prevention
        # - Due to service of valid Section 21 Notice                           - Prevention
        # - Homeless                                                            - Relief
        # - Not homeless nor threatened with homelessness within 56 days        - No duty owed
        # - Number of Households in area (000s)                                 - All
        # - Households assessed as threatened with homelessness per(000s)       - N/A
        # - Households assessed as homeless per(000s)                           - N/A

         #replacement of values done as per transformation style guide
        tmp_1 = {'Total initial assessments1,2':'Total Initial Assessments', 
        'Assessed as owed a dutyTotal owed a prevention or relief duty':'Total owed a prevention of relief duty',
        'Threatened with homelessness within 56 days - \nPrevention duty owed':'Threatened with homelessness within 56 days',
        'Of which:due to service of valid Section 21 Notice3':'Due to service of valid Section 21 Notice', 
        'Homeless - \nRelief duty owed4':'Homeless',
        'Not homeless nor threatened with homelessness within 56 days - no duty owed':'Not homeless nor threatened with homelessness within 56 days',
        'Number of households\n in area4 (000s)':'Number of Households in area (000s)',
        'Households assessed as threatened with homelessness\nper (000s)':'Households assessed as threatened with homelessness per(000s)',
        'Households assessed as homeless\nper (000s)':'Households assessed as homeless per(000s)'}
        
        df['Initial Circumstance Assessment'] = df['assessment_duty_type'].replace(tmp_1)

        #drop other temp column 
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

        #Checking values are what I expect 
        df['Duty Type'].unique()

        #Checking values are what I expect 
        df['Initial Circumstance Assessment'].unique()
#         df["Period"].unique()
        print(df['Period'].unique())
        #add to combined df
        trace.store("combined_dataframe", df)
        
# Note all the other dimension's will need to be added but they seem to be contants for this tab anyway 
# so could always add them in later and use the sheet name as reference or something along those lines. 
# Hope this helps. 
# -
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A2P', 'A2R_']:
        remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
        reasons_row3 = tab.excel_ref('E3').expand(RIGHT)    
        reasons_row4 = tab.excel_ref('E4').expand(RIGHT).is_not_blank() - tab.excel_ref('E4').expand(RIGHT).filter(contains_string("Of which:")) | tab.excel_ref('E4') 
        reasons_row5 = tab.excel_ref('E5').expand(RIGHT)
        reasons_row6 = tab.excel_ref('E6').expand(RIGHT)
        observations = tab.excel_ref('E7').expand(RIGHT).expand(DOWN).is_not_blank()   
        tab_name = tab.name 
        dimensions = [
            HDim(reasons_row3,'reasons_row3',DIRECTLY,ABOVE),
            HDim(reasons_row4,'reasons_row4',CLOSEST,LEFT),
            HDim(reasons_row5,'reasons_row5',DIRECTLY,ABOVE),
            HDim(reasons_row6,'reasons_row6',DIRECTLY,ABOVE),
            HDimConst("Duty Type", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        df['reasons_row6'] = df['reasons_row6'].replace(r'\s+|\\n', ' ', regex=True)
        g3 = "End of assured shorthold (AST) private rented tenancy, due to.. "
        i5 = "Rent arrears, due to.. "
        ab3 = 'End of social rented tenancy, due to..'
        ag3 = 'Eviction from supported housing, due to..'
        temp =  {'End of assured shorthold (AST) private rented tenancy, due to.. Rent arrears, due to.. ':'',
                'Rent arrears, due to..':'',
                'Of which:' : ''}
        #row 6 post processing 
        df['reasons_row6'] = g3 + i5 + df['reasons_row6'] 
        df['reasons_row6'] = df['reasons_row6'].replace(temp)
        #row 3 post processing 
        df['reasons_row3'] = df['reasons_row3'].map(lambda x: '' if ', due to..' in x else x )
        #row 4 post processing 
        df['reasons_row4'] = df['reasons_row4'].replace(r'\s+|\\n', ' ', regex=True)
        df['reasons_row4'] = df['reasons_row4'].replace(temp)
        df.loc[df["reasons_row6"] == '','reasons_row6'] = df["reasons_row4"] 
        df['reasons_row4'] = df['reasons_row4'].map(lambda x: ab3 if 'social' in x else (ag3 if 'supported' in x else x))
        #row 5 post processing 
        df['reasons_row5'] = df['reasons_row5'].replace(temp)
        df['reasons_row5'] = df['reasons_row4'] + " " + df['reasons_row5']
        #Brining values in columns together and removing what is no longer needed. 
        df['reasons_row6'] = df['reasons_row3'] + df['reasons_row6']
        del df['reasons_row3']
        del df['reasons_row4']
        del df['reasons_row5']
        df.rename(columns={'reasons_row6' : 'Reason for loss or threat of loss of home'}, inplace=True)
        df['Duty Type'] = df['Duty Type'].map(lambda x: 'Prevention' if x == 'A2P' else 'Relief' )
        #additional columns 
        df['Initial Assessment'] = 'All'
        df['Support needs of household'] = 'All'
        df['Accommodation Type'] = 'All'
        df['Household Composition'] = 'All'
        df['Referral Public Body'] = 'N/A'
        df['Eligibility for Homelessness Status'] = 'All'
        df['Measure Type'] = 'Households'
        df['Unit'] = 'Count'
        trace.store("combined_dataframe_A2P_redo", df) #Rename "combined_dataframe_A2P_redo" to match the rest when needed 
#outputting for now just to check     
df = trace.combine_and_trace(datasetTitle, "combined_dataframe_A2P_redo")
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df.head()

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A3']: #only transforming tab A3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
        reason_of_households_with_support_needs = tab.filter("Households with no support needs owed duty1,2").assert_one().assert_one().expand(RIGHT)
        total_no_of_households = reason_of_households_with_support_needs.shift(ABOVE)
        total_households_with_support_needs = reason_of_households_with_support_needs.shift(DOWN)
        observations = total_households_with_support_needs.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(RIGHT)
        ons_geo = unwanted.shift(LEFT)-unwanted
        period = reason_of_households_with_support_needs.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(total_no_of_households,'total_no_of_households',CLOSEST, LEFT),
            HDim(reason_of_households_with_support_needs,'reason_of_households_with_support_needs',DIRECTLY, ABOVE),
            HDim(total_households_with_support_needs,'total_households_with_support_needs', DIRECTLY, ABOVE),
# #             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        df['Period']= df['Period'].str.split(", ", n = 1, expand = True)[1]
        #Assignment
        temp =  {'1.0':'Households with one support need', 
                 '2.0':'Households with two support needs',
                 '3+':'Households with three or more support needs'}
        #Replacement
        df['Support needs of household'] = df['total_households_with_support_needs'].replace(temp)

        #sheet:A3 - combine three series into one series in the dataframe
        # df['support_needs_of_household'] = df['total_no_of_households'] + df['reason_of_households_with_support_needs'] + df['total_households_with_support_needs']

        # sheet:A3
        df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_with_support_needs'], axis=1, inplace=True)
        print(df['Period'].unique())
        print(df['Support needs of household'].unique())
        trace.store("combined_dataframe", df)


# The Requirement
# H  - Total households with support needs
# I4 - Households with one support need
# J4 - Households with two support needs
# K4 - Households with three or more support needs

#Ignore the below comments. Requirement is satisfied.

# 'Number of householdsHouseholds with three or more support needs',is a odd value. Needs investigation.
#'Households with one or more support needs owed duty1,2Total households with support needs',is a odd value. Needs investigation.
# -



# +
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
# df.head()
# -

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A4P', 'A4R']: 
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        row_1 = tab.excel_ref("E3").expand(RIGHT).is_not_blank()
        row_2 = tab.excel_ref("E4").expand(RIGHT)
        row_3 = tab.excel_ref("E5").expand(RIGHT)
        geo = tab.excel_ref('A5').expand(DOWN).is_not_blank()
        tab_name = tab.name 
        observations = tab.excel_ref('E6').expand(RIGHT).expand(DOWN).is_not_blank() - remove_notes
        dimensions = [
            HDim(row_1,'row_1',CLOSEST, LEFT),
            HDim(row_2,'row_2',DIRECTLY, ABOVE),
            HDim(row_3,'row_3',DIRECTLY, ABOVE),
            HDim(geo,'ONS Geography code',DIRECTLY, LEFT),
            HDimConst("Duty Type", tab_name)
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        df['row_1'] = df['row_1'].replace(r'\s+|\\n', ' ', regex=True)
        df['row_2'] = df['row_2'].replace(r'\s+|\\n', ' ', regex=True)
        df['row_3'] = df['row_3'].replace(r'\s+|\\n', ' ', regex=True)
        temp =  {'Of which:' : ''}
        df['row_2'] = df['row_2'].replace(temp)
        df['Accomodation type'] = df['row_1'] + ' ' + df['row_3']
        df['Accomodation type'] = df['row_2'] + ' ' + df['Accomodation type']
        df['Accomodation type'] = df['Accomodation type'].str.lstrip()
        df['Duty Type'] = df['Duty Type'].map(lambda x: 'Prevention' if x == 'A4P' else 'Relief' )
        del df['row_1']
        del df['row_2']
        del df['row_3']
        #additional columns 
        df['Initial Assessment'] = 'All'
        df['Support needs of household'] = 'All'
        df['Accommodation Type'] = 'All'
        df['Household Composition'] = 'All'
        df['Referral Public Body'] = 'N/A'
        df['Eligibility for Homelessness Status'] = 'All'
        df['Measure Type'] = 'Households'
        df['Unit'] = 'Count'
        trace.store("combined_dataframe_A4P", df) #Rename "combined_dataframe_A4P" to match the rest when needed 
#Outputting for now just to check 
df = trace.combine_and_trace(datasetTitle, "combined_dataframe_A4P")
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A5P', 'A5R']: #only transforming tab A5P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_duty_owed_by_household = tab.filter("Single parent with dependent children").shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT).is_blank()
        single_parent_adult_male_female  = prevention_duty_owed_by_household.shift(DOWN)
        total_col = prevention_duty_owed_by_household|single_parent_adult_male_female
        
        
        total_prevention_duty_owed = tab.filter("Single parent with dependent children").shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT)
        total_single = total_prevention_duty_owed.shift(DOWN)

        total_column = total_prevention_duty_owed|total_single
        total_observations = total_column.shift(DOWN).fill(DOWN).is_not_blank()-remove_notes 
         
        household_2 = prevention_duty_owed_by_household.shift(DOWN).is_not_blank()
        household_2_obs = household_2.fill(DOWN).is_not_blank()
        unwanted_observations = total_col.shift(DOWN).fill(DOWN).is_not_blank()-household_2_obs
        
        observations = total_observations - unwanted_observations
        
        sheet = tab.name
        ons_geo = tab.filter("E92000001").expand(DOWN).is_not_blank()

        period = prevention_duty_owed_by_household.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        savepreviewhtml(total_single, fname= tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(total_prevention_duty_owed,'total_prevention_duty_owed',DIRECTLY, ABOVE),
            HDim(total_single,'total_single',DIRECTLY, ABOVE),
            HDimConst('sheet', sheet),  #Might be handy to have for post processing when other tabs are running also
             
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['Household composition'] = df['total_prevention_duty_owed']+df['total_single']
        
        # a5p&a5r.prevention &relief to be changed
        if tab.name == 'A5P':
            df['Duty Type'] = df['sheet'].apply(lambda x: "a5p.Prevention" if x == 'A5P' else x)

        if tab.name == 'A5R':
            df['Duty Type'] = df['sheet'].apply(lambda x: "a5r.Relief" if x == 'A5R' else x)
        
        
        df['Household composition'] = df['total_prevention_duty_owed']+df['total_single']
        df.drop(['total_prevention_duty_owed', 'total_single'], axis=1, inplace=True)
        df.drop(['sheet'], axis=1, inplace=True)
        print(df['Household composition'].value_counts())
        print(df['Duty Type'].value_counts())
        
# Female and other/gender not known as ouputs as two dimensions instead of four dimensions
# -

df.head()

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A7']: #only transforming tab A7 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        remove_notes_1 = tab.filter(contains_string('% assessed as owed a duty')).expand(RIGHT)
        remove_notes_2 = tab.filter(contains_string('Grand Total'))
        total_remove = remove_notes|remove_notes_1|remove_notes_2
        referral_public_body = tab.filter("Total households assessed as a result of a referral1,5").assert_one().expand(RIGHT)
        referred_household = referral_public_body.shift(DOWN)
        breakdown_of_referred_household = referred_household.shift(DOWN)
        observations = breakdown_of_referred_household.fill(DOWN).expand(RIGHT).is_not_blank()-total_remove
        unwanted = observations.shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(RIGHT)
        ons_geo = unwanted.shift(LEFT)-unwanted # "-" suppressed in geography code to be processed in stage-2 transformation
        period = referral_public_body.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank() #period can be extracted from this cell 
        sheet = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(referral_public_body,'Referral Public Body',DIRECTLY, ABOVE),
            HDim(referred_household,'referred_household',DIRECTLY, ABOVE),
            HDim(breakdown_of_referred_household, 'breakdown_of_referred_household', DIRECTLY, ABOVE),
            HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
#         df['Referral Public Body'] = df['assessed_household']
        df.drop(['referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
        
        print(df['Referral Public Body'].unique())
        trace.store("combined_dataframe", df)
# -
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df.head()





# +
#Age of main applicants assessed as owed a prevention or relief duty by local authority England
"""part of new table structure"""
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A6_']: #only transforming tab A6_ for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        total_unwanted = tab.filter("Total owed a prevention or relief duty1").assert_one().shift(RIGHT).expand(DOWN)|remove_notes
        age_of_main_applicants = tab.filter("Total owed a prevention or relief duty1").assert_one().expand(RIGHT).is_not_blank().filter(lambda x: type(x.value) != '%' not in x.value) 
        unwanted_ons_geo = tab.filter("Total owed a prevention or relief duty1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-remove_notes
        unwanted = unwanted_ons_geo.filter("-").expand(RIGHT)|remove_notes
        ons_geo = unwanted_ons_geo-unwanted
        period = tab.filter("Total owed a prevention or relief duty1").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        observations = age_of_main_applicants.waffle(ons_geo)-total_unwanted
        sheet = tab.name
#         savepreviewhtml(total_unwanted, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(age_of_main_applicants,'age_of_main_applicants',DIRECTLY, ABOVE),
            HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        print(df['age_of_main_applicants'].unique())
        
        trace.store("combined_dataframe", df)

# (E3:W3) Age (including total and not known)

# To be done
# Measure Type = Applicant
# Unit = count

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A8']: #only transforming tab A8 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted = tab.excel_ref("A6").expand(DOWN).filter("-").expand(RIGHT)|remove_notes
        ethnicgroup_blank = tab.filter("Total owed a prevention or relief duty1").assert_one().expand(RIGHT).is_blank()
        breakdown_of_ethnicgroup_blank = ethnicgroup_blank.shift(DOWN).is_blank()
        ethnicgroup = tab.filter("Total owed a prevention or relief duty1").assert_one().expand(RIGHT)
        breakdown_of_ethnicgroup = ethnicgroup.shift(DOWN)
        unwanted_observations = breakdown_of_ethnicgroup_blank.fill(DOWN).is_not_blank()
        unwanted_ons_geo = tab.filter("Total owed a prevention or relief duty1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_observations|unwanted_ons_geo
        observations = ethnicgroup.shift(DOWN).fill(DOWN).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Total owed a prevention or relief duty1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = tab.filter("Total owed a prevention or relief duty1").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
#         savepreviewhtml(breakdown_of_ethnicgroup, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(ethnicgroup,'ethnicgroup',DIRECTLY, ABOVE),
            HDim(breakdown_of_ethnicgroup,'breakdown_of_ethnicgroup',DIRECTLY, ABOVE),
            HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        print(df['ethnicgroup'].unique())
        print(df['breakdown_of_ethnicgroup'].unique())
        trace.store("combined_dataframe", df)
        
        
# Ignore percentage values - TO be done     
# (A) Geography (Remove Rest of England row as it does not have a geography code) - Done
# (E3:BH3) Ethnicity (including total and not known) - Done
# (E3:BH3) Ethnic Group (including total and not known) - Done

# To be Done
# Measure Type = Applicant
# Unit = count

# +
#Employment status of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A10']: #only transforming tab A10 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        employment_status = tab.filter("Total owed a prevention or relief duty1").assert_one().expand(RIGHT)
        unwanted_ons_geo = employment_status.fill(DOWN).shift(LEFT).shift(LEFT).shift(LEFT).filter("Rest of England").shift(LEFT).expand(RIGHT)|remove_notes
        observations = employment_status.fill(DOWN).expand(RIGHT).is_not_blank()-unwanted_ons_geo
        period = employment_status.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        ons_geo = period.shift(DOWN).shift(DOWN).fill(DOWN).is_not_blank()-unwanted_ons_geo
        sheet_name = tab.name
#         savepreviewhtml(ons_geo, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(employment_status,'employment_status',DIRECTLY, ABOVE),
            HDimConst("sheet_name", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        print(df['employment_status'].unique())
        
        trace.store("combined_dataframe", df)

# Ignore percentage values - done
# (A) Geography (Remove Rest of England row as it does not have a geography code) - Done
# (E3:O3) Employment Status (including total and not known) - Done

# To be done

# Measure Type = Applicant
# Unit = count

# +
# Number of households owed a homelessness duty by sexual identification of lead applicant England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A12']: #only transforming tab A12 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        sexual_identification = tab.filter("Total owed a prevention or relief duty1,2").assert_one().expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total owed a prevention or relief duty1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter("-").expand(RIGHT)|remove_notes
        total_unwanted = remove_notes|unwanted_ons_geo
        observations = sexual_identification.fill(DOWN).expand(RIGHT).is_not_blank()-total_unwanted
        period = tab.filter("Total owed a prevention or relief duty1,2").assert_one().shift(ABOVE).fill(LEFT).is_not_blank()
        ons_geo = tab.filter("Total owed a prevention or relief duty1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        sheet = tab.name
#         savepreviewhtml(ons_geo, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(sexual_identification,'Sexual Identification',DIRECTLY, ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        print(df['Sexual Identification'].unique())
        trace.store("combined_dataframe", df)

# Ignore percentages-No percentages
# Period from title-done
# (A) Geography (Remove Rest of England row as it does not have a geography code)-done
# (E2:K2) Sexual Identification-done

# To be Done

# Measure Type = Applicant
# Unit = count

# +
#Number of households whose prevention duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P1']: #only transforming tab P1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_duty_ended = tab.filter("Total number of households whose prevention duty ended1,2").assert_one().expand(RIGHT)
        accomodation = prevention_duty_ended.shift(DOWN)
        unwanted_ons_geo = tab.filter("Total number of households whose prevention duty ended1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_ons_geo|remove_notes
        observations = accomodation.fill(DOWN).expand(RIGHT).is_not_blank()-total_unwanted
        period = tab.filter("Total number of households whose prevention duty ended1,2").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        ons_geo = tab.filter("Total number of households whose prevention duty ended1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        sheet = tab.name
#         savepreviewhtml(ons_geo, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(prevention_duty_ended,'prevention_duty_ended',DIRECTLY, ABOVE),
            HDim(accomodation,'accomodation',DIRECTLY, ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['Reason Duty ended'] = df['prevention_duty_ended'] + df['accomodation']
        df.drop(['prevention_duty_ended', 'accomodation'],axis=1, inplace = True)
#         print(df['Reason Duty ended'].unique())
        
        temp = {'Secured accommodation for 6+ monthsTotal secured accommodation':'Secured accommodation for 6+months total',
               'Stayed in existing accommodation': 'Secured accommodation for 6+months stayed in existing',
               'Moved to alternative accommodation':'Secured accommodation for 6+months moved to alternative'}
        df['Reason Duty ended'] = df['Reason Duty ended'].replace(temp)
        
        print(df['Reason Duty ended'].unique())
        
        trace.store("combined_dataframe", df)

# Done
# (E3) Reason Duty ended

# 	E3, K3 to R3 to take values in cells
# 	G4 to I4 to take following values:
# 	  Secured accommodation for 6+months total (joined F3 with F4) - Done
#  	  Secured accommodation for 6+months stayed in existing (joined F3 with G4) - Done
# Secured accommodation for 6+months moved to alternative  (joined F3 with H4) - Done

# +
#Number of households whose prevention duty ended by type of accommodation secured England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P2']: #only transforming tab P2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_ons_geo|remove_notes
        prevention_duty_ended_accomodation_secured = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").assert_one().expand(RIGHT)
        prs_and_srs = prevention_duty_ended_accomodation_secured.shift(DOWN)
        tenancy_type = prs_and_srs.shift(DOWN)
        observations = tenancy_type.fill(DOWN).expand(RIGHT).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(prevention_duty_ended_accomodation_secured,'prevention_duty_ended_accomodation_secured',DIRECTLY, ABOVE),
            HDim(prs_and_srs,'prs_and_srs',DIRECTLY, ABOVE),
            HDim(tenancy_type,'tenancy_type',DIRECTLY, ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['Accommodation Type'] = df['prevention_duty_ended_accomodation_secured']+df['prs_and_srs']+df['tenancy_type']
        df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'],axis=1, inplace = True)
        print(df['Accommodation Type'].unique())
        
        temp = {'Private rented sectorTotal PRS':'Private rented sector total',
                'Of which:Self-contained':'Private rented sector self-contained',
                'House in multiple occupation (HMO)':'Private rented sector house in multiple occupation',
                'Lodging (not with family or friends)':'Private rented sector lodging (not with friends and family)',
                'Social rented sectorTotal SRS':'Social rented sector total',
                'Of which:Council\n tenancy':'Social rented sector council tenant',
                'Registered Provider\n tenancy':'Social rented sector registered provider tenant',
                'Supported\n housing or hostel':'Social rented sector supported housing or hostel '}
        
        
        df['Accommodation Type'] = df['Accommodation Type'].replace(temp)
        
        print(df['Accommodation Type'].unique())
        
        trace.store("combined_dataframe", df)

# Done all but verify the below logic as lot other values are in accomodation column
# df['Accommodation Type'] = df['prevention_duty_ended_accomodation_secured']+df['prs_and_srs']+df['tenancy_type']

# (E3) Accommodation Type
# E3, P3 to T3 to take value in cells
# F4 to I4 to have following values:
# 	Private rented sector total (joined F3 with F4)
# 	Private rented sector self-contained (joined F3 with G4 )
# Private rented sector house in multiple occupation (joined F3 with H4 )
# Private rented sector lodging (not with friends and family) (joined F3 with I4) 

# K4 to N4 to have following values:

# 	Social rented sector total (joined K3 with K4)
# 	Social rented sector council tenant (joined K3 with L4)
# 	Social rented sector registered provider tenant (joined K3 with M4)
# 	Social rented sector supported housing or hostel (joined K3 with N4)

# +
# Number of households whose relief duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R1']: #only transforming tab R1 for now
        print(tab.name)     
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Local connection referral accepted by other LA").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes 
        total_unwanted = unwanted_ons_geo|remove_notes
        end_of_relief_duty = tab.filter("Local connection referral accepted by other LA").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT)
        observations = end_of_relief_duty.fill(DOWN).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Local connection referral accepted by other LA").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = tab.filter("Local connection referral accepted by other LA").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(end_of_relief_duty,'Reason Duty ended',DIRECTLY, ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        print(df['Reason Duty ended'].unique())
        
        trace.store("combined_dataframe", df)
        
# (E3) Reason Duty ended
# 	E3 to O3 to take value in cells - DONE
# +
# Number of households whose relief duty ended by type of accommodation secured England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R2']: #only transforming tab R2 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total number of households whose relief duty ended with  accommodation secured1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_ons_geo|remove_notes
        accomodation_secured_at_end_of_relief_duty = tab.filter("Total number of households whose relief duty ended with  accommodation secured1").assert_one().expand(RIGHT)
        break_down = accomodation_secured_at_end_of_relief_duty.shift(DOWN)
        break_down_of_PRS_SRS = break_down.shift(DOWN)
        observations = break_down_of_PRS_SRS.fill(DOWN).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Total number of households whose relief duty ended with  accommodation secured1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = accomodation_secured_at_end_of_relief_duty.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank() 
        sheet = tab.name
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(accomodation_secured_at_end_of_relief_duty,'accomodation_secured_at_end_of_relief_duty',DIRECTLY, ABOVE),
            HDim(break_down,'break_down',DIRECTLY, ABOVE),
            HDim(break_down_of_PRS_SRS,'break_down_of_PRS_SRS',DIRECTLY,ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        df['total_accommodation'] = df['accomodation_secured_at_end_of_relief_duty'] + df['break_down']+df['break_down_of_PRS_SRS']
        print(df['total_accommodation'].unique())
        
        temp = {'Private rented sectorTotal PRS':'Private rented sector total',
               'Of which:Self-contained':'Private rented sector self-contained',
               'HMO':'Private rented sector house in multiple occupation',
               'Lodging (not with family or friends)':'Private rented sector lodging (not with friends and family)',
               'Social rented sectorTotal SRS':'Social rented sector total',
               'Of which:Council\n tenancy':'Social rented sector council tenant',
               'Registered Provider tenancy':'Social rented sector registered provider tenant',
               'Supported \nhousing or hostel':'Social rented sector supported housing or hostel'}
        
        df['Accommodation Type'] = df['total_accommodation'].replace(temp)
        print(df['Accommodation Type'].unique())
        trace.store("combined_dataframe", df)
#     Done but contains other values    
# (E3) Accomodation Type
# E3, P3 to T3 to take value in cells
# F4 to I4 to have following values:
# 	Private rented sector total
# 	Private rented sector self-contained
# Private rented sector house in multiple occupation
# Private rented sector lodging (not with friends and family)
# K4 to N4 to have following values:
# 	Social rented sector total
# 	Social rented sector council tenant
# 	Social rented sector registered provider tenant
# 	Social rented sector supported housing or hostel


# +
# Number of households by decision on duty owed at end of relief duty England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['MD1']: #only transforming tab MD1 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total main duty decisions for eligible households1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        eligible_house_holds = tab.filter("Total main duty decisions for eligible households1,2").assert_one().expand(RIGHT)
        observations = eligible_house_holds.fill(DOWN).is_not_blank()-unwanted_ons_geo
        ons_geo = tab.filter("Total main duty decisions for eligible households1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-unwanted_ons_geo
        period = tab.filter("Total main duty decisions for eligible households1,2").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
#         savepreviewhtml(eligible_house_holds, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(eligible_house_holds,'eligible_house_holds',DIRECTLY, ABOVE),
            HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['Decision on Duty owed'] = df['eligible_house_holds']
        print(df['Decision on Duty owed'].unique())
        
        trace.store("combined_dataframe", df)

# +
# Number of households whose main duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['MD2']: #only transforming tab MD2 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total households whose main duty ended1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        house_holds_duty_ended = tab.filter("Total households whose main duty ended1").assert_one().expand(RIGHT)
        status = house_holds_duty_ended.shift(DOWN)
        observations = status.fill(DOWN).expand(RIGHT).is_not_blank()-unwanted_ons_geo
        ons_geo = tab.filter("Total households whose main duty ended1").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-unwanted_ons_geo 
        period = tab.filter("Total households whose main duty ended1").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(house_holds_duty_ended,'house_holds_duty_ended',DIRECTLY, ABOVE),
            HDim(status,'status',DIRECTLY, ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['house_holds_duty_ended_status'] = df['house_holds_duty_ended'] + df['status']
        df.drop(['house_holds_duty_ended', 'status'],axis=1, inplace = True)
        print(df['house_holds_duty_ended_status'].unique())
        
#         temp = {}
        trace.store("combined_dataframe", df)

# Below needs to be addressed in stage-2 transform
    
"""Look at the value refused, Two different refused are associated with housing act and private
rented sector. As the Refused is there in two columns. The output is just one refused 
which cannot be differentiated according to its association"""
    
#         (A3:O3) Reason for duty end
# A3, M3 to Q3 to take value in cell
# G4:H4 to take following values
#   	Housing Act 1996 Pt6 social housing offer Accepted (joined F3 with F4)
# 	Housing Act 1996 Pt6 social housing offer Refused (joined F3 with G4)
# J4:K4 to take following values
# 	Private rented sector offer Accepted (joined I3 with I4)
# 	Private rented sector offer Refused (joined I3 with J4)

# +
# Number of households owed a main duty by priority need England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['MD3']: #only transforming tab MD3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('From July 2002, "Young applicant" ')).shift(LEFT).expand(DOWN).expand(RIGHT)
        
        households_by_priority = tab.filter("Total households owed a main duty1").assert_one().expand(RIGHT)
        vulnerable_households = households_by_priority.shift(DOWN)
        
        
#         unwanted_ons_geo

        unwanted_ons_geo = tab.filter("Total households owed a main duty1").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter('-').expand(RIGHT)|remove_notes
        
        total_observations = vulnerable_households.fill(DOWN).is_not_blank()-unwanted_ons_geo
        
#         blank
        
        households_by_priority_blank = tab.filter("Total households owed a main duty1").assert_one().expand(RIGHT).is_blank()
        
        vulnerable_households_blank_cells = households_by_priority_blank.shift(DOWN).one_of(['Old age', 'Physical disability / ill health', 'Mental health problems'])
        other_reasons = tab.filter('Homeless because of emergency5').shift(DOWN).shift(LEFT).shift(LEFT).shift(LEFT)
        domestic_abuse = other_reasons.shift(LEFT).shift(LEFT)
        young_applicant = domestic_abuse.shift(LEFT).shift(LEFT)
        total_attributes = other_reasons|domestic_abuse|young_applicant
        vulnerable_households_blank = households_by_priority_blank.shift(DOWN)-vulnerable_households_blank_cells
        vulnerable_households_blank_total = vulnerable_households_blank-total_attributes
        
#         unwanted-observations

        unwanted_observations = vulnerable_households_blank_total.fill(DOWN).is_not_blank()
        observations = total_observations-unwanted_observations
        
#         ons_geo

        ons_geo = tab.filter("Total households owed a main duty1").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-unwanted_ons_geo
        
        period = tab.filter("Total households owed a main duty1").assert_one().shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
#         savepreviewhtml(ons_geo, fname = tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(households_by_priority,'households_by_priority',DIRECTLY, ABOVE),
            HDim(vulnerable_households,'vulnerable_households',DIRECTLY, ABOVE),
#             HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname = tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['households_vulnerable'] = df['households_by_priority']+df['vulnerable_households']
        df.drop(['households_by_priority', 'vulnerable_households'],axis=1, inplace=True)
        
#         print(df['households_vulnerable'].unique())
        
        temp = {'Household member vulnerable as a result of:Total \nvulnerable households':
               'Household member vulnerable as a result of Total', 
                'Old age':'Household member vulnerable as a result of old age',
               'Physical disability / ill health':'Household member vulnerable as a result of physical disability or ill health',
               'Mental health problems':'Household member vulnerable as a result of mental health problems',
               'Young\n applicant2': 'Household member vulnerable as a result of young applicant',
               'Domestic\n abuse':'Household member vulnerable as a result of domestic abuse',
               'Other\nreasons3':'Household member vulnerable as a result of other reasons'}
        
        df['Priority Need'] = df['households_vulnerable'].replace(temp)
        
        print(df['Priority Need'].unique())
        
        trace.store("combined_dataframe", df)
        
        
# Done but contains other values        
# (E3:AA4) Priority Need
# 	E3, G3, I3, AA3 to take value in cell
#  L4: X4 to take following values:
# 	  Household member vulnerable as a result of Total (K33 to K4)
#   Household member vulnerable as a result of old age (K33 to L4) 
# 	  Household member vulnerable as a result of physical disability or ill health (K33 to M4)
# 	  Household member vulnerable as a result of mental health problems (K33 to N4)
# 	  Household member vulnerable as a result of young applicant  (K33 to O4)
# 	  Household member vulnerable as a result of domestic abuse  (K33 to P4)
# 	  Household member vulnerable as a result of other reasons (K33 to Q4)
# Add Decision after Relief duty ended column with value All
# Add Reason for duty end column with value All
# Add Measure Type column with value Households
# Add Unit column with value count and percentage

# +
#Number of households by type of temporary accommodation provided England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['TA1']: #only transforming tab TA1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).shift(LEFT).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total number of households in TA1,2,3,4").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        type_of_households = tab.filter("Total number of households in TA1,2,3,4").assert_one().expand(RIGHT)
        occupants_of_households = type_of_households.shift(DOWN)
        observations = occupants_of_households.fill(DOWN).expand(RIGHT).is_not_blank()-unwanted_ons_geo
        ons_geo = tab.filter("Total number of households in TA1,2,3,4").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-unwanted_ons_geo
        period = tab.filter("Total number of households in TA1,2,3,4").assert_one().shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(type_of_households,'type_of_households',DIRECTLY, ABOVE),
            HDim(occupants_of_households,'occupants_of_households',DIRECTLY, ABOVE),
            HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        trace.store("combined_dataframe", df)
        
# To be Done
        
# (E2:AI2) Accommodation Type
# 	All values in Row 2 (Any with nothing in a cell should be N/A) - Requirements inside brackets needs to be validated
# (H3:AI3) Household Composition column with value all - Requirements inside brackets needs to be validated
# 	All values in Row 3 (Any with nothing in a cell should be N/A)
# +
# Number of households in temporary accommodation by household composition England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['TA2']: #only transforming tab TA2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total number of households in TA1,2").assert_one().shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        
#         required

        adult_and_children_in_household = tab.filter("Total number of households in TA1,2").assert_one().expand(RIGHT)
        adult_and_children = adult_and_children_in_household.shift(ABOVE)
        type_of_occupants_households = adult_and_children.shift(ABOVE)
        male_female = adult_and_children_in_household.shift(DOWN)
        
#         To get rid of % values from observation

        adult_and_children_in_household_blank = tab.filter("Total number of households in TA1,2").assert_one().expand(RIGHT).is_blank()
        female_added = adult_and_children_in_household_blank.shift(DOWN).filter(lambda x: type(x.value) !=  'Female' in x.value) 
        other_gender_added = adult_and_children_in_household_blank.shift(DOWN).filter(lambda x: type(x.value) !=  'Other / gender not known' in x.value) 
        total_add = female_added|other_gender_added
        male_female_required = adult_and_children_in_household_blank.shift(DOWN)-total_add
        
#         unwanted observations and unwanted ons_geo

        unwanted_observations = male_female_required.fill(DOWN).is_not_blank()
        unwanted_ons_geo = tab.filter('Total number of households in TA1,2').shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter('-').expand(RIGHT)
        total_unwanted = unwanted_observations|unwanted_ons_geo

#         required observations

        observations = male_female.fill(DOWN).is_not_blank()-total_unwanted
    
#         ons_geo

        total_unwanted_ons_geo = unwanted_ons_geo|remove_notes
        ons_geo = tab.filter('Total number of households in TA1,2').shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted_ons_geo
        
        period = tab.filter('Sum of Couple with dependent children').shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(type_of_occupants_households,'type_of_occupants_households',DIRECTLY, ABOVE),
            HDim(adult_and_children,'adult_and_children',DIRECTLY, ABOVE),
            HDim(adult_and_children_in_household,'adult_and_children_in_household',DIRECTLY, ABOVE),
            HDim(male_female,'male_female',DIRECTLY, ABOVE),
            HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
        df['Household Composition'] = df['adult_and_children_in_household']+df['male_female']
        
        df.drop(['adult_and_children_in_household', 'male_female'],axis=1, inplace = True)
        print(df['Household Composition'].unique())
        
#         Two 'Female' column and 'Other / gender not known' which needs to be distinguished
        
        trace.store("combined_dataframe", df)
# -

df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

# #output cube and spec
# cubes.add_cube(scraper, df.drop_duplicates(), original_tabs.title)
# cubes.output_all()
# trace.render("spec_v1.html")
# pd.DataFrame(df).to_csv('final-output.csv')
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

pd.DataFrame(df).to_csv('final-output.csv')
