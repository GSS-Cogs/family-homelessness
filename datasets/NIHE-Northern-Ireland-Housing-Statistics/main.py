# # NIHE Northern Ireland Housing Statistics 

# +
import json
import pandas as pd
from gssutils import *
from pandas import ExcelWriter
import numpy as np

scraper = Scraper(seed = "info.json")
scraper.distributions = [x for x in scraper.distributions if hasattr(x, "mediaType")]
scraper

trace = TransformTrace()
cubes = Cubes("info.json")
# -
xls = pd.ExcelFile(scraper.distributions[0].downloadURL, engine="odf")
with ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet, index = False)
    writer.save()
tabs = loadxlstabs("data.xls")

distribution = scraper.distribution(latest=True)
datasetTitle = 'Northern Ireland Housing Statistics 2019-20'
distribution

columns = ["Period", "Homelessness Reason", "Outcome"]

tabs_names_to_process = ['T3_8', 'T3_9', 'T3_10_', 'T3_11']
for tab_name in tabs_names_to_process:

    # Raise an exception if one of our required tabs is missing
    if tab_name not in [x.name for x in tabs]:
        raise ValueError(f'Aborting. A tab named {tab_name} required but not found')

    # Select the tab in question
    tab = [x for x in tabs if x.name == tab_name][0]
    print(tab.name)
    trace.start(datasetTitle, tab, columns, distribution.downloadURL)
    
    cell = tab.excel_ref("A1")
    period = cell.shift(0, 2).fill(RIGHT).is_not_whitespace()

    if tab.name == 'T3_10_':
        remove = tab.filter(contains_string("1. See Appendix 3: Data Sources - Social Renting Demand.")).expand(RIGHT).expand(DOWN)
        outcome = cell.shift(0, 2).fill(DOWN).is_not_whitespace()-remove
        observations = period.waffle(outcome)
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(outcome, "Outcome", DIRECTLY, LEFT)
        ]
    elif tab.name == 'T3_9':
        remove = tab.filter(contains_string("SOURCE: NIHE")).expand(LEFT).expand(DOWN)
        age = cell.shift(1, 2).fill(DOWN)-remove
        house_hold_type = age.shift(LEFT).is_not_blank()
        observations = period.waffle(age)-remove
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(house_hold_type, "House_Hold_Type", CLOSEST, ABOVE)
        ]   
    else:
        remove = tab.filter(contains_string("1. See Appendix 3: Data Sources - Social Renting Demand.")).expand(RIGHT).expand(DOWN)
        homelessness_reason = cell.shift(0, 2).fill(DOWN).is_not_whitespace()-remove
        observations = period.waffle(homelessness_reason)
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(homelessness_reason, "Outcome", DIRECTLY, LEFT)
        ]
    tidy_sheet = ConversionSegment(tab, dimensions, observations)
    savepreviewhtml(tidy_sheet, fname=tab.name + "Preview.html")
    trace.with_preview(tidy_sheet)
    trace.store("combined_dataframe", tidy_sheet.topandas())

df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

df

df['Period'].unique()


# +
def left(s, amount):
    return s[:amount]
def date_time (date):
    if len(date) == 7:
        return 'financial-year/' + left(date, 4)
    
df['Period'] =  df["Period"].apply(date_time)
# -

df['Period'].unique()

df

df['DATAMARKER'].unique()

df.dtypes

"""I have two dimensions from two different tabs which has names "outcome" and "homelessness reason" 
but values are extracted from the same x and y axis. In the dataframe, dimension "outcome" 
(The first dimension mentioned) appears with values of both "outcome"  and "homelessness reason".
"Outcome" is related to result of homlessness application whereas " Homelessness Reason" is related 
to the reason for homelessness so these two dimensions can't be combined.
The problem is to be addressed latter but for now, I am moving on to get transformation to final state"""
for col in df.columns:
    print(f"Total columns - {col}")
    if col in ['House_Hold_Type', 'DATAMARKER']:
        print(f"\"COLUMNS TO BE PATHIFIED\" - {col}")
        df[col] = df[col].astype('category')
        df[col].cat.rename_categories(lambda x: pathify(x), inplace=True)
print(f"COLUMN YET TO BE PATHIFIED ----------------------- \"Outcome\"")      

cubes.add_cube(scraper, df, scraper.title)

cubes.output_all()

trace.render("spec_v1.html")
