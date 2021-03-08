# # NIHE Northern Ireland Housing Statistics 

# +
import json
import pandas as pd
from gssutils import *
from pandas import ExcelWriter
import numpy as np
from io import StringIO

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

columns = ["Period", "Age", "Homelessness Reason", "House Hold Type", "Outcome"]

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

    if tab.name == 'T3_10_':
# footnotes and Total column is captured in remove
        period = cell.shift(0, 2).fill(RIGHT).is_not_whitespace()
        trace.Period("Defined from cell B3 right")
        
        remove = tab.filter(contains_string("1. See Appendix 3: Data Sources - Social Renting Demand.")).expand(RIGHT).expand(DOWN)|tab.filter(contains_string('Total'))
        
        outcome = cell.shift(0, 2).fill(DOWN).is_not_whitespace()-remove
        trace.Outcome("Defined from cell A4 and down")
        
        observations = period.waffle(outcome)
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(outcome, "Outcome", DIRECTLY, LEFT),
            HDimConst("Age", "all")
        ]
    elif tab.name == 'T3_9':
#footnotes and Total column is captured in remove
        period = cell.shift(1, 2).fill(RIGHT).is_not_whitespace()
        trace.Period("Defined from cell C3 right")
        
        remove = tab.filter(contains_string("SOURCE: NIHE")).expand(LEFT).expand(DOWN)|tab.filter(contains_string('Total')).expand(RIGHT)
        age = cell.shift(1, 2).fill(DOWN)-remove
        trace.Age("Defined from cell B4 and down excluding remove")
        
        house_hold_type = age.shift(LEFT).is_not_blank()
        trace.House_Hold_Type("Defined from cell A4 and down")
                  
        observations = period.waffle(age)-remove
        dimensions = [
            HDim(period, "Period", DIRECTLY, ABOVE),
            HDim(age, "Age", DIRECTLY, LEFT),
            HDim(house_hold_type, "House_Hold_Type", CLOSEST, ABOVE)
        ]  
#['T3_8', 'T3_11']
    else:
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
        ]
    tidy_sheet = ConversionSegment(tab, dimensions, observations)
    savepreviewhtml(tidy_sheet, fname=tab.name + "Preview.html")
    trace.with_preview(tidy_sheet)
    trace.store("combined_dataframe", tidy_sheet.topandas())

df = trace.combine_and_trace(datasetTitle, "combined_dataframe")

df


# +
def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]
def date_time (date):
    if len(date)  == 7:
        #id/government-year/{year1}-{year2}
        return 'id/government-year/' + left(date, 4) + '-' + left(date, 2) + right(date, 2)

df['Period'] =  df["Period"].apply(date_time)
trace.Period("formatted as id/government-year/{year1}-{Year2}")
# -

#Replace empty string with nan
df.loc[df['Age'] == '', 'Age'] = np.nan
trace.Age("Empty string in Age column is replaced by np.nan")


# pattern for "Age" is number-number so we have to remove brackets () and yrs
def converter(x):
    try:
        return str(x).strip("(yrs)")
    except AttributeError:
        return None


df['Age'] = df['Age'].apply(converter)
trace.Age("(yrs) is removed and age has a pattern number-number")

#remove empty space
df['Age'] = df['Age'].str.strip()

df = df.rename(columns={'OBS': 'Value', 'DATAMARKER': 'MARKER'})

df['Value'] = df['Value'].apply(lambda x: None if pd.isnull(x) else '{0:.0f}'.format(pd.to_numeric(x)))

df['MARKER'].unique()

for col in df.columns:
# Transform by saying the columns which are not required to be transformed
# as the number of columns not to be transformed is less than the ones to be transformed.
    if col not in ['Value', 'Age']:       
        df[col] = df[col].apply(lambda x: pathify(str(x)))
        df[col] = df[col].astype('category')
#         df[col].cat.rename_categories(lambda x: pathify(str(x)))

cubes.add_cube(scraper, df, scraper.title)

cubes.output_all()

trace.render("spec_v1.html")
