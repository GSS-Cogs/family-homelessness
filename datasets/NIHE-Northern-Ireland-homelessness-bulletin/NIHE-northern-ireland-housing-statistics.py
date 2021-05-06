#!/usr/bin/env python
# coding: utf-8

# In[10]:


# # NIHE Northern Ireland Housing Statistics


# In[11]:


import pandas as pd
from gssutils import *
import json
import numpy as np

info = json.load(open("info.json"))

info['dataURL'] = "https://www.communities-ni.gov.uk/system/files/publications/communities/ni-housing-stats-19-20-tables3.ods"
info['landingPage'] = "https://www.communities-ni.gov.uk/topics/housing-statistics#toc-2"

with open('info.json', 'w') as outfile:
    json.dump(info, outfile, indent=4)

scraper = Scraper(seed = "info.json")
scraper.distributions = [x for x in scraper.distributions if hasattr(x, "mediaType")]
scraper
#%%

trace = TransformTrace()
#cubes = Cubes("housing-stats-info.json")
# +
# The source data is published  in ODS format. ODS is converted to xls with the below lines of code as databaker is compatible with xls

"""xls = pd.ExcelFile("https://www.communities-ni.gov.uk/system/files/publications/communities/ni-housing-stats-19-20-tables3.ods", engine="odf")
with pd.ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet, index = False)
    writer.save()
tabs = loadxlstabs("data.xls")"""


# In[12]:


"""print(type(tabs))"""

distribution = scraper.distribution(latest=True)
datasetTitle = info["title"]
distribution
#%%
datasetTitle

columns = ["Period", "Age", "Homelessness Reason", "House Hold Type", "Outcome", "Unit"]

tabs_names_to_process = {'T3_8', 'T3_9', 'T3_10_', 'T3_11'}

"""if len(set(tabs_names_to_process)-{x.name for x in tabs}) != 0:
    raise ValueError(f'Aborting. A tab named {set(tabs_names_to_process)-{x.name for x in tabs}} required but not found')"""

tabs = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}


# In[13]:


tab = tabs['T3_10_']
trace.start(datasetTitle, tab, columns, distribution.downloadURL)

cell = tab.excel_ref("A1")

unit = "household"
trace.Unit("Hardcoded as household")
period = cell.shift(0, 2).fill(RIGHT).is_not_whitespace()
trace.Period("Defined from cell B3 right")

remove = tab.filter(contains_string("1. See Appendix 3: Data Sources - Social Renting Demand.")).expand(RIGHT).expand(DOWN)|tab.filter(contains_string('Total'))

outcome = cell.shift(0, 2).fill(DOWN).is_not_whitespace()-remove
trace.Outcome("Defined from cell A4 and down")

observations = period.waffle(outcome)
dimensions = [
    HDim(period, "Period", DIRECTLY, ABOVE),
    HDim(outcome, "Outcome", DIRECTLY, LEFT),
    HDimConst("Age", "all"),
    HDimConst("Unit", "household")
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
savepreviewhtml(tidy_sheet, fname=tab.name + "Preview.html")
trace.with_preview(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())


# In[14]:


tab = tabs['T3_9']
trace.start(datasetTitle, tab, columns, distribution.downloadURL)

cell = tab.excel_ref("A1")

unit = "household"
trace.Unit("Hardcoded as household")
#footnotes and Total column is captured in remove
period = cell.shift(1, 2).fill(RIGHT).is_not_whitespace()
trace.Period("Defined from cell C3 right")

remove = tab.filter(contains_string("SOURCE: NIHE")).expand(LEFT).expand(DOWN)|tab.filter(contains_string('Total')).expand(RIGHT)
age = cell.shift(1, 2).fill(DOWN).is_not_blank()-remove
trace.Age("Defined from cell B4 and down excluding remove")

house_hold_type = age.shift(LEFT).is_not_blank()
trace.House_Hold_Type("Defined from cell A4 and down")

observations = period.waffle(age)-remove
dimensions = [
    HDim(period, "Period", DIRECTLY, ABOVE),
    HDim(age, "Age", DIRECTLY, LEFT),
    HDim(house_hold_type, "House_Hold_Type", CLOSEST, ABOVE),
    HDimConst("Unit", "household")
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
savepreviewhtml(tidy_sheet, fname=tab.name + "Preview.html")
trace.with_preview(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())


# In[15]:


#'T3_8'
tab = tabs['T3_8']
trace.start(datasetTitle, tab, columns, distribution.downloadURL)

cell = tab.excel_ref("A1")

unit = "household"
trace.Unit("Hardcoded as household")

#footnotes and Total column is captured in remove
period = cell.shift(0, 2).fill(RIGHT).is_not_whitespace()
trace.Period("Defined from cell B3 right")

remove = tab.filter(contains_string("Appendix 3")).expand(RIGHT).expand(DOWN)|tab.filter(contains_string('Total'))
homelessness_reason = cell.shift(0, 2).fill(DOWN).is_not_whitespace()-remove
trace.Homelessness_Reason("Defined from cell A4 and down")

observations = period.waffle(homelessness_reason)
dimensions = [
    HDim(period, "Period", DIRECTLY, ABOVE),
    HDim(homelessness_reason, "Homelessness Reason", DIRECTLY, LEFT),
    HDimConst("Age", "all"),
    HDimConst("Unit", "household")
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
savepreviewhtml(tidy_sheet, fname=tab.name + "Preview.html")
trace.with_preview(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())


# In[16]:


#'T3_11'
tab = tabs['T3_11']
trace.start(datasetTitle, tab, columns, distribution.downloadURL)

cell = tab.excel_ref("A1")

unit = "household"
trace.Unit("Hardcoded as household")

#footnotes and Total column is captured in remove
period = cell.shift(0, 2).fill(RIGHT).is_not_whitespace()
trace.Period("Defined from cell B3 right")

remove = tab.filter(contains_string("1. See Appendix 3: Data Sources - Social Renting Demand.")).expand(RIGHT).expand(DOWN)|tab.filter(contains_string('Total'))
homelessness_reason = cell.shift(0, 2).fill(DOWN).is_not_whitespace()-remove
trace.Homelessness_Reason("Defined from cell A4 and down")

observations = period.waffle(homelessness_reason)
dimensions = [
    HDim(period, "Period", DIRECTLY, ABOVE),
    HDim(homelessness_reason, "Homelessness Reason", DIRECTLY, LEFT),
    HDimConst("Age", "all"),
    HDimConst('Outcome', 'Accepted'),
    HDimConst("Unit", "household")
]
tidy_sheet = ConversionSegment(tab, dimensions, observations)
savepreviewhtml(tidy_sheet, fname=tab.name + "Preview.html")
trace.with_preview(tidy_sheet)
trace.store("combined_dataframe", tidy_sheet.topandas())


# In[17]:


df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

df

df['Period'] = df['Period'].astype('category')

df['Period'].cat.categories

df['Period'] =  df["Period"].cat.rename_categories(lambda x: f"government-year/{x[:4]}-{x[:2]}{x[-2:]}")

#Replace empty string with nan
df.loc[df['Age'] == '', 'Age'] = np.nan
trace.Age("Empty string in Age column is replaced by np.nan")

# pattern for "Age" is number-number so we have to remove brackets () and yrs
df['Age'] = df['Age'].apply(lambda x: str(x).strip("(yrs)"))

trace.Age("(yrs) is removed and age has a pattern number-number")

#remove empty space
df['Age'] = df['Age'].str.strip()

df = df.rename(columns={'OBS': 'Value', 'DATAMARKER': 'MARKER'})

df['Value'] = df['Value'].apply(lambda x: None if pd.isnull(x) else '{0:.0f}'.format(pd.to_numeric(x)))

"""for col in df.columns:
# Transform by saying the columns which are not required to be transformed
# as the number of columns not to be transformed is less than the ones to be transformed.
    if col not in ['Value', 'Age']:
        df[col] = df[col].apply(lambda x: pathify(str(x)))
        df[col] = df[col].astype('category')"""

df


# In[18]:


tidy = df

# In[19]:

info['landingPage'] = "https://www.communities-ni.gov.uk/publications/topic/8182?search=%22Northern+Ireland+Homelessness+Bulletin%22&Search-exposed-form=Go&sort_by=field_published_date"

del info['dataURL']

with open('info.json', 'w') as outfile:
    json.dump(info, outfile, indent= 4 )

