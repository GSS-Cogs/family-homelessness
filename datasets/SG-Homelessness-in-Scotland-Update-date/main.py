# # SG Homelessness in Scotland  Update  date 

# NOTE FOR DM : 
#
# Please note this is only a stage one transform. For that reason the 5 dataframes produced have been outputted as only CSV's for now to aid a DM with their checks to produce a stage 2 spec. 
#
# The 5 outputs follow the structure detailed in the source spreadsheet found here https://www.gov.scot/binaries/content/documents/govscot/publications/statistics/2021/03/homelessness-scotland-update-30-september-2020/documents/tables-march-2021/tables-march-2021/govscot%3Adocument/tables-march-2021.xlsx
#
# The only data included in the transform is the raw data and excludes the values within each spreadsheet that can be derived, e.g. 'As a proportion of', 'As a percentage of'. 
#
# Temp scraper is also in use. 

# +
import json
import pandas as pd
from gssutils import *

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def month_format (date):
    if len(date)  == 10:
        return (date[5:7])
    else:
        return date

def year_format (date):
    if len(date)  >10:
        return right(date,4)
    else:
        return date

def date_time_government (date):
    if len(date)  == 4:
        return 'year/' + date
    elif len(date) == 6:
        return 'government-quarter/' + left(date,4) + '-' + right(date,2)
    elif len(date) == 7:
        return 'government-half/' + left(date,4) + '-' + right(date,2)
    else:
        return date
     
    
def date_time (date):
    if len(date)  == 4:
        return 'year/' + date
    elif len(date) == 6:
        return 'quarter/' + left(date,4) + '-' + right(date,2)
    else:
        return date
 

info = 'info.json'
cubes = Cubes(info)
trace = TransformTrace()
scraper = Scraper(seed=info)
# -

distribution = scraper.distribution(latest = True)
distribution.title = "Homelessness in Scotland: Update"
datasetTitle = distribution.title 
tabs = { tab.name: tab for tab in distribution.as_databaker() }

#Data will be split out into sperate outputs under the following;  
out = Path('out')
out.mkdir(exist_ok=True)
#SG - Homelessness Update - Applications
applications = ['Table 1', 'Table 2', 'Table 3', 'Table 4', 'Table 5', 'Table 6']
#SG - Homelessness Update - Assessments
assessments = ['Table 7', 'Table 8', 'Table 9', 'Table 10', 'Table 11', 'Table 12', 'Table 13']
#SG - Homelessness Update - Temporary  Accommadation 
temp_accomadation = ['Table 14', 'Table 15', 'Table 16', 'Table 17', 'Table 18', 'Table 19', 'Table 20', 'Table 21', 'Table 22', 'Table 23']
#SG - Homelessness Update - Outcomes 
outcomes = ['Table 24', 'Table 25', 'Table 26', 'Table 27', 'Table 28']
#SG - Homelessness Update - Covid
covid = ['Table 29', 'Table 30', 'Table 31', 'Table 32', 'Table 33']

for name, tab in tabs.items():
    remove_summary = tab.filter(contains_string('6-monthly summary')).expand(DOWN).expand(RIGHT) | tab.excel_ref('M4').expand(RIGHT).expand(DOWN)
    remove_proportion = tab.excel_ref('A5').expand(DOWN).filter(contains_string('Table ')).expand(DOWN).expand(RIGHT)

    if name in applications:
        columns = ['Period', 'Local Authority', 'Reason for Application', 'Failing to Maintain Accommodation reasons']
        trace.start(distribution.title, tab, columns, distribution.downloadURL)
        months = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - remove_summary
        year = months.shift(UP).is_not_blank()
        
        if right((name), 2) == ' 1' or right((name), 2) == ' 6': 
            geo = tab.excel_ref('A5').expand(DOWN).is_not_blank() - remove_proportion
            reason = tab.excel_ref('A1').is_not_blank()
            observations = geo.fill(RIGHT).is_not_blank() - remove_summary - remove_proportion
            
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(geo,'Local Authority',DIRECTLY,LEFT),
                HDim(reason, "Reason for Application", CLOSEST, ABOVE),
                HDimConst('Failing to Maintain Accommodation reasons', 'not-applicable'),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            trace.store("applications", tidy_sheet.topandas())
            
        elif right((name), 2) == ' 2' or right((name), 2) == ' 3': 
            remove = tab.excel_ref('A8').expand(DOWN).expand(RIGHT)
            reason = tab.excel_ref('A5').expand(DOWN).is_not_blank() - remove 
            observations = months.fill(DOWN).is_not_blank() - remove
            
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(reason, "Reason for Application", DIRECTLY, LEFT),
                HDimConst('Failing to Maintain Accommodation reasons', 'not-applicable'),
                HDimConst('Local Authority', 'Scotland')
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            trace.store("applications", tidy_sheet.topandas())
            
        elif right((name), 2) == ' 4':
            months = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove_summary
            year = months.shift(UP).is_not_blank()
            reason = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
            observations = months.fill(DOWN).is_not_blank()  - remove_proportion
            
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(reason, "Reason for Application", DIRECTLY, LEFT),
                HDimConst('Failing to Maintain Accommodation reasons', 'not-applicable'),
                HDimConst('Local Authority', 'Scotland')
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            trace.store("applications", tidy_sheet.topandas())
            
        elif right((name), 2) == ' 5': 
            months = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove_summary
            year = months.shift(UP).is_not_blank()
            remove = tab.excel_ref('A17').expand(DOWN).expand(RIGHT)
            reason = tab.excel_ref('A1').is_not_blank()
            failing = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove
            observations = months.fill(DOWN).is_not_blank()  - remove
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(reason, "Reason for Application", CLOSEST, LEFT),
                HDim(failing,'Failing to Maintain Accommodation reasons', DIRECTLY, LEFT),
                HDimConst('Local Authority', 'Scotland')
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            trace.store("applications", tidy_sheet.topandas())

    else: 
        continue

applications = trace.combine_and_trace(datasetTitle, "applications")
applications.rename(columns={'OBS' : 'Value','DATAMARKER' : 'Marker'}, inplace=True)
applications['Year'] = applications['Year'].astype(str).replace('\.0', '', regex=True)
applications['Months'] = applications['Months'].apply(lambda x: 'Q1' if 'Jan-March' in x or '03' in x else 
                                      ('Q2' if 'April-June' in x or '06' in x else 
                                       ('Q3' if 'July-Sept' in x or '09' in x else 
                                        ( 'Q4' if 'Oct-Dec' in x or '12' in x else x))))
applications['Period'] = applications['Year'] + applications['Months']
applications.drop(['Year', 'Months'], axis=1, inplace=True)
applications['Period'] =  applications["Period"].apply(date_time_government)
applications["Reason for Application"]= applications["Reason for Application"].str.split(': ',expand=True)[1]
applications.replace({'Reason for Application': {'Reasons\xa0for\xa0failing\xa0to\xa0maintain\xa0accommodation\xa0prior\xa0to\xa0application': 'Reasons for failing to maintain accommodation prior to application'}}, inplace=True)
applications.to_csv(out / 'applications.csv', index = False)
applications
for name, tab in tabs.items():
    remove_summary = tab.filter(contains_string('6-monthly summary')).expand(DOWN).expand(RIGHT) | tab.excel_ref('M4').expand(RIGHT).expand(DOWN)
    remove_proportion = tab.excel_ref('A5').expand(DOWN).filter(contains_string('Table ')).expand(DOWN).expand(RIGHT)

    if name in assessments:
        columns = ['Period', 'Local Authority', 'Assessment Decision', 'Property type from which the household became homeless', 'Household Type', 'Gender', 'Age', 'Ethnicity']
        trace.start(distribution.title, tab, columns, distribution.downloadURL)
        months = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove_summary
        year = months.shift(UP).is_not_blank()
        
        if right((name), 2) == ' 9': # Table 9 in different format, will do seperately 
            local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank() - remove_proportion
            date = tab.excel_ref('A1')
            assessment_decision = (tab.excel_ref('A4').expand(RIGHT).is_not_blank() | tab.excel_ref('B5').expand(RIGHT)) - tab.excel_ref('O4').expand(DOWN) 
            observations = local_authority.fill(RIGHT).is_not_blank() - tab.excel_ref('O4').expand(DOWN)
            dimensions = [
                HDim(date, "Months", CLOSEST, LEFT), 
                HDim(date, "Year", CLOSEST, LEFT),
                HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
                HDim(assessment_decision, "Assessment Decision", DIRECTLY, ABOVE),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            trace.store("assessments", tidy_sheet.topandas())
        else:
            observations = months.fill(DOWN).is_not_blank() - remove_proportion
            if right((name), 2) == ' 8':
                local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank() - remove_proportion
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("assessments", tidy_sheet.topandas())
            elif right((name), 2) == ' 7':
                assessment_decision = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(assessment_decision, "Assessment Decision", DIRECTLY, LEFT),
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("assessments", tidy_sheet.topandas())
            elif right((name), 2) == '10':
                property_type = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
                months = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - remove_summary
                year = months.shift(UP).is_not_blank()
                observations = months.fill(DOWN).is_not_blank() - remove_proportion
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(property_type, "Property Type", DIRECTLY, LEFT),
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("assessments", tidy_sheet.topandas())
            elif right((name), 2) == '11':
                #Will need spilt up to Household type and gender column 
                household_gender = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(household_gender, "Household Type", DIRECTLY, LEFT),
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("assessments", tidy_sheet.topandas())
            elif right((name), 2) == '12':
                gender = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
                age = tab.excel_ref('B4').expand(DOWN).is_not_blank() - remove_proportion
                
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(gender, "Gender", CLOSEST, ABOVE),
                    HDim(age, "Age", DIRECTLY, LEFT),
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("assessments", tidy_sheet.topandas())
            elif right((name), 2) == '13':
                ethnicity = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(ethnicity, "Ethnicity", DIRECTLY, LEFT),
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("assessments", tidy_sheet.topandas())
            else:
                continue        
    else: 
        continue

# +
assessments = trace.combine_and_trace(datasetTitle, "assessments").fillna('')
assessments.rename(columns={'OBS' : 'Value','DATAMARKER' : 'Marker'}, inplace=True)
assessments['Year'] = assessments['Year'].astype(str).replace('\.0', '', regex=True)
assessments['Year'] =  assessments["Year"].apply(year_format)
assessments['Months'] = assessments['Months'].apply(lambda x: 'Q4' if 'Jan-March' in x else 
                                      ('Q1' if 'April-June' in x else 
                                       ('Q2' if 'July-Sept' in x else 
                                        ( 'Q3' if 'Oct-Dec' in x else
                                         ('gH1' if 'April to September ' in x else x)))))
assessments['Period'] = assessments['Year'] + assessments['Months']
assessments.drop(['Year', 'Months'], axis=1, inplace=True)
assessments['Period'] =  assessments["Period"].apply(date_time_government)

assessments["Local Authority"] = assessments["Local Authority"].replace({'' : 'Scotland'})
assessments["Property Type"] = assessments["Property Type"].replace({'' : 'Unknown'})
#Using the House hold type column to populate gender column based on the value outputted 
assessments['Gender'] = assessments['Household Type'].apply(lambda x: 'Male' if 'Male' in x else 
                                      ('Female' if 'Female' in x else 
                                       ('Total' if 'Total' in x else
                                        ('Unknown' if 'Couple' in x or 'Other' in x else
                                        'All' if 'All' in x else x))))
assessments['Household Type'] = assessments['Household Type'].str.replace(' - Male' , '')
assessments['Household Type'] = assessments['Household Type'].str.replace(' - Female' , '')
assessments['Household Type'] = assessments['Household Type'].str.replace(' Male' , '')
assessments['Household Type'] = assessments['Household Type'].str.replace(' Female' , '')
assessments["Household Type"] = assessments["Household Type"].replace({'' : 'All'})
assessments["Gender"] = assessments["Gender"].replace({'' : 'All'})
assessments["Ethnicity"] = assessments["Ethnicity"].replace({'' : 'All'})                                       
assessments["Assessment Decision"] = assessments["Assessment Decision"].replace({'' : 'All Assessments '})
assessments['Assessment Decision'] = assessments['Assessment Decision'].str.strip()
assessments["Age"] = assessments["Age"].replace({'' : 'All'})
assessments.to_csv(out / 'assessments.csv', index = False)
assessments

# +
#### Temporary Accomadtion 
# -

for name, tab in tabs.items():
    remove_summary = tab.filter(contains_string('6-monthly summary')).expand(DOWN).expand(RIGHT) | tab.excel_ref('M4').expand(RIGHT).expand(DOWN)
    remove_proportion = tab.excel_ref('A5').expand(DOWN).filter(contains_string('Table ')).expand(DOWN).expand(RIGHT)

    if name in temp_accomadation:
        columns = ['Period', 'Local Authority', 'Household Composition', 'Local Authority', 'Accommadation Types', 'Temporary Accommadation Breakdown']
        trace.start(distribution.title, tab, columns, distribution.downloadURL)
        months = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove_summary
        year = months.shift(UP).is_not_blank()
        
        accommadation_type_breakdown = ['20', '21', '22', '23']
        accommadation_type = ['17', '18', '19']
        
        if right((name), 2) in accommadation_type_breakdown: #20,21,22,23
            if right((name), 2) == '20':
                remove = tab.excel_ref('D6').expand(RIGHT).expand(DOWN)
                date = tab.excel_ref('A1')
                local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank().is_not_whitespace()
                temp_acc_breakdown = tab.excel_ref('B6').expand(RIGHT).is_not_blank() - remove
                observations = temp_acc_breakdown.fill(DOWN).is_not_blank()
                dimensions = [
                    HDim(date, "Year", CLOSEST, LEFT), 
                    HDim(date, "Months", CLOSEST, LEFT),
                    HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
                    HDim(temp_acc_breakdown, "Temporary Accommadation Breakdown", DIRECTLY, ABOVE)
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("temp_accommadtion", tidy_sheet.topandas())    
           
            elif right((name), 2) == '21':
                months = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - remove_summary
                year = months.shift(UP).is_not_blank()
                temp_acc_breakdown = tab.excel_ref('A1')
                local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank().is_not_whitespace()
                observations = months.fill(DOWN).is_not_blank() - remove_proportion
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
                    HDim(temp_acc_breakdown, "Temporary Accommadation Breakdown", CLOSEST, ABOVE)
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("temp_accommadtion", tidy_sheet.topandas())
                
            else: #22, 23
                months = tab.excel_ref('B6').expand(RIGHT).is_not_blank() - remove_summary
                year = months.shift(UP).is_not_blank()
                temp_acc_breakdown = tab.excel_ref('A1')
                local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank().is_not_whitespace()
                observations = months.fill(DOWN).is_not_blank() - remove_proportion    
                dimensions = [
                    HDim(year, "Year", CLOSEST, LEFT), 
                    HDim(months, "Months", DIRECTLY, ABOVE),
                    HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
                    HDim(temp_acc_breakdown, "Temporary Accommadation Breakdown", CLOSEST, ABOVE)
                ]
                tidy_sheet = ConversionSegment(tab, dimensions, observations)
                trace.with_preview(tidy_sheet)
                #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
                trace.store("temp_accommadtion", tidy_sheet.topandas())
                
        elif right((name), 2) in accommadation_type: #17,18,19
            accommadation_types = tab.excel_ref('A5').expand(DOWN).is_not_blank() - remove_proportion 
            observations = months.fill(DOWN).is_not_blank() - remove_proportion
            household_composition = tab.excel_ref('A1')
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(household_composition, "Household Composition", CLOSEST, LEFT),
                HDim(accommadation_types, "Accommadation Types", DIRECTLY, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            trace.store("temp_accommadtion", tidy_sheet.topandas())

        else: #14,15,16
            if right((name), 2) == '15':
                months = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - remove_summary
                year = months.shift(UP).is_not_blank()
                
            local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank().is_not_whitespace() - remove_proportion 
            accomadtion_type = 'temporary accommodation'
            household_composition = tab.excel_ref('A1')
            observations = months.fill(DOWN).is_not_blank() - remove_proportion
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(household_composition, "Household Composition", CLOSEST, LEFT),
                HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            trace.store("temp_accommadtion", tidy_sheet.topandas())
        

# +
temp_accommadtion = trace.combine_and_trace(datasetTitle, "temp_accommadtion").fillna('')
temp_accommadtion.rename(columns={'OBS' : 'Value','DATAMARKER' : 'Marker'}, inplace=True)
temp_accommadtion['Year'] = temp_accommadtion['Year'].astype(str).replace('\.0', '', regex=True)
temp_accommadtion['Year'] =  temp_accommadtion["Year"].apply(year_format)
temp_accommadtion['Months'] = temp_accommadtion['Months'].apply(lambda x: 'Q4' if 'Jan-March' in x or '03' in x else  
                                      ('Q1' if 'April-June' in x or '06' in x else 
                                       ('Q2' if 'July-Sept' in x or '09' in x else  
                                        ( 'Q3' if 'Oct-Dec' in x or '12' in x else
                                         ('gH1' if 'April to September ' in x else x)))))

temp_accommadtion['Period'] = temp_accommadtion['Year'] + temp_accommadtion['Months']
temp_accommadtion.drop(['Year', 'Months'], axis=1, inplace=True)
temp_accommadtion['Period'] =  temp_accommadtion["Period"].apply(date_time_government)
temp_accommadtion["Local Authority"] = temp_accommadtion["Local Authority"].replace({'' : 'Scotland'})

temp_accommadtion['Household Composition'] = temp_accommadtion['Household Composition'].astype(str).str.replace(u'\xa0', ' ')
temp_accommadtion["Household Composition"]= temp_accommadtion["Household Composition"].str.split(': ',expand=True)[1]
temp_accommadtion["Household Composition"]= temp_accommadtion["Household Composition"].str.split(', ',expand=True)[0]
temp_accommadtion['Temporary Accommadation Breakdown'] = temp_accommadtion['Temporary Accommadation Breakdown'].astype(str).str.replace(u'\xa0', ' ')
temp_accommadtion["Temporary Accommadation Breakdown"]= temp_accommadtion["Temporary Accommadation Breakdown"].str.split(': ',expand=True)[1]
temp_accommadtion["Temporary Accommadation Breakdown"]= temp_accommadtion["Temporary Accommadation Breakdown"].str.split(', ',expand=True)[0]
temp_accommadtion.to_csv(out / 'temp_accommadtion.csv', index = False)
temp_accommadtion
# -

#SG - Homelessness Update - Outcomes 
for name, tab in tabs.items():
    remove_summary = tab.filter(contains_string('6-monthly summary')).expand(DOWN).expand(RIGHT) | tab.excel_ref('M4').expand(RIGHT).expand(DOWN)
    remove_proportion = tab.excel_ref('A5').expand(DOWN).filter(contains_string('Table ')).expand(DOWN).expand(RIGHT)

    if name in outcomes:
        columns = ['Period', 'Local Authority', 'Contact Status', 'Homelessness Status', 'Outcome Type', 'Support', 'Assessment']
        trace.start(distribution.title, tab, columns, distribution.downloadURL)
       
        if right((name), 2) == '24':
            remove = tab.excel_ref('A9').expand(DOWN).expand(RIGHT)
            months = tab.excel_ref('B5').expand(RIGHT).is_not_blank() - remove_summary
            year = months.shift(UP).is_not_blank()
            contact_status = tab.excel_ref('A5').expand(DOWN).is_not_blank() - remove 
            homelessness_status = tab.excel_ref('A1')
            observations = months.fill(DOWN).is_not_blank() - remove
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(contact_status, "Contact Status", DIRECTLY, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            df = tidy_sheet.topandas()
            df['Homelessness Status'] = 'Unintentionally homesless households'
            df['Outcome Type'] = 'All'
            trace.store("outcomes", df)    
        if right((name), 2) == '25':
            months = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove_summary
            year = months.shift(UP).is_not_blank()
            outcome_type = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
            observations = months.fill(DOWN).is_not_blank() - remove_proportion
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(outcome_type, "Outcome Type", DIRECTLY, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            df = tidy_sheet.topandas()
            df['Homelessness Status'] = 'Unintentionally homeless or threatened with homelessness'
            df['Contact Status'] = 'Contact maintained'
            trace.store("outcomes", df) 
        if right((name), 2) == '26':   
            months = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove_summary
            year = months.shift(UP).is_not_blank()
            outcome_type = tab.excel_ref('A4').expand(DOWN).is_not_blank() - remove_proportion
            observations = months.fill(DOWN).is_not_blank() - remove_proportion
            dimensions = [
                HDim(year, "Year", CLOSEST, LEFT), 
                HDim(months, "Months", DIRECTLY, ABOVE),
                HDim(outcome_type, "Outcome Type", DIRECTLY, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            df = tidy_sheet.topandas()
            df['Homelessness Status'] = 'Intentionally homeless or threatened with homelessness'
            df['Contact Status'] = 'Contact maintained'
            trace.store("outcomes", df) 
        if right((name), 2) == '27': 
            remove = tab.excel_ref('K1').expand(RIGHT).expand(DOWN)
            date = tab.excel_ref('A1').is_not_blank()
            local_authority = tab.excel_ref('A4').expand(DOWN).is_not_blank()
            outcome_type = tab.excel_ref('A3').expand(RIGHT).is_not_blank() -remove
            observations = outcome_type.fill(DOWN).is_not_blank()
            dimensions = [
                HDim(date, "Year", CLOSEST, LEFT), 
                HDim(date, "Months", CLOSEST, LEFT),
                HDim(outcome_type, "Outcome Type", DIRECTLY, ABOVE),
                HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            df = tidy_sheet.topandas()
            df['Homelessness Status'] = 'Unintentionally homesless households'
            df['Contact Status'] = 'Contact maintained'
            trace.store("outcomes", df) 
        if right((name), 2) == '28': 
            remove = tab.excel_ref('J1').expand(RIGHT).expand(DOWN)
            local_authority = tab.excel_ref('A4').expand(DOWN).is_not_blank()
            date = tab.excel_ref('A1').is_not_blank()
            support = tab.excel_ref('B4').expand(RIGHT).is_not_blank() - remove
            assessment = tab.excel_ref('B3').expand(RIGHT).is_not_blank() - remove
            observations = local_authority.fill(RIGHT).is_not_blank() - remove
            dimensions = [
                HDim(date, "Year", CLOSEST, LEFT), 
                HDim(date, "Months", CLOSEST, LEFT),
                HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
                HDim(assessment, "Assessment", CLOSEST, LEFT),
                HDim(support, "Support", CLOSEST, LEFT),
            ]
            tidy_sheet = ConversionSegment(tab, dimensions, observations)
            trace.with_preview(tidy_sheet)
            #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
            df = tidy_sheet.topandas()
            df['Homelessness Status'] = 'Unintentionally homeless or threatened with homelessness'
            df['Outcome Type'] = 'All'
            df['Contact Status'] = 'All outcomes'
            trace.store("outcomes", df) 

# +
outcomes = trace.combine_and_trace(datasetTitle, "outcomes").fillna('')
outcomes.rename(columns={'OBS' : 'Value','DATAMARKER' : 'Marker'}, inplace=True)
outcomes["Local Authority"] = outcomes["Local Authority"].replace({'' : 'Scotland'})
outcomes["Assessment"] = outcomes["Assessment"].replace({'' : 'All'})
outcomes["Support"] = outcomes["Support"].replace({'' : 'All'})
outcomes['Year'] = outcomes['Year'].astype(str).replace('\.0', '', regex=True)
outcomes['Year'] =  outcomes["Year"].apply(year_format)
outcomes['Months'] = outcomes['Months'].apply(lambda x: 'Q4' if 'Jan-March' in x or '03' in x else  
                                      ('Q1' if 'April-June' in x or '06' in x else 
                                       ('Q2' if 'July-Sept' in x or '09' in x else  
                                        ( 'Q3' if 'Oct-Dec' in x or '12' in x else
                                         ('gH1' if 'April to September ' in x else x)))))

outcomes['Period'] = outcomes['Year'] + outcomes['Months']
outcomes.drop(['Year', 'Months'], axis=1, inplace=True)
outcomes['Period'] =  outcomes["Period"].apply(date_time_government)
outcomes.to_csv(out / 'outcomes.csv', index = False)
outcomes

# +
#SG - Homelessness Update - Covid
# -

for name, tab in tabs.items():
    if name in covid:
        print(tab.name)
        columns = ['Period', 'Local Authority',]
        trace.start(distribution.title, tab, columns, distribution.downloadURL)
        
        breakdown = tab.excel_ref('A1')
        local_authority = tab.excel_ref('A5').expand(DOWN).is_not_blank()
        year = tab.excel_ref('B4').expand(RIGHT).is_not_blank()
        month = tab.excel_ref('B5').expand(RIGHT).is_not_blank()
        observations = month.fill(DOWN).is_not_blank()
            
        dimensions = [
            HDim(year, "Year", CLOSEST, LEFT), 
            HDim(month, "Months", DIRECTLY, ABOVE),
            HDim(local_authority, "Local Authority", DIRECTLY, LEFT),
            HDim(breakdown, "Breakdown", CLOSEST, LEFT),
        ]
        tidy_sheet = ConversionSegment(tab, dimensions, observations)
        trace.with_preview(tidy_sheet)
        #savepreviewhtml(tidy_sheet, fname = tab.name+ "Preview.html")
        trace.store("covid", tidy_sheet.topandas())   
    else:    
        continue


covid = trace.combine_and_trace(datasetTitle, "covid").fillna('')
covid.rename(columns={'OBS' : 'Value','DATAMARKER' : 'Marker'}, inplace=True)
covid["Breakdown"]= covid["Breakdown"].str.split(': ',expand=True)[1]
covid['Year'] = covid['Year'].astype(str).replace('\.0', '', regex=True)
#month/{year}-{month}
covid['Months'] = covid['Months'].apply(lambda x: '01' if 'January' in x else 
                                        ('02' if 'February' in x else 
                                         ('03' if 'March' in x else 
                                          ('04' if 'April' in x else
                                           ('05' if 'May' in x else 
                                            ('06' if 'June' in x else 
                                             ('07' if 'July' in x else 
                                              ('08' if 'August' in x else 
                                               ('09' if 'September' in x else 
                                                ('10' if 'October' in x else 
                                                 ('11' if 'November' in x else 
                                                  ('12' if 'December' in x else x))))))))))))
covid['Months'] =  covid["Months"].apply(month_format)
covid['Period'] = 'month/' + covid['Year'] + '-' + covid['Months']   
covid.drop(['Year', 'Months'], axis=1, inplace=True)
covid["Marker"] = covid["Marker"].replace({'<4' : 'between-1-and-4'})
covid.to_csv(out / 'covid.csv', index = False)
covid



# +
###################################################################################
