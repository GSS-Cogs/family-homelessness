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


def extract_table(tab, ref1, ref2, ref3, ref4, ref5, ref6, ref7, title1, title2, title3, title4, title5, title6):
    try:
        col1 = tab.excel_ref(ref1).fill(DOWN).is_not_blank()
        col2 = tab.excel_ref(ref2).fill(DOWN).is_not_blank()
        col3 = tab.excel_ref(ref3).fill(DOWN).is_not_blank()
        col4 = tab.excel_ref(ref4).expand(RIGHT).is_not_blank() 
        col5 = tab.excel_ref(ref5).expand(RIGHT).is_not_blank() 
        col6 = tab.excel_ref(ref6).expand(RIGHT).is_not_blank() 
        col7 = tab.excel_ref(ref7).is_not_blank()

        Dimensions = [
            HDim(col1,title1, DIRECTLY, LEFT),
            HDim(col2,title2, DIRECTLY, LEFT),
            HDim(col3,title3, DIRECTLY, LEFT),
            HDim(col4,title4, DIRECTLY, ABOVE),
            HDim(col5,title5, DIRECTLY, ABOVE),
            HDim(col6,title6, DIRECTLY, ABOVE)
            ]

        c1 = ConversionSegment(col7, Dimensions, processTIMEUNIT=True)
        tbl = c1.topandas()
        
        # Get rid of any columns that have the word Spare in their name as they are not needed
        for col in tbl.columns:
            if 'Spare' in col:
                tbl = tbl.drop(col, 1)
                
        return tbl
    except Exception as e:
        return "extract_sheet: " + str(e)   


tbl_set = []
no_of_datasets = int(info['noofdatasets'])
for x in range(no_of_datasets):
    x = x + 1
    no_of_sheets = int(info['dataset' + str(x)]['noofsheets'])
    for y in range(no_of_sheets):
        try:
            y = y + 1
            dataset_title = info['dataset' + str(x)]['name'] 
            sheet_name = info['dataset' + str(x)]['sheet' + str(y)]['name']
            col_names = info['dataset' + str(x)]['sheet' + str(y)]['columnnames']
            coords = info['dataset' + str(x)]['sheet' + str(y)]['coords']
            print('Title: ' + dataset_title + ' - Sheet Name: ' + sheet_name)
            print(col_names)
            print(coords)

            tbl = extract_table([t for t in sheets if t.name == sheet_name][0], 
                    coords[0], coords[1], coords[2], coords[3], coords[4], coords[5], coords[6],  
                    col_names[0], col_names[1], col_names[2], col_names[3], col_names[4], col_names[5])
            tbl_set.append(tbl)
            del tbl
        except Exception as e:
            print('Error: ' + str(e))

# Get all the unique column names
col_set = []
for t in tbl_set:
    for c in t.columns:
        if c not in col_set:
            col_set.append(c)
col_set

# +
# Add missing columns to each table and reorder all the tables to have the same structure and then concat
i = 0

for t in tbl_set:
    for l in col_set:
        if l not in t.columns:
            t[l] = 'All'
    tbl_set[i] = t[col_set]
    print('Table ' + str(i))
    print(tbl_set[i].columns)
    i = i + 1
    
main_tbl = pd.concat(tbl_set)
# -

# Display unique values to ensure everythng has been included
for c in main_tbl.columns:
    if 'OBS' not in c:
        print(c)
        print(main_tbl[c].unique())

# Rename, add column and reorder
main_tbl = main_tbl.rename(columns={'OBS': 'Value'})
main_tbl['Measure Type'] = ''
main_tbl['Unit'] = ''
main_tbl['Marker'] = ''
main_tbl = main_tbl[['Period', 'ONS Geography Code', 'Nationality', 'Age', 'Gender', 'Measure Type', 'Unit', 'Marker', 'Value']]

main_tbl.head(60)


