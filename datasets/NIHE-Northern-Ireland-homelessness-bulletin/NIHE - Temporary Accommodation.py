# -*- coding: utf-8 -*-
# # NIHE Northern Ireland homelessness bulletin 
# ##NIHE - Temporary Accommodation

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
tab = tabs['3_1']
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
            HDimConst('Measure Type','Placements')
    
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
tab = tabs['3_2']
cell = tab.excel_ref('A2')
accomdation = cell.fill(RIGHT).is_not_blank().is_not_whitespace() | tab.excel_ref('P5:Q5')
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(accomdation,'Accommodation Type',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Placements')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

 next_table = pd.concat([next_table, new_table])

# +
tab = tabs['3_3']
cell = tab.excel_ref('A2')
accomdation = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
year = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = year.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(accomdation,'Accommodation Type',DIRECTLY,ABOVE),
            HDim(year, 'Period',DIRECTLY,LEFT),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Children')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['3_4']
cell = tab.excel_ref('A2')
year = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
age = cell.fill(DOWN).is_not_blank().is_not_whitespace()  
observations = age.fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(age,'Age Bracket',DIRECTLY,LEFT),
            HDim(year, 'Period',DIRECTLY,ABOVE),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Children')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
# -

next_table = pd.concat([next_table, new_table])

# Sheet: 3_5 Households in temporary accommodation Tab `Year` hard coded 

# +
tab = tabs['3_5']
cell = tab.excel_ref('A2')
stay = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
accommodation = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
year = tab.excel_ref('A4:A9') 
observations = year.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(accommodation,'Accommodation Type',DIRECTLY,LEFT),
            HDim(stay,'Length of Stay',DIRECTLY,ABOVE),
            HDimConst('Period','gregorian-month/2019-Jan'),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Households')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Length of Stay'] = new_table['Length of Stay'].map(
    lambda x: {
        '< 6 Months' : 'less than 6 Months', 
        '6 Months to < 12 Months' : '6 to 12 months', 
        '1 to <2 Years' : '1 to 2 years' ,
       '2 to <3 Years' : '2 to 3 years', 
        '3 to <4 years' : '3 to 4 years', 
        '4 to <5 Years' : '4 to 5 years', 
        '5 Years +' : '5 years plus',
       'Total' :'total'      
        }.get(x, x))
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['3_5']
cell = tab.excel_ref('A2')
stay = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
accommodation = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
year = tab.excel_ref('A10:A15') 
observations = year.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(accommodation,'Accommodation Type',DIRECTLY,LEFT),
            HDim(stay,'Length of Stay',DIRECTLY,ABOVE),
            HDimConst('Period','gregorian-month/2019-Jul'),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Households')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Length of Stay'] = new_table['Length of Stay'].map(
    lambda x: {
        '< 6 Months' : 'less than 6 Months', 
        '6 Months to < 12 Months' : '6 to 12 months', 
        '1 to <2 Years' : '1 to 2 years' ,
       '2 to <3 Years' : '2 to 3 years', 
        '3 to <4 years' : '3 to 4 years', 
        '4 to <5 Years' : '4 to 5 years', 
        '5 Years +' : '5 years plus',
       'Total' :'total'      
        }.get(x, x))
# -

next_table = pd.concat([next_table, new_table])

# +
tab = tabs['3_5']
cell = tab.excel_ref('A2')
stay = cell.fill(RIGHT).is_not_blank().is_not_whitespace()
accommodation = cell.shift(1,0).fill(DOWN).is_not_blank().is_not_whitespace()
year = tab.excel_ref('A16:A21') 
observations = year.shift(1,0).fill(RIGHT).is_not_blank().is_not_whitespace() 
Dimensions = [
            HDim(accommodation,'Accommodation Type',DIRECTLY,LEFT),
            HDim(stay,'Length of Stay',DIRECTLY,ABOVE),
            HDimConst('Period','gregorian-month/2020-Jan'),
            HDimConst('Unit','Count'),  
            HDimConst('Measure Type','Households')
    
]  
c1 = ConversionSegment(observations, Dimensions, processTIMEUNIT=True)
new_table = c1.topandas()
import numpy as np
new_table.rename(columns={'OBS': 'Value','DATAMARKER': 'Marker'}, inplace=True)
new_table['Length of Stay'] = new_table['Length of Stay'].map(
    lambda x: {
        '< 6 Months' : 'less than 6 Months', 
        '6 Months to < 12 Months' : '6 to 12 months', 
        '1 to <2 Years' : '1 to 2 years' ,
       '2 to <3 Years' : '2 to 3 years', 
        '3 to <4 years' : '3 to 4 years', 
        '4 to <5 Years' : '4 to 5 years', 
        '5 Years +' : '5 years plus',
       'Total' :'total'      
        }.get(x, x))
# -

next_table = pd.concat([next_table, new_table])

list(next_table)

next_table = next_table[['Accommodation Type',
 'Age Bracket',
 'Household Composition',
 'Length of Stay',
 'Marker',
 'Measure Type',
 'Period',
 'Unit',
 'Value']]

next_table.fillna('All', inplace = True)

next_table['Period'] = next_table['Period'].str.rstrip('123 ')

next_table['Period'] = next_table['Period'].map(
    lambda x: {
        'Apr-Sep' : 'government-half/2018-2019/H1', 
        'Oct-Mar' : 'government-half/2018-2019/H2',
        'Apr-Jun': 'government-quarter/2018-2019/Q1' ,
        'Jul-Dec': 'government-quarter/2018-2019/Q2',
        'Jul-Dec³' : 'government-quarter/2018-2019/Q2', 
       'Apr-Jun (Financial year Q1)²' : 'government-quarter/2018-2019/Q1' ,
        'Apr-Jun (Financial year Q1)³' : 'government-quarter/2018-2019/Q1' ,
       'Apr-Jun (Financial year 2019 Q1)¹' : 'government-quarter/2018-2019/Q1',
        'Jan 2019' : 'gregorian-month/2019-Jan' , 
        'Jul 2019' : 'gregorian-month/2019-Jul' ,
        'Jan 2020' : 'gregorian-month/2020-Jan'
        }.get(x, x))

next_table['Marker'] = next_table['Marker'].map(
    lambda x: {
        '*' : 'Statistical disclosure',
        'All' : ''        
        }.get(x, x))


# +
def user_perc2(x,y):
    
    if (str(x) ==  'Statistical disclosure'): 
        
        return 0
    else:
        return y
    
next_table['Value'] = next_table.apply(lambda row: user_perc2(row['Marker'], row['Value']), axis = 1)
# -

from pathlib import Path
import numpy as np
out = Path('out')
out.mkdir(exist_ok=True)
next_table.drop_duplicates().to_csv(out / 'nihe-temporary-accommodation.csv', index = False)

next_table
