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
# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A2P', 'A2R_']: #only transforming tab A2P for now
        print(tab.name)
    
        remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
        reason_for_loss_of_home_1 = tab.filter("End of assured shorthold (AST) private rented tenancy, due to..").assert_one().shift(LEFT).shift(LEFT).expand(RIGHT)
        end_of_tenancy_2 = reason_for_loss_of_home_1.shift(DOWN)
        reason_for_end_of_tenancy_3 = end_of_tenancy_2.shift(DOWN)
        change_of_circumstances_4 = reason_for_end_of_tenancy_3.shift(DOWN)
        observations = change_of_circumstances_4.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(RIGHT)
        ons_geo = unwanted.shift(LEFT)-unwanted
        period = reason_for_loss_of_home_1.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(reason_for_loss_of_home_1,'reason_for_loss_of_home_1',DIRECTLY, ABOVE),
            HDim(end_of_tenancy_2,'end_of_tenancy_2',DIRECTLY, ABOVE),
            HDim(reason_for_end_of_tenancy_3,'reason_for_end_of_tenancy_3',DIRECTLY, ABOVE),
            HDim(change_of_circumstances_4,'change_of_circumstances_4',DIRECTLY, ABOVE),
            HDimConst("sheet", tab.name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        df = tidy_sheet.topandas()
        df["Period"]= df["Period"].str.split(", ", n = -1, expand = True)[3]
        
        df['Reason for loss or threat of loss of home'] = df['reason_for_loss_of_home_1']+df['end_of_tenancy_2']+df['reason_for_end_of_tenancy_3']+df['change_of_circumstances_4']
        df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3','change_of_circumstances_4'], axis=1, inplace=True)


        print(df['Period'].unique())
        print(df['Reason for loss or threat of loss of home'].unique())
        if tab.name == 'A2P':
            df['Duty Type'] = df['sheet'].apply(lambda x: "a2p.Prevention" if x == 'A2P' else x)
#         df.head(5)
        if tab.name == 'A2R_':
            df['Duty Type'] = df['sheet'].apply(lambda x: "a2r.Relief" if x == 'A2R_' else x)
        df.drop(['sheet'], axis=1, inplace=True)
        trace.store("combined_dataframe", df)
        
#More clarity needed on Spec.

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A3']: #only transforming tab A3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).assert_one().expand(DOWN).expand(RIGHT)
        reason_of_households_with_support_needs = tab.filter("Households with no support needs owed duty1,2").assert_one().expand(RIGHT)
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
        trace.store("combined_dataframe", df)


# The Requirement
# H  - Total households with support needs
# I4 - Households with one support need
# J4 - Households with two support needs
# K4 - Households with three or more support needs

# 'Number of householdsHouseholds with three or more support needs',is a odd value. Needs investigation.
#'Households with one or more support needs owed duty1,2Total households with support needs',is a odd value. Needs investigation.

# +
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
# df.head()

# +
# Number of households owed a prevention duty by household composition England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A5P', 'A5R']: #only transforming tab A5P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_duty_owed_by_household = tab.filter("Single parent with dependent children").shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT)
        single_parent_adult_male_female = prevention_duty_owed_by_household.shift(DOWN)
        observations = prevention_duty_owed_by_household.shift(DOWN).fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(RIGHT)
        ons_geo = unwanted.shift(LEFT)-unwanted
        sheet = tab.name
        period = prevention_duty_owed_by_household.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,LEFT),
            HDim(prevention_duty_owed_by_household,'prevention_duty_owed_by_household',DIRECTLY, ABOVE),
            HDim(single_parent_adult_male_female,'single_parent_adult_male_female',DIRECTLY, ABOVE),
            HDimConst('sheet', tab.name),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
#         df['Household composition'] = df['prevention_duty_owed_by_household']+df['single_parent_adult_male_female']
        
        #a5p&a5r.prevention &relief to be changed
        if tab.name == 'A5P':
            df['Duty Type'] = df['sheet'].apply(lambda x: "a5p.Prevention" if x == 'A5P' else x)

        if tab.name == 'A5R':
            df['Duty Type'] = df['sheet'].apply(lambda x: "a5r.Relief" if x == 'A5R' else x)
        
        
        df['Household composition'] = df['prevention_duty_owed_by_household']+df['single_parent_adult_male_female']
        df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
        df.drop(['sheet'], axis=1, inplace=True)
#         print(df['Household composition'].value_counts())
#         print(df['Duty Type'].value_counts())
        trace.store("combined_dataframe", df)
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
        referral_public_body = tab.filter("Total households assessed as a result of a referral1,5").expand(RIGHT)
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
        
#         print(df['Referral Public Body'].unique())
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
        total_unwanted = tab.filter("Total owed a prevention or relief duty1").shift(RIGHT).expand(DOWN)|remove_notes
        age_of_main_applicants = tab.filter("Total owed a prevention or relief duty1").expand(RIGHT).is_not_blank().filter(lambda x: type(x.value) != '%' not in x.value) 
        unwanted_ons_geo = tab.filter("Total owed a prevention or relief duty1").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-remove_notes
        unwanted = unwanted_ons_geo.filter("-").expand(RIGHT)|remove_notes
        ons_geo = unwanted_ons_geo-unwanted
        period = tab.filter("Total owed a prevention or relief duty1").shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
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
        
        
        trace.store("combined_dataframe", df)

# (E3:W3) Age (including total and not known)
# Measure Type = Applicant
# Unit = count

# +
#Ethnicity of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A8']: #only transforming tab A8 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        unwanted = tab.excel_ref("A6").expand(DOWN).filter("-").expand(RIGHT)|remove_notes
        ethnicgroup = tab.filter("Total owed a prevention or relief duty1").expand(RIGHT)
        breakdown_of_ethnicgroup = ethnicgroup.shift(DOWN)
        observations = breakdown_of_ethnicgroup.fill(DOWN).expand(RIGHT).is_not_blank()-unwanted
        unwanted = observations.shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(RIGHT)-remove_notes
        ons_geo = unwanted.shift(LEFT)-unwanted
        period = tab.filter("Total owed a prevention or relief duty1").shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
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
        
        trace.store("combined_dataframe", df)
        
# Ignore percentages - TO be done
# (A) Geography (Remove Rest of England row as it does not have a geography code) - Done
# (E3:BH3) Ethnicity (including total and not known) - To be done
# (E3:BH3) Ethnic Group (including total and not known) - To be done



# +
#Employment status of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A10']: #only transforming tab A10 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        employment_status = tab.filter("Total owed a prevention or relief duty1").expand(RIGHT)
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
        
        trace.store("combined_dataframe", df)

# Ignore percentages - To be done
# (A) Geography (Remove Rest of England row as it does not have a geography code) - Done
# (E3:O3) Employment Status (including total and not known) - To be done

# +
# Number of households owed a homelessness duty by sexual identification of lead applicant England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A12']: #only transforming tab A12 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        sexual_identification = tab.filter("Total owed a prevention or relief duty1,2").expand(RIGHT)
        unwanted_ons_geo = tab.filter("Total owed a prevention or relief duty1,2").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter("-").expand(RIGHT)|remove_notes
        total_unwanted = remove_notes|unwanted_ons_geo
        observations = sexual_identification.fill(DOWN).expand(RIGHT).is_not_blank()-total_unwanted
        period = tab.filter("Total owed a prevention or relief duty1,2").shift(ABOVE).fill(LEFT).is_not_blank()
        ons_geo = tab.filter("Total owed a prevention or relief duty1,2").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
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
        trace.store("combined_dataframe", df)
# Ignore percentages-No percentages
# Period from title-done
# (A) Geography (Remove Rest of England row as it does not have a geography code)-done
# (E2:K2) Sexual Identification-done

# +
#Number of households whose prevention duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P1']: #only transforming tab P1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_duty_ended = tab.filter("Total number of households whose prevention duty ended1,2").expand(RIGHT)
        accomodation = prevention_duty_ended.shift(DOWN)
        unwanted_ons_geo = tab.filter("Total number of households whose prevention duty ended1,2").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank().filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_ons_geo|remove_notes
        observations = accomodation.fill(DOWN).expand(RIGHT).is_not_blank()-total_unwanted
        period = tab.filter("Total number of households whose prevention duty ended1,2").shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        ons_geo = tab.filter("Total number of households whose prevention duty ended1,2").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
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
        unwanted_ons_geo = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_ons_geo|remove_notes
        prevention_duty_ended_accomodation_secured = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").expand(RIGHT)
        prs_and_srs = prevention_duty_ended_accomodation_secured.shift(DOWN)
        tenancy_type = prs_and_srs.shift(DOWN)
        observations = tenancy_type.fill(DOWN).expand(RIGHT).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = tab.filter("Total number of households whose prevention duty ended with accommodation secured1").shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
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
        unwanted_ons_geo = tab.filter("Local connection referral accepted by other LA").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes 
        total_unwanted = unwanted_ons_geo|remove_notes
        end_of_relief_duty = tab.filter("Local connection referral accepted by other LA").shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT)
        observations = end_of_relief_duty.fill(DOWN).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Local connection referral accepted by other LA").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = tab.filter("Local connection referral accepted by other LA").shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank()
        sheet = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(end_of_relief_duty,'Reason Duty ended',DIRECTLY, ABOVE),
            HDimConst("sheet", sheet) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        
        df = tidy_sheet.topandas()
        
        df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
        
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
        unwanted_ons_geo = tab.filter("Total number of households whose relief duty ended with  accommodation secured1").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).filter("-").expand(RIGHT)|remove_notes
        total_unwanted = unwanted_ons_geo|remove_notes
        accomodation_secured_at_end_of_relief_duty = tab.filter("Total number of households whose relief duty ended with  accommodation secured1").expand(RIGHT)
        break_down = accomodation_secured_at_end_of_relief_duty.shift(DOWN)
        break_down_of_PRS_SRS = break_down.shift(DOWN)
        observations = break_down_of_PRS_SRS.fill(DOWN).is_not_blank()-total_unwanted
        ons_geo = tab.filter("Total number of households whose relief duty ended with  accommodation secured1").shift(LEFT).shift(LEFT).shift(LEFT).shift(LEFT).fill(DOWN).is_not_blank()-total_unwanted
        period = accomodation_secured_at_end_of_relief_duty.shift(ABOVE).shift(ABOVE).fill(LEFT).is_not_blank() 
        sheet = tab.name
#         ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
#         period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
#         accomodation_secured_at_end_of_relief_duty = tab.excel_ref('D3').expand(RIGHT)
#         break_down = tab.excel_ref('D4').expand(RIGHT)
#         break_down_of_PRS_SRS = tab.excel_ref('D5').expand(RIGHT)
#         observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
# #         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
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
        
        trace.store("combined_dataframe", df)


# +
# Main relief activity that resulted in accommodation secured for households at end of relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R3']: #only transforming tab R3_ for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).shift(LEFT).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        accomodation_secured = tab.excel_ref('D3').expand(RIGHT)
        observations = tab.excel_ref('D4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(accomodation_secured, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(accomodation_secured,'accomodation_secured',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")


#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df


# +
# Household type of households with accommodation secured at end of relief duty England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R5']: #only transforming tab R5 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        secured_accomodation_at_end_of_relief_duty = tab.excel_ref('D3').expand(RIGHT)
        male_female_other_gender = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(secured_accomodation_at_end_of_relief_duty,'secured_accomodation_at_end_of_relief_duty',DIRECTLY, ABOVE),
            HDim(male_female_other_gender, 'male_female_other_gender', DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# Number of households by decision on duty owed at end of relief duty England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['MD1']: #only transforming tab MD1 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        eligible_house_holds = tab.excel_ref('E3').expand(RIGHT)
#         male_female_other_gender = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('E4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(eligible_house_holds, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(eligible_house_holds,'eligible_house_holds',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)
#Sheet = R5
df.drop(['secured_accomodation_at_end_of_relief_duty', 'male_female_other_gender'], axis=1, inplace=True)


df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# Number of households whose main duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['MD2']: #only transforming tab MD2 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        house_holds_duty_ended = tab.excel_ref('E3').expand(RIGHT)
        status = tab.excel_ref('E4').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(house_holds_duty_ended, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(house_holds_duty_ended,'house_holds_duty_ended',DIRECTLY, ABOVE),
            HDim(status,'status',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)
#Sheet = R5
df.drop(['secured_accomodation_at_end_of_relief_duty', 'male_female_other_gender'], axis=1, inplace=True)
#Sheet = MD1
df.drop(['eligible_house_holds'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# Number of households owed a main duty by priority need England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['MD3']: #only transforming tab MD3 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('From July 2002, "Young applicant" ')).shift(LEFT).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(remove_notes, fname= tab.name + "PREVIEW.html")
        households_by_priority = tab.excel_ref('E3').expand(RIGHT)
        vulnerable_households = tab.excel_ref('E4').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(households_by_priority,'households_by_priority',DIRECTLY, ABOVE),
            HDim(vulnerable_households,'vulnerable_households',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)
#Sheet = R5
df.drop(['secured_accomodation_at_end_of_relief_duty', 'male_female_other_gender'], axis=1, inplace=True)
#Sheet = MD1
df.drop(['eligible_house_holds'], axis=1, inplace=True)
#Sheet = MD2
df.drop(['house_holds_duty_ended', 'status'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df
# +
#Number of households by type of temporary accommodation provided England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['TA1']: #only transforming tab TA1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        type_of_households = tab.excel_ref('E2').expand(RIGHT)
        occupants_of_households = tab.excel_ref('E3').expand(RIGHT)
        observations = tab.excel_ref('E4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(occupants_of_households, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(type_of_households,'type_of_households',DIRECTLY, ABOVE),
            HDim(occupants_of_households,'occupants_of_households',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)
#Sheet = R5
df.drop(['secured_accomodation_at_end_of_relief_duty', 'male_female_other_gender'], axis=1, inplace=True)
#Sheet = MD1
df.drop(['eligible_house_holds'], axis=1, inplace=True)
#Sheet = MD2
df.drop(['house_holds_duty_ended', 'status'], axis=1, inplace=True)
#Sheet = TA1
df.drop(['households_by_priority', 'vulnerable_households'], axis=1, inplace=True)

# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
# df
# +
# Number of households in temporary accommodation by household composition England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['TA2']: #only transforming tab TA2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")

        type_of_occupants_households = tab.excel_ref('E3').expand(RIGHT)
        adult_and_children = tab.excel_ref('E4').expand(RIGHT)
        adult_and_children_in_household = tab.excel_ref('E5').expand(RIGHT)
        male_female = tab.excel_ref('E6').expand(RIGHT)
        observations = tab.excel_ref('E7').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(type_of_occupants_households,'type_of_occupants_households',DIRECTLY, ABOVE),
            HDim(adult_and_children,'adult_and_children',DIRECTLY, ABOVE),
            HDim(adult_and_children_in_household,'adult_and_children_in_household',DIRECTLY, ABOVE),
            HDim(male_female,'male_female',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)
#Sheet = R5
df.drop(['secured_accomodation_at_end_of_relief_duty', 'male_female_other_gender'], axis=1, inplace=True)
#Sheet = MD1
df.drop(['eligible_house_holds'], axis=1, inplace=True)
#Sheet = MD2
df.drop(['house_holds_duty_ended', 'status'], axis=1, inplace=True)
#Sheet = TA1
df.drop(['households_by_priority', 'vulnerable_households'], axis=1, inplace=True)
#Sheet = TA1
df.drop(['type_of_households', 'occupants_of_households'], axis=1, inplace=True)

# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
# df

# +
# Number of households by duty under which temporary accommodation is provided England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['TA3']: #only transforming tab TA3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).shift(LEFT).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(remove_notes, fname= tab.name + "PREVIEW.html")

        temporary_accomodation_households = tab.excel_ref('E3').expand(RIGHT)
        breakdown_of_accomodation = tab.excel_ref('E4').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(temporary_accomodation_households,'temporary_accomodation_households',DIRECTLY, ABOVE),
            HDim(breakdown_of_accomodation,'breakdown_of_accomodation',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
#Sheet = A2R
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)
# Sheet = A5P
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
# Sheet = A5R
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)
#Sheet = A6_
df.drop(['age_of_main_applicants'], axis=1, inplace=True)
#Sheet = A7
df.drop(['assessed_household', 'referred_household', 'breakdown_of_referred_household'], axis=1, inplace=True)
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)
#Sheet = P2
df.drop(['prevention_duty_ended_accomodation_secured', 'prs_and_srs', 'tenancy_type'], axis=1, inplace=True)
#Sheet = P3
df.drop(['type_of_secured_accomodation'], axis=1, inplace=True)
#Sheet = P5
df.drop(['accomodation_secured_at_end_of_prevention_duty', 'gender'], axis=1, inplace=True)
#Sheet = R1
df.drop(['end_of_relief_duty'], axis=1, inplace=True)
#Sheet = R2
df.drop(['accomodation_secured_at_end_of_relief_duty', 'break_down', 'break_down_of_PRS_SRS'], axis=1, inplace=True)
#Sheet = R3_
df.drop(['accomodation_secured'], axis=1, inplace=True)
#Sheet = R5
df.drop(['secured_accomodation_at_end_of_relief_duty', 'male_female_other_gender'], axis=1, inplace=True)
#Sheet = MD1
df.drop(['eligible_house_holds'], axis=1, inplace=True)
#Sheet = MD2
df.drop(['house_holds_duty_ended', 'status'], axis=1, inplace=True)
#Sheet = TA1
df.drop(['households_by_priority', 'vulnerable_households'], axis=1, inplace=True)
#Sheet = TA1
df.drop(['type_of_households', 'occupants_of_households'], axis=1, inplace=True)
#Sheet = TA2
df.drop(['type_of_occupants_households', 'adult_and_children', 'adult_and_children_in_household', 'male_female'], axis=1, inplace=True)

# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
# df
# -

df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

# #output cube and spec
# cubes.add_cube(scraper, df.drop_duplicates(), original_tabs.title)
# cubes.output_all()
# trace.render("spec_v1.html")
# pd.DataFrame(df).to_csv('final-output.csv')
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

pd.DataFrame(df).to_csv('final-output.csv')
