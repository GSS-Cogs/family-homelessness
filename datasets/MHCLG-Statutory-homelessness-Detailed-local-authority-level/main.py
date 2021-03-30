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
df["Period"]= df["Period"].str.split(",", n = -1, expand = True)[3]

df.drop(['temp_assessment_duty_type_1', 'temp_assessment_duty_type_2', 'temp_assessment_duty_type_3'], axis=1, inplace=True)
#Check the outputs of the temp column

df
