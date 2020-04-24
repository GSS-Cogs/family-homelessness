# # MHCLG Rough sleeping 

from gssutils import * 
import json 

# +
info = json.load(open('info.json')) 

landing_page = info['landingPage'] 
print(landing_page)
spreadsheet_title = info['dataset1']['spreadsheetname']
print(spreadsheet_title)

# +
#### Add transformation script here #### 

scraper = Scraper(landingPage) 
scraper.select_dataset(latest=True) 
scraper 
# -

try:
    for i in scraper.distributions:
        if spreadsheet_title in i.title:
            print(i.title)
            sheets = i
            break
except Exception as e:
         print('Error: ' + str(e))

#### Convert to a DataBaker object
try:
    sheets = sheets.as_databaker()
except Exception as e:
    print(e.message, e.args)


def extract_table(tab, ref1, ref2, ref3, ref4, title1, title2, title3):
    try:
        col1 = tab.excel_ref(ref1).fill(DOWN).is_not_blank()
        col2 = tab.excel_ref(ref2).fill(DOWN).is_not_blank()
        col3 = tab.excel_ref(ref3).expand(RIGHT).is_not_blank() 
        col4 = tab.excel_ref(ref4).is_not_blank()

        Dimensions = [
            HDim(col1,title1, DIRECTLY, LEFT),
            HDim(col2,title2, DIRECTLY, LEFT),
            HDim(col3,title3, DIRECTLY, ABOVE)
            ]

        c1 = ConversionSegment(col4, Dimensions, processTIMEUNIT=True)
        tbl = c1.topandas()
        
        return tbl
    except Exception as e:
        return "extract_sheet: " + str(e)   


dataset_title = info['dataset1']['name'] 
sheet_name = info['dataset1']['sheet1']['name']
col_names = info['dataset1']['sheet1']['columnnames']
coords = info['dataset1']['sheet1']['coords']
print(dataset_title)
print(sheet_name)
print(col_names)
print(coords)

tbl = extract_table([t for t in sheets if t.name == 'table 1'][0], 
        coords[0], coords[1], coords[2], coords[3], 
        col_names[0], col_names[1], col_names[2])
tbl

tbl['Period'].unique()


