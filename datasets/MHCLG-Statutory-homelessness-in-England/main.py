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
scraper.select_dataset(latest=True) 
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
#Now start the transformation

for tab in tabs:
    columns=['Contents']
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    if tab.name in ['A1']: #only transforming tab A1 for now
        print(tab.name)
# -


