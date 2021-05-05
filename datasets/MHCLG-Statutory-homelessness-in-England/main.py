# -*- coding: utf-8 -*-
# # MHCLG Statutory homelessness in England 

from gssutils import * 
import json 
import pandas as pd
import numpy as np 
from io import BytesIO
import pyexcel
import messytables

trace = TransformTrace()
df = pd.DataFrame()
cubes = Cubes("info.json")
info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

# +
#### Add transformation script here #### 

scraper = Scraper(landingPage)  
scraper 
scraper.dataset.family = info['families']
# -
# get only the distribution which we need
distribution = scraper.distribution(latest = True)


distribution

# convert the isolated distribution ODS in to XLS
with distribution.open() as ods_obj:
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


datasetTitle = distribution.title
datasetTitle

# get the tab names to validate with ODS
for tab in tabs:
    print(tab.name)

# +
#Number of households by initial assessment of homelessness circumstances and needs England

for tab in tabs:
    columns=['Contents']
#     columns=['quarter', 'period', 'initial_assessment', 'duty_owed', 'section_21']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A1']: #only transforming tab A1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
    
        initial_assessment = tab.excel_ref('D3').expand(RIGHT)
        duty_owed = tab.excel_ref('D4').expand(RIGHT)
        section_21 = tab.excel_ref('D5').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(RIGHT).expand(DOWN)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(initial_assessment,'initial_assessment',DIRECTLY, ABOVE),
            HDim(duty_owed,'duty_owed',DIRECTLY, ABOVE),
            HDim(section_21,'section_21',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
# df
# pd.DataFrame(df).to_csv("A1-output.csv")

# +
# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

# +
# # cubes.add_cube(scraper, df.drop_duplicates(), distribution.title)
# pd.DataFrame(df).to_excel("output.xlsx")

# +
# cubes.output_all()
# -

#Number of households owed a prevention duty by reason for threat of loss, of last settled home England
for tab in tabs:
    columns=['Contents']
#     columns=['quarter', 'period', 'prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A2P']: #only transforming tab A2P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
    
        prevention_duty = tab.excel_ref('D3').expand(RIGHT)
        tenancy_type = tab.excel_ref('D4').expand(RIGHT)
        reasons_for_breach = tab.excel_ref('D5').expand(RIGHT)
        reasons_for_rent_arrears = tab.excel_ref('D6').expand(RIGHT)
        observations = tab.excel_ref('D7').expand(RIGHT).expand(DOWN)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(prevention_duty,'prevention_duty',DIRECTLY, ABOVE),
            HDim(tenancy_type,'tenancy_type',DIRECTLY, ABOVE),
            HDim(reasons_for_breach,'reasons_for_breach',DIRECTLY, ABOVE),
            HDim(reasons_for_rent_arrears,'reasons_for_rent_arrears',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
# df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
# df
# pd.DataFrame(df).to_csv("A2P-output.csv")

# +
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

# +
# df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)

# +
# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)

# +
# pd.DataFrame(df).to_excel("output.xlsx")
# cubes.add_cube(scraper, df.drop_duplicates(), distribution.title)

# +
# cubes.output_all()
# -

#Number of households owed a relief duty by reason for loss, of last settled home England
for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A2R']: #only transforming tab A2R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B7').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")

        relief_prevention_duty = tab.excel_ref('D3').expand(RIGHT)
        relief_tenancy_type = tab.excel_ref('D4').expand(RIGHT)
        relief_reasons_for_breach = tab.excel_ref('D5').expand(RIGHT)
        relief_reasons_for_rent_arrears = tab.excel_ref('D6').expand(RIGHT)
        observations = tab.excel_ref('D7').expand(RIGHT).expand(DOWN)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(relief_prevention_duty,'relief_prevention_duty',DIRECTLY, ABOVE),
            HDim(relief_tenancy_type,'relief_tenancy_type',DIRECTLY, ABOVE),
            HDim(relief_reasons_for_breach,'relief_reasons_for_breach',DIRECTLY, ABOVE),
            HDim(relief_reasons_for_rent_arrears,'relief_reasons_for_rent_arrears',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A2R-output.csv")

# +
# Number of households owed a homelessness duty by support needs of household England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A3']: #only transforming tab A3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(quarter, fname= tab.name + "PREVIEW.html")
    
        total_households_with_supportneeds = tab.excel_ref('D2').expand(RIGHT)
        households_with_one_supportneeds = tab.excel_ref('D3').expand(RIGHT)
        households_with_two_supportneeds = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(total_households_with_supportneeds,'total_households_with_supportneeds',DIRECTLY, ABOVE),
            HDim(households_with_one_supportneeds,'households_with_one_supportneeds',DIRECTLY, ABOVE),
            HDim(households_with_two_supportneeds,'households_with_two_supportneeds',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A3-output.csv")

# +
#Number of households owed a prevention duty by accommodation at time of application England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A4P']: #only transforming tab A4P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
    
        rented_sector = tab.excel_ref('D3').expand(RIGHT)
        prs_srs = tab.excel_ref('D4').expand(RIGHT)
        breakdown_of_prs_srs = tab.excel_ref('D5').expand(RIGHT)
        observations = tab.excel_ref('D7').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(rented_sector,'rented_sector',DIRECTLY, ABOVE),
            HDim(prs_srs,'prs_srs',DIRECTLY, ABOVE),
            HDim(breakdown_of_prs_srs,'breakdown_of_prs_srs',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A4P-output.csv")

# +
#Number of households owed a relief duty by accommodation at time of application England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A4R']: #only transforming tab A4R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        accomodation_during_application = tab.excel_ref('D3').expand(RIGHT)
        breakdown_of_accomodation = tab.excel_ref('D4').expand(RIGHT)
        accomodation_type = tab.excel_ref('D5').expand(RIGHT)
        observations = tab.excel_ref('D7').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(accomodation_during_application,'accomodation_during_application',DIRECTLY, ABOVE),
            HDim(breakdown_of_accomodation,'breakdown_of_accomodation',DIRECTLY, ABOVE),
            HDim(accomodation_type,'accomodation_type',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A4R-output.csv")

# +
#Number of households owed a prevention duty by household composition England
#The columns with % needs to be filtered

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A5P']: #only transforming tab A5P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")

        household_composition = tab.excel_ref('D3').expand(RIGHT)
        gender = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('D7').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(household_composition,'household_composition',DIRECTLY, ABOVE),
            HDim(gender,'gender',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A5P-output.csv")
# +
# Number of households owed a relief duty by household composition England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A5R']: #only transforming tab A5R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(remove_notes, fname= tab.name + "PREVIEW.html")

        relief_duty_household_composition = tab.excel_ref('D3').expand(RIGHT)
        relief_duty_gender = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('D7').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(household_composition, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(relief_duty_household_composition,'relief_duty_household_composition',DIRECTLY, ABOVE),
            HDim(relief_duty_gender,'relief_duty_gender',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition', 'gender'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A5R-output.csv")


# +
#Age of main applicants assessed as owed a prevention or relief duty by local authority England
#Percentage in age and observations column needs to be cleansed

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A6']: #only transforming tab A6 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B5').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(quarter, fname= tab.name + "PREVIEW.html")

        age_of_applicants = tab.excel_ref('D3').expand(RIGHT)
        observations = tab.excel_ref('D5').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(age_of_applicants,'age_of_applicants',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition', 'gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A6-output.csv")
# +
# Number of households assessed as a result of a referral, including under the Duty to Refer England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A7']: #only transforming tab A7 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        total_referred_households = tab.excel_ref('D3').expand(RIGHT)
        total_households_duty_refer2 = tab.excel_ref('D4').expand(RIGHT)
        breakdown_total_households_duty_refer2 = tab.excel_ref('D5').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(total_referred_households,'total_referred_households',DIRECTLY, ABOVE),
            HDim(total_households_duty_refer2,'total_households_duty_refer2',DIRECTLY, ABOVE),
            HDim(breakdown_total_households_duty_refer2,'breakdown_total_households_duty_refer2',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition', 'gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A7-output.csv")


# +
#Ethnicity of main applicants assessed as owed a prevention or relief duty by local authority England
#Percentage in observations column needs to be cleansed

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A8']: #only transforming tab A8 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = tab.excel_ref('B6').expand(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes 
#         sheet_name = tab.name
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
    
        ethnicity_of_main_applicants = tab.excel_ref('D3').expand(RIGHT)
        breakdown_of_ethnicity_of_main_applicants = tab.excel_ref('D4').expand(RIGHT)
        observations = tab.excel_ref('D6').expand(DOWN).expand(RIGHT)-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(ethnicity_of_main_applicants,'ethnicity_of_main_applicants',DIRECTLY, ABOVE),
            HDim(breakdown_of_ethnicity_of_main_applicants,'breakdown_of_ethnicity_of_main_applicants',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition', 'gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
#Sheet = "A7"
df.drop(['total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A8-output.csv")
# +
#Employment status of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A10']: #only transforming tab A10 for now
        print(tab.name)
        
        cell = tab.excel_ref('A1')
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = cell.shift(1, 4).fill(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes
#         savepreviewhtml(quarter, fname= tab.name + "PREVIEW.html")
        
        prevention_or_relief_duty = tab.filter('Total owed a prevention or relief duty').expand(RIGHT)
        observations = prevention_or_relief_duty.fill(DOWN).expand(RIGHT).is_not_blank()
#         savepreviewhtml(observations, fname = tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(prevention_or_relief_duty,'prevention_or_relief_duty',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition', 'gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
#Sheet = "A7"
df.drop(['total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2'], axis=1, inplace=True)
#Sheet = "A8"
df.drop(['ethnicity_of_main_applicants', 'breakdown_of_ethnicity_of_main_applicants'], axis=1, inplace=True)
# df
pd.DataFrame(df).to_csv("A10-output.csv")
# +
# Number of households owed a homelessness duty by sexual identification of lead applicant England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A12']: #only transforming tab A12 for now
        print(tab.name)
        
        cell = tab.excel_ref('A1')
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = cell.shift(1, 4).fill(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes
#         savepreviewhtml(quarter, fname= tab.name + "PREVIEW.html")

        sexual_identification = tab.filter("Total owed a prevention or relief duty").expand(RIGHT)
        observations = sexual_identification.waffle(quarter)
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")

        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(sexual_identification, 'sexual_identification',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition', 'gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
#Sheet = "A7"
df.drop(['total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2'], axis=1, inplace=True)
#Sheet = "A8"
df.drop(['ethnicity_of_main_applicants', 'breakdown_of_ethnicity_of_main_applicants'], axis=1, inplace=True)
#Sheet = "A10"
df.drop(['prevention_or_relief_duty'], axis=1, inplace=True)
pd.DataFrame(df).to_csv("A12-output.csv")

# +
#Number of households whose prevention duty ended by reason for duty end England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P1']: #only transforming tab P1 for now
        print(tab.name)
        
        cell = tab.excel_ref('A1')
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = cell.shift(1, 4).fill(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        prevention_duty_ended = tab.filter("Total number of households whose prevention duty ended1").expand(RIGHT)
        moved_or_stayed_accomodation = prevention_duty_ended.shift(DOWN).expand(RIGHT)
        observations = moved_or_stayed_accomodation.waffle(quarter).is_not_blank()
#         savepreviewhtml(moved_or_stayed_accomodation, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(prevention_duty_ended, 'prevention_duty_ended',DIRECTLY, ABOVE),
            HDim(moved_or_stayed_accomodation, 'moved_or_stayed_accomodation',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition','gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
#Sheet = "A7"
df.drop(['total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2'], axis=1, inplace=True)
#Sheet = "A8"
df.drop(['ethnicity_of_main_applicants', 'breakdown_of_ethnicity_of_main_applicants'], axis=1, inplace=True)
#Sheet = "A10"
df.drop(['prevention_or_relief_duty'], axis=1, inplace=True)
#Sheet = "A12"
df.drop(['sexual_identification'], axis=1, inplace=True)
pd.DataFrame(df).to_csv("P1-output.csv")
# +
#Number of households whose prevention duty ended by type of accommodation secured England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P2']: #only transforming tab P2 for now
        print(tab.name)
        
        cell = tab.excel_ref('A1')
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        quarter = cell.shift(1, 5).fill(DOWN)-remove_notes
        period = quarter.shift(LEFT).is_not_blank()-remove_notes
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        
        household_type_and_composition = tab.filter("Total number of households whose prevention duty ended with accommodation secured").expand(RIGHT)
        prs_srs_1 = household_type_and_composition.shift(DOWN).expand(RIGHT)
        breakdown_of_prs_srs_1 = prs_srs.shift(DOWN).expand(RIGHT)
        observations = breakdown_of_prs_srs.fill(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()-remove_notes
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(household_type_and_composition, 'household_type_and_composition', DIRECTLY,ABOVE),
            HDim(prs_srs_1, 'prs_srs_1', DIRECTLY, ABOVE),
            HDim(breakdown_of_prs_srs_1, 'breakdown_of_prs_srs_1', DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition','gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
#Sheet = "A7"
df.drop(['total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2'], axis=1, inplace=True)
#Sheet = "A8"
df.drop(['ethnicity_of_main_applicants', 'breakdown_of_ethnicity_of_main_applicants'], axis=1, inplace=True)
#Sheet = "A10"
df.drop(['prevention_or_relief_duty'], axis=1, inplace=True)
#Sheet = "A12"
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = "P1"
df.drop(['prevention_duty_ended', 'moved_or_stayed_accomodation'], axis=1, inplace=True)
pd.DataFrame(df).to_csv("P2-output.csv")
# -

# Main prevention activity that resulted in accommodation secured for households at end of prevention duty by local authority England
for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P3']: #only transforming tab A10 for now
        print(tab.name)

        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_with_secured_accomodation = tab.filter("Total number of households where prevention duty ended with accommodation secured").expand(RIGHT)
        observations = household_with_secured_accomodation.fill(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()

        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,ABOVE),
            HDim(household_with_secured_accomodation, 'household_with_secured_accomodation', DIRECTLY,ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
#Sheet = "A2P"
df.drop(['prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A2R"
df.drop(['relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears'], axis=1, inplace=True)
#Sheet = "A3"
df.drop(['total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds'], axis=1, inplace=True)
#Sheet = "A4P"
df.drop(['rented_sector', 'prs_srs', 'breakdown_of_prs_srs'], axis=1, inplace=True)
#Sheet = "A4R"
df.drop(['accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type'], axis=1, inplace=True)
#Sheet = "A5P"
df.drop(['household_composition','gender'], axis=1, inplace=True)
#Sheet = "A5R"
df.drop(['relief_duty_household_composition', 'relief_duty_gender'], axis=1, inplace=True)
#Sheet = "A6"
df.drop(['age_of_applicants'], axis=1, inplace=True)
#Sheet = "A7"
df.drop(['total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2'], axis=1, inplace=True)
#Sheet = "A8"
df.drop(['ethnicity_of_main_applicants', 'breakdown_of_ethnicity_of_main_applicants'], axis=1, inplace=True)
#Sheet = "A10"
df.drop(['prevention_or_relief_duty'], axis=1, inplace=True)
#Sheet = "A12"
df.drop(['sexual_identification'], axis=1, inplace=True)
#Sheet = "P1"
df.drop(['prevention_duty_ended', 'moved_or_stayed_accomodation'], axis=1, inplace=True)
#Sheet = 'P2'
df.drop(['household_type_and_composition', 'prs_srs_1', 'breakdown_of_prs_srs_1'], axis=1, inplace=True)
pd.DataFrame(df).to_csv("P3-output.csv")



# +
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

# +
# df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

# +
# df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
# cubes.add_cube(scraper, df.drop_duplicates(), distribution.title)


# +
# cubes.add_cube(scraper, df.drop_duplicates(), distribution.title)
# pd.DataFrame(df).to_excel("df-output.xlsx")

# +
# cubes.output_all()

# +
# trace.render("spec_v1.html")
