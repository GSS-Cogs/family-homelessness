# # NIHE Northern Ireland Housing Statistics 

# +
import json
import pandas as pd
from gssutils import *
from pandas import ExcelWriter

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

df
