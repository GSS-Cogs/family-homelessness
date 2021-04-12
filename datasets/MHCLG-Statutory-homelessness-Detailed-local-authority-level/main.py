# # MHCLG Statutory homelessness Detailed local authority-level 

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
scraper = Scraper(seed = "info.json")
scraper.distributions = [x for x in scraper.distributions if hasattr(x, "mediaType")] 
scraper


original_tabs = scraper.distribution(title = lambda x: "Detailed local authority level tables: July to September 2020 (revised)" in x)
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
datasetTitle
for tab in tabs:
    print(tab.name)

# + endofcell="--"
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A1']: #only transforming tab A1 for now
    
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A6').expand(DOWN).is_not_blank() - remove_notes
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        temp_assessment_duty_type_1 = tab.excel_ref('C3').expand(RIGHT)
        temp_assessment_duty_type_2 = tab.excel_ref('C4').expand(RIGHT)
        temp_assessment_duty_type_3 = tab.excel_ref('C5').expand(RIGHT)
        observations = tab.excel_ref('C6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(temp_assessment_duty_type_1,'temp_assessment_duty_type_1',DIRECTLY, ABOVE),
            HDim(temp_assessment_duty_type_2,'temp_assessment_duty_type_2',DIRECTLY, ABOVE),
            HDim(temp_assessment_duty_type_3,'temp_assessment_duty_type_3',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
    else:
        continue 

# # +
#Below is how I matched the values up - I just took this info from the spec for tab A1

#Initial Assessments                                                   Duty Type Owned
#- Total Initial Assessments                                           - N/A
#- Total owed a prevention of relief duty                              - Relief
#- Threatened with homelessness within 56 days                         - Prevention
#- Due to service of valid Section 21 Notice                           - Prevention
#- Homeless                                                            - Relief
#- Not homeless nor threatened with homelessness within 56 days        - No duty owed
#- Number of Households in area (000s)                                 - All
#- Households assessed as threatened with homelessness per(000s)       - N/A
#- Households assessed as homeless per(000s)                           - N/A

# # +
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df
df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
#Bring the 3 temp columns together - we will then decide the Duty Type Owed values based on them
df['assessment_duty_type'] = df['temp_assessment_duty_type_1'] + df['temp_assessment_duty_type_2'] + df['temp_assessment_duty_type_3']
#drop the other temp ones as no longer needed 
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#Check the outputs of the temp column
df['assessment_duty_type'].unique()
#Use lambda function to map to correct values we want for Inital assessmrnt column first 

df['Initial Circumstance Assessment'] = df['assessment_duty_type'].map(lambda x: 'Total Initial Assessments' if 'Total initial assessments1' in x 
                                                                       else ('Total owed a prevention of relief duty' if 'Assessed as owed a dutyTotal owed a prevention or relief duty' in x 
                                                                             else ('Threatened with homelessness within 56 days' if 'Threatened with homelessness within 56 days - \nPrevention duty owed' in x else
                                                                                  ('Due to service of valid Section 21 Notice' if 'Of which:due to service of valid Section 21 Notice3' in x 
                                                                                   else ('Homeless' if 'Homeless - \nRelief duty owed4' in x 
                                                                                        else ('Not homeless nor threatened with homelessness within 56 days' if 'Not homeless nor threatened with homelessness within 56 days - no duty owed' in x 
                                                                                             else ('Number of Households in area (000s)' if 'Number of households\n in area4 (000s)' in x 
                                                                                                  else('Households assessed as threatened with homelessness per(000s)' if 'Households assessed as threatened with homelessness\nper (000s)' in x
                                                                                                     else ('Households assessed as homeless per(000s)' if 'Households assessed as homeless\nper (000s)' in x else x )))))))))

#drop other temp column 
df.drop(['assessment_duty_type'], axis=1, inplace=True)
#map Duty Type Owned values based on Initial Circumstance Assessment column values 
df['Duty Type Owned values'] = df['Initial Circumstance Assessment'].map(lambda x: 'N/A' if 'Total Initial Assessments' in x 
                                                                       else ('Relief' if 'Total owed a prevention of relief duty' in x 
                                                                             else ('Prevention' if 'Threatened with homelessness within 56 days' in x else
                                                                                  ('Prevention' if 'Due to service of valid Section 21 Notice' in x 
                                                                                   else ('Relief' if 'Homeless' in x 
                                                                                        else ('No duty owed' if 'Not homeless nor threatened with homelessness within 56 days' in x 
                                                                                             else ('All' if 'Number of Households in area (000s)' in x 
                                                                                                  else('N/A' if 'Households assessed as threatened with homelessness per(000s)' in x
                                                                                                     else ('N/A' if 'Households assessed as homeless per(000s)' in x else x )))))))))

# -

#Checking values are what I expect 
df['Duty Type Owned values'].unique()

#Checking values are what I expect 
df['Initial Circumstance Assessment'].unique()

df.head()

# # +
# Note all the other dimension's will need to be added but they seem to be contants for this tab anyway 
# so could always add them in later and use the sheet name as reference or something along those lines. 
# Hope this helps. 
# -
# --
# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A2P']: #only transforming tab A2P for now
        print(tab.name)
    
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A6').fill(DOWN).is_not_blank() - remove_notes
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name

        reason_for_loss_of_home_1 = tab.excel_ref('C3').expand(RIGHT)
        end_of_tenancy_2 = tab.excel_ref('C4').expand(RIGHT)
        reason_for_end_of_tenancy_3 = tab.excel_ref('C5').expand(RIGHT)
        change_of_circumstances_4 = tab.excel_ref('C6').expand(RIGHT)
        observations = tab.excel_ref('C7').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(reason_for_loss_of_home_1,'reason_for_loss_of_home_1',DIRECTLY, ABOVE),
            HDim(end_of_tenancy_2,'end_of_tenancy_2',DIRECTLY, ABOVE),
            HDim(reason_for_end_of_tenancy_3,'reason_for_end_of_tenancy_3',DIRECTLY, ABOVE),
            HDim(change_of_circumstances_4,'change_of_circumstances_4',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df['reason_for_loss_or_loss_of_tenancy'] = df['reason_for_loss_of_home_1']+df['end_of_tenancy_2']+df['reason_for_end_of_tenancy_3']+df['change_of_circumstances_4']
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = -1, expand = True)[3]

df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
df

# +
#Number of households owed a relief duty by reason for loss, or threat of loss, of last settled home England
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A2R_']: #only transforming tab A2P for now
        print(tab.name)
    
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A6').fill(DOWN).is_not_blank() - remove_notes
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")

        relief_duty_by_reason = tab.excel_ref('C3').expand(RIGHT)
        end_of_AST = tab.excel_ref('C4').expand(RIGHT)
        reason_for_end_of_AST = tab.excel_ref('C5').expand(RIGHT)
        reason_for_rent_arrears = tab.excel_ref('C6').expand(RIGHT)
        observations = tab.excel_ref('C7').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(relief_duty_by_reason,'relief_duty_by_reason',DIRECTLY, ABOVE),
            HDim(end_of_AST,'end_of_AST',DIRECTLY, ABOVE),
            HDim(reason_for_end_of_AST,'reason_for_end_of_AST',DIRECTLY, ABOVE),
            HDim(reason_for_rent_arrears,'reason_for_rent_arrears',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

df['total_relief_duty_by_reason'] = df['relief_duty_by_reason'] + df['end_of_AST']+df['reason_for_end_of_AST']+df['reason_for_rent_arrears']
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)

df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = -1, expand = True)[3]
df

# +
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A3']: #only transforming tab A3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A4').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        
        total_no_of_households = tab.excel_ref('C2').expand(RIGHT)
        reason_of_households_with_support_needs = tab.excel_ref('C3').expand(RIGHT)
        total_households_and_no_of_people_with_support_needs = tab.excel_ref('C4').expand(RIGHT)
        observations = tab.excel_ref('C5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(total_no_of_households,'total_no_of_households',DIRECTLY, ABOVE),
            HDim(reason_of_households_with_support_needs,'reason_of_households_with_support_needs',DIRECTLY, ABOVE),
            HDim(total_households_and_no_of_people_with_support_needs,'total_households_and_no_of_people_with_support_needs',DIRECTLY, ABOVE)
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
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

df


#This output csv file has 3+ value
pd.DataFrame(df['total_households_and_no_of_people_with_support_needs'].unique()).to_csv('output.csv')

#sheet:A3 - combine three series into one series in the dataframe
df['total_no_of_households_with_support_needs'] = df['total_no_of_households'] + df['reason_of_households_with_support_needs'] + df['total_households_and_no_of_people_with_support_needs']

# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)

#This output CSv doesn't have 3+ or has Number of households3+. Needs further investigation
pd.DataFrame(df['total_no_of_households_with_support_needs'].unique()).to_csv('output.csv')

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]

# df['total_households_with_support_needs'] = df['total_no_of_households_with_support_needs'].map(lambda x: "Households with one support need" if '1.0' in x else x)

# The Requirement
# H  - Total households with support needs (Already extracted from spreadsheet)
# I4 - Households with one support need
# J4 - Households with two support needs
# K4 - Households with three or more support needs

# Above three column names needs to be processed. Blocked. Needs investigation

# pd.api.types.is_string_dtype(df['total_households_and_no_of_people_with_support_needs'])

# For now moving on to the next tab or sheet
df

# +
#Number of households owed a prevention duty by accommodation at time of application England
for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A4P']: #only transforming tab A4P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A4').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        
        prevention_duty_owed_by_sector = tab.excel_ref('C3').expand(RIGHT)
        prs_srs_homeless_on_departure_from_institution = tab.excel_ref('C4').expand(RIGHT)
        status_of_occupation = tab.excel_ref('C5').expand(RIGHT)
        observations = tab.excel_ref('C6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(prevention_duty_owed_by_sector,'prevention_duty_owed_by_sector',DIRECTLY, ABOVE),
            HDim(prs_srs_homeless_on_departure_from_institution,'prs_srs_homeless_on_departure_from_institution',DIRECTLY, ABOVE),
            HDim(status_of_occupation,'status_of_occupation',DIRECTLY, ABOVE)
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df['total_prevention'] = df['prevention_duty_owed_by_sector']+df['prs_srs_homeless_on_departure_from_institution']+df['status_of_occupation']
#sheet:A4P
df.drop(['prevention_duty_owed_by_sector', 'prs_srs_homeless_on_departure_from_institution', 'status_of_occupation'],axis=1,inplace=True)
# df
#sheet:A1
df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#sheet:A2P
df.drop(['reason_for_loss_of_home_1', 'end_of_tenancy_2', 'reason_for_end_of_tenancy_3', 'change_of_circumstances_4'], axis=1, inplace=True)
#sheet:A2R_
df.drop(['relief_duty_by_reason', 'end_of_AST', 'reason_for_end_of_AST', 'reason_for_rent_arrears'], axis =1, inplace=True)
# sheet:A3
df.drop(['total_no_of_households', 'reason_of_households_with_support_needs', 'total_households_and_no_of_people_with_support_needs'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]

df

# +
# Number of households owed a relief duty by accommodation at time of application England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A4R']: #only transforming tab A4R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A4').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        
        relief_duty_owed_by_sector = tab.excel_ref('C3').expand(RIGHT)
        relief_prs_srs_homeless_on_departure_from_institution = tab.excel_ref('C4').expand(RIGHT)
        relief_status_of_occupation = tab.excel_ref('C5').expand(RIGHT)
        observations = tab.excel_ref('C6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(relief_duty_owed_by_sector,'relief_duty_owed_by_sector',DIRECTLY, ABOVE),
            HDim(relief_prs_srs_homeless_on_departure_from_institution,'relief_prs_srs_homeless_on_departure_from_institution',DIRECTLY, ABOVE),
            HDim(relief_status_of_occupation,'relief_status_of_occupation',DIRECTLY, ABOVE)
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = A2R
df['Relief_Total'] = df['relief_duty_owed_by_sector']+df['relief_prs_srs_homeless_on_departure_from_institution']+df['relief_status_of_occupation']
df.drop(['relief_duty_owed_by_sector', 'relief_prs_srs_homeless_on_departure_from_institution', 'relief_status_of_occupation'], axis=1, inplace=True)

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

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]

df

# +
# Number of households owed a prevention duty by household composition England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A5P']: #only transforming tab A5P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A4').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        prevention_duty_owed_by_household = tab.excel_ref('C3').expand(RIGHT)
        single_parent_adult_male_female = tab.excel_ref('C4').expand(RIGHT)
        observations = tab.excel_ref('C6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(single_parent_adult_male_female, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(prevention_duty_owed_by_household,'prevention_duty_owed_by_household',DIRECTLY, ABOVE),
            HDim(single_parent_adult_male_female,'single_parent_adult_male_female',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
# df
df['prevention_duty_male_female'] = df['prevention_duty_owed_by_household']+df['single_parent_adult_male_female']
df.drop(['prevention_duty_owed_by_household', 'single_parent_adult_male_female'], axis=1, inplace=True)
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

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df
# +
# Number of households owed a relief duty by household composition England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A5R']: #only transforming tab A5R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        remove_notes_1 = tab.excel_ref("C334").expand(DOWN).expand(RIGHT).shift(LEFT).shift(LEFT)
        remove_total = remove_notes|remove_notes_1
        ons_geo = tab.excel_ref('A4').fill(DOWN).is_not_blank() - remove_total # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        
#         savepreviewhtml(ons_geo, fname= tab.name + "PREVIEW.html")
        
        relief_duty_owed_by_household = tab.excel_ref('E3').expand(RIGHT)
        relief_single_parent_adult_male_female = tab.excel_ref('E4').expand(RIGHT)
        observations = tab.excel_ref('E6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_total
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(relief_duty_owed_by_household,'relief_duty_owed_by_household',DIRECTLY, ABOVE),
            HDim(relief_single_parent_adult_male_female,'relief_single_parent_adult_male_female',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df['relief_duty_owed'] = df['relief_duty_owed_by_household']+df['relief_single_parent_adult_male_female']
df.drop(['relief_duty_owed_by_household', 'relief_single_parent_adult_male_female'], axis=1, inplace=True)



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


df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df
# +
#Age of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A6_']: #only transforming tab A6_ for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name

        age_of_main_applicants = tab.excel_ref('E3').expand(RIGHT)
        observations = tab.excel_ref('E4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(age_of_main_applicants,'age_of_main_applicants',DIRECTLY, ABOVE),
#             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
# df

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

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# for tab in tabs:
#     columns=['TO DO']
#     trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
#     if tab.name in ['A7']: #only transforming tab A7 for now
#         print(tab.name)
        
#         remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
#         remove_notes_1 = tab.filter(contains_string('% assessed as owed a duty'))
#         total_remove = remove_notes|remove_notes_1
#         ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - total_remove # "-" suppressed in geography code to be processed in stage-2 transformation
#         period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
# #         sheet_name = tab.name
        
# #         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
# #         assessed_household = tab.excel_ref('E3').expand(RIGHT)
# #         referred_household = tab.excel_ref('E4').expand(RIGHT)
# #         breakdown_of_referred_household = tab.excel_ref('E5').expand(RIGHT)
#         observations = tab.excel_ref('E6').expand(DOWN).expand(RIGHT).is_not_blank() - total_remove
# #         savepreviewhtml(assessed_household, fname= tab.name + "PREVIEW.html")
#         dimensions = [
#             HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
#             HDim(period,'Period',CLOSEST,ABOVE),
# #             HDim(assessed_household,'assessed_household',DIRECTLY, ABOVE),
# #             HDim(referred_household,'referred_household',DIRECTLY, ABOVE),
# #             HDim(breakdown_of_referred_household, 'breakdown_of_referred_household', DIRECTLY, ABOVE),
# #             HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
#         ]
#         tidy_sheet = ConversionSegment(tab, dimensions, observations)
#         savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
# #         savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
# #         trace.with_preview(tidy_sheet)
# #         trace.store("combined_dataframe", tidy_sheet.topandas())
# # df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
# +
#Ethnicity of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A8']: #only transforming tab A8 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(remove_notes, fname= tab.name + "PREVIEW.html")

        ethnicgroup = tab.excel_ref('E3').expand(RIGHT)
        breakdown_of_ethnicgroup = tab.excel_ref('E4').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(ethnicgroup, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(ethnicgroup,'ethnicgroup',DIRECTLY, ABOVE),
            HDim(breakdown_of_ethnicgroup,'breakdown_of_ethnicgroup',DIRECTLY, ABOVE),
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


df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df


# +
#Employment status of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A10']: #only transforming tab A10 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        employment_status = tab.excel_ref('E3').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(employment_status,'employment_status',DIRECTLY, ABOVE),
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
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)


df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# Number of households owed a homelessness duty by sexual identification of lead applicant England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['A12']: #only transforming tab A12 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(ons_geo, fname= tab.name + "PREVIEW.html")
        
        sexual_identification = tab.excel_ref('E2').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(sexual_identification, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(sexual_identification,'sexual_identification',DIRECTLY, ABOVE),
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
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
#Number of households whose prevention duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P1']: #only transforming tab P1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        prevention_duty_ended = tab.excel_ref('E3').expand(RIGHT)
        accomodation = tab.excel_ref('E4').expand(RIGHT)
        observations = tab.excel_ref('E5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(prevention_duty_ended,'prevention_duty_ended',DIRECTLY, ABOVE),
            HDim(accomodation,'accomodation',DIRECTLY, ABOVE),
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
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
#Number of households whose prevention duty ended by type of accommodation secured England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P2']: #only transforming tab P2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
        
        prevention_duty_ended_accomodation_secured = tab.excel_ref('D3').expand(RIGHT)
        prs_and_srs = tab.excel_ref('D4').expand(RIGHT)
        tenancy_type = tab.excel_ref('D5').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(tenancy_type, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(prevention_duty_ended_accomodation_secured,'prevention_duty_ended_accomodation_secured',DIRECTLY, ABOVE),
            HDim(prs_and_srs,'prs_and_srs',DIRECTLY, ABOVE),
            HDim(tenancy_type,'tenancy_type',DIRECTLY, ABOVE),
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
#Sheet = A8
df.drop(['ethnicgroup', 'breakdown_of_ethnicgroup'], axis=1, inplace=True)
#Sheet = A10
df.drop(['employment_status'],axis=1, inplace=True)
#Sheet = A12
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = P1
df.drop(['prevention_duty_ended', 'accomodation'], axis=1, inplace=True)

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
#Main prevention activity that resulted in accommodation secured for households at end of prevention duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P3']: #only transforming tab P3 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        type_of_secured_accomodation = tab.excel_ref('D3').expand(RIGHT)
        observations = tab.excel_ref('D4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(type_of_secured_accomodation,'type_of_secured_accomodation',DIRECTLY, ABOVE),
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


df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# Household type of households with accommodation secured at end of prevention duty England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['P5']: #only transforming tab P5 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")

        accomodation_secured_at_end_of_prevention_duty = tab.excel_ref('D3').expand(RIGHT)
        gender = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('D5').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(accomodation_secured_at_end_of_prevention_duty,'accomodation_secured_at_end_of_prevention_duty',DIRECTLY, ABOVE),
            HDim(gender,'gender',DIRECTLY, ABOVE),
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

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df

# +
# Number of households whose relief duty ended by reason for duty end England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R1']: #only transforming tab R1 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")

        end_of_relief_duty = tab.excel_ref('D3').expand(RIGHT)
        observations = tab.excel_ref('D4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(end_of_relief_duty,'end_of_relief_duty',DIRECTLY, ABOVE),
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


df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df
# +
# Number of households whose relief duty ended by type of accommodation secured England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R2']: #only transforming tab R2 for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(remove_notes, fname= tab.name + "PREVIEW.html")
        
        accomodation_secured_at_end_of_relief_duty = tab.excel_ref('D3').expand(RIGHT)
        break_down = tab.excel_ref('D4').expand(RIGHT)
        break_down_of_PRS_SRS = tab.excel_ref('D5').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(ons_geo,'ONS Geography Code',DIRECTLY,LEFT),
            HDim(period,'Period',CLOSEST,ABOVE),
            HDim(accomodation_secured_at_end_of_relief_duty,'accomodation_secured_at_end_of_relief_duty',DIRECTLY, ABOVE),
            HDim(break_down,'break_down',DIRECTLY, ABOVE),
            HDim(break_down_of_PRS_SRS,'break_down_of_PRS_SRS',DIRECTLY,ABOVE),
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

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
df["Period"]= df["Period"].str.split(",", n = 1, expand = True)[1]
df


# +
# Main relief activity that resulted in accommodation secured for households at end of relief duty by local authority England

for tab in tabs:
    columns=['TO DO']
    trace.start(datasetTitle, tab, columns, original_tabs.downloadURL)
    if tab.name in ['R3_']: #only transforming tab R3_ for now
        print(tab.name)
              
        remove_notes = tab.filter(contains_string('Notes')).shift(LEFT).expand(DOWN).expand(RIGHT)
        ons_geo = tab.excel_ref('A3').fill(DOWN).is_not_blank() - remove_notes # "-" suppressed in geography code to be processed in stage-2 transformation
        period = tab.excel_ref('A1').is_not_blank() #period can be extracted from this cell 
        sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        accomodation_secured = tab.excel_ref('D3').expand(RIGHT)
        observations = tab.excel_ref('D4').expand(DOWN).expand(RIGHT).is_not_blank() - remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
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

# -


