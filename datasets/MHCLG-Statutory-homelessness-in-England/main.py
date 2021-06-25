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
    columns=['quarter', 'period', 'initial_assessment', 'duty_owed', 'section_21']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A1']: #only transforming tab A1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        initial_assessment = tab.filter("Total initial assessments1").expand(RIGHT)
        duty_owed = initial_assessment.shift(DOWN).expand(RIGHT)
        section_21 = duty_owed.shift(DOWN).expand(RIGHT)
        observations = section_21.fill(DOWN).expand(RIGHT).is_not_blank()
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(initial_assessment,'initial_assessment',DIRECTLY, ABOVE),
            HDim(duty_owed,'duty_owed',DIRECTLY, ABOVE),
            HDim(section_21,'section_21',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# -

#Number of households owed a prevention duty by reason for threat of loss, of last settled home England
for tab in tabs:
    columns=['quarter', 'period', 'prevention_duty', 'tenancy_type', 'reasons_for_breach', 'reasons_for_rent_arrears']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A2P']: #only transforming tab A2P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_duty = tab.filter("Total owed a prevention duty1").expand(RIGHT)
        tenancy_type = prevention_duty.shift(DOWN).expand(RIGHT)
        reasons_for_breach = tenancy_type.shift(DOWN).expand(RIGHT)
        reasons_for_rent_arrears = reasons_for_breach.shift(DOWN).expand(RIGHT)
        observations = reasons_for_rent_arrears.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
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

#Number of households owed a relief duty by reason for loss, of last settled home England
for tab in tabs:
    columns=['quarter', 'period', 'relief_prevention_duty', 'relief_tenancy_type', 'relief_reasons_for_breach', 'relief_reasons_for_rent_arrears']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A2R']: #only transforming tab A2R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        relief_prevention_duty = tab.filter("Total owed a relief duty1").expand(RIGHT)
        relief_tenancy_type = relief_prevention_duty.shift(DOWN).expand(RIGHT)
        relief_reasons_for_breach = relief_tenancy_type.shift(DOWN).expand(RIGHT)
        relief_reasons_for_rent_arrears = relief_reasons_for_breach.shift(DOWN).expand(RIGHT)
        observations = relief_reasons_for_rent_arrears.fill(DOWN).expand(RIGHT).is_not_blank()
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
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

# +
# Number of households owed a homelessness duty by support needs of household England

for tab in tabs:
    columns=['quarter', 'period', 'total_households_with_supportneeds', 'households_with_one_supportneeds', 'households_with_two_supportneeds']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A3']: #only transforming tab A3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        total_households_with_supportneeds = tab.filter("Number of households").expand(RIGHT).is_not_blank()
        households_with_one_supportneeds = tab.filter("Households with no support needs1").expand(RIGHT)
        households_with_two_supportneeds = households_with_one_supportneeds.shift(DOWN).expand(RIGHT)
        observations = households_with_two_supportneeds.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(total_households_with_supportneeds,'total_households_with_supportneeds',CLOSEST, LEFT),
            HDim(households_with_one_supportneeds,'households_with_one_supportneeds',DIRECTLY, ABOVE),
            HDim(households_with_two_supportneeds,'households_with_two_supportneeds',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households owed a prevention duty by accommodation at time of application England

for tab in tabs:
    columns=['quarter', 'period', 'rented_sector', 'prs_srs', 'breakdown_of_prs_srs']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A4P']: #only transforming tab A4P for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        rented_sector = tab.filter("Total owed a prevention duty1").expand(RIGHT)
        prs_srs = rented_sector.shift(DOWN).expand(RIGHT)
        breakdown_of_prs_srs = prs_srs.shift(DOWN).expand(RIGHT)
        observations = breakdown_of_prs_srs.fill(DOWN).expand(RIGHT).is_not_blank()
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
            HDim(period,'period',CLOSEST,LEFT),
            HDim(rented_sector,'rented_sector',DIRECTLY, ABOVE),
            HDim(prs_srs,'prs_srs',DIRECTLY, ABOVE),
            HDim(breakdown_of_prs_srs,'breakdown_of_prs_srs',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households owed a relief duty by accommodation at time of application England

for tab in tabs:
    columns=['quarter', 'period', 'accomodation_during_application', 'breakdown_of_accomodation', 'accomodation_type']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A4R']: #only transforming tab A4R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        accomodation_during_application = tab.filter("Total owed a relief duty1").expand(RIGHT)
        breakdown_of_accomodation = accomodation_during_application.shift(DOWN).expand(RIGHT)
        accomodation_type = breakdown_of_accomodation.shift(DOWN).expand(RIGHT)
        observations = accomodation_type.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(accomodation_during_application,'accomodation_during_application',DIRECTLY, ABOVE),
            HDim(breakdown_of_accomodation,'breakdown_of_accomodation',DIRECTLY, ABOVE),
            HDim(accomodation_type,'accomodation_type',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households owed a prevention duty by household composition England
#The columns with % needs to be filtered

for tab in tabs:
    columns=['quarter', 'period', 'household_composition', 'gender']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A5P']: #only transforming tab A5P for now
        print(tab.name)
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_composition = tab.filter("Total owed a prevention duty").expand(RIGHT)
        gender = household_composition.shift(DOWN).expand(RIGHT)
        observations = gender.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_composition,'household_composition',DIRECTLY, ABOVE),
            HDim(gender,'gender',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# +
# Number of households owed a relief duty by household composition England

for tab in tabs:
    columns=['quarter', 'period', 'relief_duty_household_composition', 'relief_duty_gender']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A5R']: #only transforming tab A5R for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        relief_duty_household_composition = tab.filter("Total owed a relief duty").expand(RIGHT)
        relief_duty_gender = relief_duty_household_composition.shift(DOWN)
        observations = relief_duty_gender.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(relief_duty_household_composition,'relief_duty_household_composition',DIRECTLY, ABOVE),
            HDim(relief_duty_gender,'relief_duty_gender',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())


# +
#Age of main applicants assessed as owed a prevention or relief duty by local authority England
#Percentage in age and observations column needs to be cleansed

for tab in tabs:
    columns=['quarter', 'period', 'age_of_applicants']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A6']: #only transforming tab A6 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        age_of_applicants = tab.filter("Total owed a prevention or relief duty").expand(RIGHT)
        observations = age_of_applicants.fill(DOWN).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(age_of_applicants,'age_of_applicants',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# -
# Number of households assessed as a result of a referral, including under the Duty to Refer England
for tab in tabs:
    columns=['quarter', 'period', 'total_referred_households', 'total_households_duty_refer2', 'breakdown_total_households_duty_refer2']    
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A7']: #only transforming tab A7 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        total_referred_households = tab.filter("Total households assessed as a result of a referral1").expand(RIGHT)
        total_households_duty_refer2 = total_referred_households.shift(DOWN)
        breakdown_total_households_duty_refer2 = total_households_duty_refer2.shift(DOWN)
        observations = breakdown_total_households_duty_refer2.fill(DOWN).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(total_referred_households,'total_referred_households',DIRECTLY, ABOVE),
            HDim(total_households_duty_refer2,'total_households_duty_refer2',DIRECTLY, ABOVE),
            HDim(breakdown_total_households_duty_refer2,'breakdown_total_households_duty_refer2',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())


# +
#Ethnicity of main applicants assessed as owed a prevention or relief duty by local authority England
#Percentage in observations column needs to be cleansed

for tab in tabs:
    columns=['quarter', 'period', 'ethnicity_of_main_applicants', 'breakdown_of_ethnicity_of_main_applicants']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A8']: #only transforming tab A8 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        ethnicity_of_main_applicants = tab.filter("Total owed a prevention or relief duty1").expand(RIGHT)
        breakdown_of_ethnicity_of_main_applicants = ethnicity_of_main_applicants.shift(DOWN)
        observations = breakdown_of_ethnicity_of_main_applicants.fill(DOWN).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(ethnicity_of_main_applicants,'ethnicity_of_main_applicants',DIRECTLY, ABOVE),
            HDim(breakdown_of_ethnicity_of_main_applicants,'breakdown_of_ethnicity_of_main_applicants',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# +
#Employment status of main applicants assessed as owed a prevention or relief duty by local authority England

for tab in tabs:
    columns = ['quarter', 'period', 'prevention_or_relief_duty']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A10']: #only transforming tab A10 for now
        print(tab.name)
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_or_relief_duty = tab.filter("Total owed a prevention or relief duty").expand(RIGHT)
        observations = prevention_or_relief_duty.fill(DOWN).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(prevention_or_relief_duty,'prevention_or_relief_duty',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# +
# Number of households owed a homelessness duty by sexual identification of lead applicant England

for tab in tabs:
    columns = ['quarter', 'period', 'sexual_identification']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A12']: #only transforming tab A12 for now
        print(tab.name)
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        sexual_identification = tab.filter("Total owed a prevention or relief duty").expand(RIGHT)
        observations = sexual_identification.fill(DOWN).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(sexual_identification, 'sexual_identification',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households whose prevention duty ended by reason for duty end England

for tab in tabs:
    columns = ['quarter', 'period', 'prevention_duty_ended', 'moved_or_stayed_accomodation']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P1']: #only transforming tab P1 for now
        print(tab.name)
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        prevention_duty_ended = tab.filter("Total number of households whose prevention duty ended1").expand(RIGHT)
        moved_or_stayed_accomodation = prevention_duty_ended.shift(DOWN)
        observations = moved_or_stayed_accomodation.fill(DOWN).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(prevention_duty_ended, 'prevention_duty_ended',DIRECTLY, ABOVE),
            HDim(moved_or_stayed_accomodation, 'moved_or_stayed_accomodation',DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# +
#Number of households whose prevention duty ended by type of accommodation secured England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P2']: #only transforming tab P2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_type_and_composition = tab.filter("Total number of households whose prevention duty ended with accommodation secured").expand(RIGHT)
        prs_srs_1 = tab.filter("Total PRS").expand(RIGHT).is_not_blank()
        breakdown_of_prs_srs_1 = tab.filter("Self-contained").shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT)
        observations = breakdown_of_prs_srs_1.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(observations, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_type_and_composition, 'household_type_and_composition', DIRECTLY,ABOVE),
            HDim(prs_srs_1, 'prs_srs_1', CLOSEST, LEFT),
            HDim(breakdown_of_prs_srs_1, 'breakdown_of_prs_srs_1', DIRECTLY, ABOVE),
            #HDimConst("sheet_name", sheet_name) #Might be handy to have for post processing when other tabs are running also 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# -

# Main prevention activity that resulted in accommodation secured for households at end of prevention duty by local authority England
for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P3']: #only transforming tab P3 for now
        print(tab.name)

        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_with_secured_accomodation = tab.filter("Total number of households where prevention duty ended with accommodation secured").expand(RIGHT)
        observations = household_with_secured_accomodation.fill(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()

        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_with_secured_accomodation, 'household_with_secured_accomodation', DIRECTLY,ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Household type of households with accommodation secured at end of prevention duty England
#Percentage in observations column needs to be cleansed

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['P5']: #only transforming tab P5 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_secured_accomodation_at_end_preventionduty = tab.filter("Total with accommodation secured at end of prevention duty").expand(RIGHT)
        breakdown_of_household_secured_accomodation_at_end_preventionduty = household_secured_accomodation_at_end_preventionduty.shift(DOWN)
        observations = breakdown_of_household_secured_accomodation_at_end_preventionduty.fill(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_secured_accomodation_at_end_preventionduty, 'household_secured_accomodation_at_end_preventionduty', DIRECTLY,ABOVE),
            HDim(breakdown_of_household_secured_accomodation_at_end_preventionduty, 'breakdown_of_household_secured_accomodation_at_end_preventionduty', DIRECTLY,ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households whose relief duty ended by reason for duty end England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['R1']: #only transforming tab R1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_relief_duty_ended = tab.filter("Local connection referral accepted by other LA").shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT)
        observations = household_relief_duty_ended.fill(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_relief_duty_ended, 'household_relief_duty_ended', DIRECTLY,ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
# Number of households whose relief duty ended by type of accommodation secured England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['R2']: #only transforming tab R2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_relief_duty_ended_by_type_of_accommodation = tab.filter("Total number of households whose relief duty ended with  accommodation secured").expand(RIGHT)
        prs_srs_breakdown = household_relief_duty_ended_by_type_of_accommodation.shift(DOWN).shift(DOWN).expand(RIGHT)
        observations = prs_srs_breakdown.fill(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_relief_duty_ended_by_type_of_accommodation, 'household_relief_duty_ended_by_type_of_accommodation', DIRECTLY,ABOVE),
            HDim(prs_srs_breakdown, 'prs_srs_breakdown', DIRECTLY, ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# +
# Main relief activity that resulted in accommodation secured for households at end of relief duty by local authority England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['R3_']: #only transforming tab R3_ for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        relief_duty_ended_with_accomodation_secured = tab.filter("Total number of households where relief duty ended with accommodation secured").expand(RIGHT)
        observations = relief_duty_ended_with_accomodation_secured.fill(DOWN).expand(RIGHT).is_not_blank()
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(relief_duty_ended_with_accomodation_secured, 'relief_duty_ended_with_accomodation_secured', DIRECTLY,ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())


# +
#Household type of households with accommodation secured at end of relief duty England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['R5']: #only transforming tab R3_ for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_inmate_combination = tab.filter("Total with accommodation secured at end of relief duty").expand(RIGHT)
        breakdown_of_inmate_combination = household_inmate_combination.shift(DOWN).shift(LEFT).fill(RIGHT).is_not_blank()
        observations = breakdown_of_inmate_combination.fill(DOWN).shift(LEFT).shift(LEFT).shift(LEFT).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname = tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_inmate_combination, 'household_inmate_combination', DIRECTLY, ABOVE),
            HDim(breakdown_of_inmate_combination, 'breakdown_of_inmate_combination', CLOSEST, LEFT), 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# +
#Number of households by decision on duty owed England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['MD1']: #only transforming tab MD1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_by_decision_duty_owed = tab.filter("Total main duty decisions for eligible households1").expand(RIGHT)
        observations = household_by_decision_duty_owed.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_by_decision_duty_owed, 'household_by_decision_duty_owed', DIRECTLY, ABOVE), 
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households whose main duty ended by reason for duty end England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['MD2']: #only transforming tab MD2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_main_duty_ended = tab.filter("Total households whose main duty ended1").expand(RIGHT)
        accepted_refused = household_main_duty_ended.shift(DOWN).expand(RIGHT)
        observations = accepted_refused.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_main_duty_ended, 'household_main_duty_ended', DIRECTLY, ABOVE), 
            HDim(accepted_refused, 'accepted_refused', DIRECTLY, ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())  


# +
#Number of households owed a main duty by priority need England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['MD3']: #only transforming tab MD3 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_owed_priority = tab.filter("Total households owed a main duty1").expand(RIGHT)
        vulnerable_household = household_owed_priority.shift(DOWN).expand(RIGHT)
        observations = vulnerable_household.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_owed_priority, 'household_owed_priority', DIRECTLY, ABOVE), 
            HDim(vulnerable_household, 'vulnerable_household', DIRECTLY, ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households in temporary accommodation at the end of quarter by type of TA provided England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['TA1']: #only transforming tab TA1 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_in_temporary_accomodation = tab.filter("Total number of households in TA1,2,3").expand(RIGHT)
        household_occupants_breakdown = household_in_temporary_accomodation.shift(DOWN).expand(RIGHT)
        observations = household_occupants_breakdown.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_in_temporary_accomodation, 'household_in_temporary_accomodation', DIRECTLY, ABOVE), 
            HDim(household_occupants_breakdown, 'household_occupants_breakdown', DIRECTLY, ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())

# +
#Number of households in temporary accommodation at the end of quarter by household composition England

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['TA2']: #only transforming tab TA2 for now
        print(tab.name)
        
        remove_notes = tab.filter(contains_string('Notes')).expand(DOWN).expand(RIGHT)
        household_composition_by_end_of_quarter = tab.filter("Total number of households in TA1,2,3").expand(RIGHT)
        gender_breakdown = household_composition_by_end_of_quarter.shift(DOWN).expand(RIGHT)
        observations = gender_breakdown.fill(DOWN).expand(RIGHT).is_not_blank()-remove_notes
        unwanted = observations.shift(LEFT).shift(LEFT).fill(RIGHT)
        quarter = unwanted.shift(LEFT)-unwanted
        period = quarter.shift(LEFT).is_not_blank()
#         savepreviewhtml(period, fname= tab.name + "PREVIEW.html")
        dimensions = [
            HDim(quarter,'quarter',DIRECTLY,LEFT),
#             HDim(period,'period',CLOSEST,LEFT),
            HDim(household_composition_by_end_of_quarter, 'household_composition_by_end_of_quarter', DIRECTLY, ABOVE), 
            HDim(gender_breakdown, 'gender_breakdown', DIRECTLY, ABOVE),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        savepreviewhtml(tidy_sheet, fname= tab.name + "PREVIEW.html")
        trace.with_preview(tidy_sheet)
        trace.store("combined_dataframe", tidy_sheet.topandas())
# -

df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

df.rename(columns={'OBS' : 'Value', 'DATAMARKER' : 'Marker'}, inplace=True)
# cubes.add_cube(scraper, df.drop_duplicates(), distribution.title)


# cubes.add_cube(scraper, df.drop_duplicates(), distribution.title)
pd.DataFrame(df).to_excel("df-output.xlsx")

# +
# cubes.output_all()

# +
# trace.render("spec_v1.html")
