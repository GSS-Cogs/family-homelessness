# -*- coding: utf-8 -*-
# # NIHE Northern Ireland homelessness bulletin 

from gssutils import * 
import json 

info = json.load(open('info.json')) 
landingPage = info['landingPage'] 
landingPage 

scraper = Scraper(landingPage) 
scraper 

tabs = { tab.name: tab for tab in scraper.distributions[2].as_databaker() }
list(tabs)

next_table = pd.DataFrame()

# +
tab = tabs['1_1']
cell = tab.excel_ref('A2')
reason = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = reason.fill(DOWN).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(reason,'Reason for Homelessness',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

 next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_1A']
cell = tab.excel_ref('A2')
reason = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(reason,'Accommodation not Reasonable breakdown',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_1B']
cell = tab.excel_ref('A2')
reason = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(reason,'Intimidation Breakdown',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_1C']
cell = tab.excel_ref('A2')
reason = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(reason,'Loss of Rented Accommodation reason',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_2']
cell = tab.excel_ref('A2')
htype = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
hstatus = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(hstatus,'Household Composition',CLOSEST,LEFT),
            HDim(htype,'sex',CLOSEST,LEFT),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Household Composition'] = new_table['Household Composition'].map(str)  + ' ' + new_table['sex'].map(str) 
new_table['Household Composition'] = new_table['Household Composition'].map(
    lambda x: {
        'Single males 16-17 yrs' : 'Single Male 16-17 yrs' ,
        'Single males 18-25 yrs' : 'Single Male 18-25 yrs', 
        'Single males 26-59 yrs': 'Single Male 26-59 yrs',
       'Single males Total' : 'Single Male Total', 
        'Single females 16-17 yrs': 'Single Female 16-17 yrs', 
        'Single females 18-25 yrs': 'Single Female 18-25 yrs',
       'Single females 26-59 yrs': 'Single Female 26-59 yrs', 
        'Single females Total' : 'Single Female Total',
        'Couples Total' : 'Couples' ,
       'Families¹ Total' : 'Families' ,
        'Pensioner households Total' : 'Pensioner households', 
        'Undefined Total': 'Undefined',
       'Total Total' : 'Total'        
        }.get(x, x))
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_3']
cell = tab.excel_ref('A2')
year = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
area = cell.fill(DOWN).is_not_blank().is_not_whitespace() - tab.excel_ref('A18').expand(DOWN)
unit = cell.shift(0,2).fill(RIGHT).is_not_blank().is_not_whitespace()
observations = area.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(area,'ONS Geography',DIRECTLY,LEFT),
            HDim(year, 'Period',CLOSEST,LEFT),
            HDim(unit,'Unit',DIRECTLY,ABOVE),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Unit'] = new_table['Unit'].map(
    lambda x: {
        'Total presenters' : 'Count', 
        'Presenters per 1,000 population' : 'Per 1,000 population'
        }.get(x, x))
new_table['ONS Geography'] = new_table['ONS Geography'].map(
    lambda x: {
        'Antrim and Newtownabbey' : 'N09000001', 
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
        }.get(x, x))
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_4']
cell = tab.excel_ref('A2')
year = cell.shift(0,1).fill(RIGHT).is_not_blank().is_not_whitespace()
decision = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = decision.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(decision,'Assessment Decision',DIRECTLY,LEFT),
            HDim(year, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_5']
cell = tab.excel_ref('A2')
outcome = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(outcome,'Legislative test Outcome',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['1_6']
cell = tab.excel_ref('A2')
presenter = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(presenter,'Repeat Homeless Presentations',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Household')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

next_table.fillna('All', inplace = True)
next_table['ONS Geography'] = next_table['ONS Geography'].map(lambda cell: cell.replace('All', 'N07000001'))
next_table['Repeat Homeless Presentations'] = next_table['Repeat Homeless Presentations'].map(lambda cell: cell.replace('All', 'Not Applicable'))

next_table['Marker'] = next_table['Marker'].map(
    lambda x: {
        '*' : 'Statistical disclosure',
        'All' : ''        
        }.get(x, x))

next_table['Period'] = next_table['Period'].str.rstrip('123 ')

next_table['Period'] = next_table['Period'].map(
    lambda x: {
        'Apr-Sep' : 'government-half/2018-2019/H1', 
        'Oct-Mar' : 'government-half/2018-2019/H2',
        'Apr-Jun': 'government-quarter/2018-2019/Q1' ,
        'Jul-Dec': 'government-quarter/2018-2019/Q2',
        'Jul-Dec³' : 'government-quarter/2018-2019/Q2', 
       'Apr-Jun (Financial year Q1)²' : 'government-quarter/2018-2019/Q1' ,
       'Apr-Jun (Financial year 2019 Q1)¹' : 'government-quarter/2018-2019/Q1', 
        '2018/19' : 'government-year/2018-2019'
        }.get(x, x))


# +
def user_perc2(x,y):
    
    if (str(x) ==  'Statistical disclosure'): 
        
        return 0
    else:
        return y
    
next_table['Value'] = next_table.apply(lambda row: user_perc2(row['Marker'], row['Value']), axis = 1)
# -

next_table = next_table[['Period', 'Reason for Homelessness', 'Accommodation not Reasonable breakdown', 'Intimidation Breakdown', 'Loss of Rented Accommodation reason', 'Household Composition', 'ONS Geography', 'Assessment Decision', 'Legislative test Outcome', 'Repeat Homeless Presentations', 'Measure Type', 'Unit', 'Value','Marker']]

from pathlib import Path
import numpy as np
out = Path('out')
out.mkdir(exist_ok=True)
next_table.drop_duplicates().to_csv(out / 'nihe-homelessness-presentation.csv', index = False)

next_table


