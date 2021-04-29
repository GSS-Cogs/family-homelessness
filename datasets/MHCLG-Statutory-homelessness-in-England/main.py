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
# scraper.select_dataset(latest=True) 
scraper 
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
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
df
# -

#Number of households owed a prevention duty by reason for threat of loss, of last settled home England
for tab in tabs:
    columns=['Contents']
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
df = trace.combine_and_trace(datasetTitle, "combined_dataframe")
#Sheet = "A1"
df.drop(['initial_assessment', 'duty_owed', 'section_21'], axis=1, inplace=True)
df

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
df

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
df     

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
df

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
df

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
df
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
df       


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
df       
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
df


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
df
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
df
# -



