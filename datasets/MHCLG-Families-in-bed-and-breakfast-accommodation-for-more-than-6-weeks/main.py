#!/usr/bin/env python
# coding: utf-8

# In[563]:


# # MHCLG Families in bed and breakfast accommodation for more than 6 weeks


# In[564]:


import json
import logging

from dateutil.parser import parse
from rdflib import Graph
import requests

from gssutils import *

trace = TransformTrace()
cubes = Cubes("info.json")


# In[565]:


scraper = Scraper(seed="info.json")
distro = scraper.distribution(latest=True)
distro


# In[566]:


from dateutil.parser import parse
from rdflib import Graph
import logging

class GeoCodeFinder:

    def __init__(self, choices=None):
        self.choices = choices
        self.has_had_warning = []
        self.graph = Graph()
        self.graph.parse("https://raw.githubusercontent.com/GSS-Cogs/de-resources/main/lookups/geography.ttl", format="ttl")

        lookups = {}
        for s, o, p in self.graph:
            if str(o) == 'http://statistics.data.gov.uk/def/statistical-geography#officialname' or                  str(o) == 'http://publishmydata.com/def/ontology/foi/displayName':

                code = s.split('/')[-1]
                label = p.split('/')[-1]

                if label in lookups.keys():
                    if code not in lookups[label]:
                        lookups[label].append(code)
                else:
                    lookups[label] = [code]

        self.lookups = lookups

    def __call__(self, cell_val):
        cell_val = cell_val.strip()

        if self.choices is not None:
            if cell_val in self.choices.keys():
                return self.choices[cell_val]

        codes = self.lookups.get(cell_val, None)
        if codes is None:
            if cell_val not in self.has_had_warning:
                logging.warning(f'Unable to find code for label {cell_val}.\nPlease specifiy what you want to use '                                + f'by passing in a dictionary, eg "GeoCodeFinder(choices={{"{cell_val}":"Z123456789"}})"\n')
                self.has_had_warning.append(cell_val)
            return cell_val

        if len(codes) > 1:
            if cell_val not in self.has_had_warning:
                logging.warning(f'The label {cell_val} has {len(codes)} possible codes as follows" {codes}.\nPlease specify which you want to use'                                 + f'by passing in a dictionary, eg "GeoCodeFinder(choices={{"{cell_val}":"{codes[0]}"}})"\n')
                self.has_had_warning.append(cell_val)
            return cell_val

        return codes[0]


def format_period(time_val, tab_name):
    """
    Given a timeformatted as per the following examples:
    "As at 30 September 2007"
    "As at 30 June 2007"

    Return formatted as periods:
    /day/{year}-{month}-{day}
    """
    try:
        time_val_without_asat = " ".join(time_val.split(" ")[2:])
        time_obj = parse(time_val_without_asat)
        return time_obj.strftime('day/%Y-%m-%d')
    except Exception as err:
        raise Exception('Aborting. Unable to format value "{time_val}" from tab {tab_name} as period.') from err


def excel_range(bag):
    """Get the furthermost tope-left and bottom-right cells of a given selection"""
    min_x = min([cell.x for cell in bag])
    max_x = max([cell.x for cell in bag])
    min_y = min([cell.y for cell in bag])
    max_y = max([cell.y for cell in bag])
    top_left_cell = xypath.contrib.excel.excel_location(bag.filter(lambda x: x.x == min_x and x.y == min_y))
    bottom_right_cell = xypath.contrib.excel.excel_location(bag.filter(lambda x: x.x == max_x and x.y == max_y))
    return f"{top_left_cell}:{bottom_right_cell}"


# In[567]:


# # Note: Geography
#
# When you run the below cell it'll attempt to identify the correct 9 digit Geography codes using our label:code mappings for geography.
#
# This fails in two scenarios:
#
#   * More than one code for a label.
#   * No codes for a label.
#
#
# This will show up as warnings, asking you what code you you want use.
#
# You specify it with a dictionary (called `choices` in the below cell).
#
# It'll make sense when you run it, but basically when you know what code you want to use to represent a given label - stick it in the `choices` dictionary and it'll just work..


# In[568]:


# Data marker for where an authority has not submitted data
missing_marker = 'no-data-submitted'

for tab in distro.as_databaker():

    try:

        trace.start("mhclg-families-in-bed-and-breakfast-accommodation-for-more-than-6-weeks", tab.name,
            ["Value", "Marker", "Period", "Family Accommodation" ,"Area"], distro.downloadURL)

        # Anchor to authority in column A as out generic start point
        anchor = tab.excel_ref('A').filter(contains_string("Authority")).assert_one()

        period = anchor.fill(UP).filter(contains_string("As at")).assert_one().expand(RIGHT).is_not_blank().is_not_whitespace()
        trace.Period('Extracted from the stated "As at...." entries near the top of the sheet.', excel_range(period))

        area = period.fill(DOWN).is_not_blank().is_not_whitespace() - anchor.expand(RIGHT)
        trace.Area("Area taken as the places stated beneath the word 'Authority'.")

        family_accommodation = anchor.expand(RIGHT) - area.expand(UP)
        trace.Family_Accommodation('Fields taken from alongside (but not including) "Authority".', excel_range(family_accommodation))

        trace.obs('Taken as cells that can be cross referenced from the "Area" and "Family Accommodation" selections.')
        obs = family_accommodation.waffle(area).is_not_blank().is_not_whitespace()

        dimensions = [
            HDim(period, "Period", CLOSEST, LEFT),
            HDim(family_accommodation, "Family Accommodation", DIRECTLY, ABOVE),
            HDim(area, "Area", DIRECTLY, LEFT)
        ]

        cs = ConversionSegment(tab, dimensions, obs)

        df = cs.topandas()
        df = df.fillna('')
        trace.store("MHCLG Final", df)

    except Exception as err:
        raise Exception(f'Failed on processing tab {tab.name}') from err

# Combine all tabs, then post process
df = trace.combine_and_trace('MHCLG Final', 'MHCLG Final')
df = df.rename(columns={"OBS": "Value", "DATAMARKER": "Marker"})
df


# In[569]:


# The non submitting authrorities will show in the data marker column at this point,
# move them to area before looking up codes

df["Area"][df["Marker"] != ''] = df["Marker"]
df["Marker"][df["Marker"] != ''] = missing_marker

# Replace 'Authorities that did not submit a figure' with a "missing" data marker for both Family Accomodation dimension options
data_frame = df.copy()[df["Marker"] == ""]
marker_frame1 = df.copy()[df["Marker"] != ""]
marker_frame2 = df.copy()[df["Marker"] != ""]
marker_frame1["Family Accommodation"] = 'Number of families in B&B accommodation for 6 or more weeks'
marker_frame2["Family Accommodation"] = 'Number of families in B&B accommodation for 6 or more weeks not pending a review or appeal'
df = pd.concat([data_frame, marker_frame1, marker_frame2])
trace.multi(["Family_Accommodation", "Marker"], f'Replace each "Authorities that did not submit a figure" with a "{missing_marker}" '                             + 'against each Family Accommodation option')

df["Family Accommodation"] = df["Family Accommodation"].apply(pathify)
trace.Family_Accommodation('Pathify all values')
df


# In[570]:


df['Family Accommodation'] = df.apply(lambda x: 'number-of-families-in-b-b-accommodation-for-6-or-more-weeks-not-pending-a-review-or-appeal' if '(not pending review or appeal)' in x['Area'] else x['Family Accommodation'], axis = 1)
df['Area'] = df.apply(lambda x: x['Area'].replace('(not pending review or appeal)', '').strip(), axis = 1)

indexNames = df[df['Area'].isin(['unknown']) ].index
df.drop(indexNames, inplace = True)

df = df.replace({'Area' : {'Shropshire' : 'E06000051',
                           'Isle Of Wight' : 'E06000046',
                           'Cornwall_UA' : 'E06000052',
                           'Medway Towns' : 'E06000035'}})

# ---- GEOGRAPHY CODES ----
choices = {"Gateshead":"E08000020"}
df['Area'] = df['Area'].apply(GeoCodeFinder(choices=choices))
trace.Area('Replace Area names with 9 digit geography codes')

# Format the periods
df["Period"] = df["Period"].map(lambda x: format_period(x, tab.name))
trace.Period('Format period as per standard intervals')

df['Value'] = pd.to_numeric(df['Value'], errors='coerce').astype('Int64')

df = df.drop_duplicates()


# In[571]:


df = df.reset_index()
df = df.drop(df.loc[(df['Marker'] == 'no-data-submitted') & (df['Period'] == 'day/2009-03-31') & (df['Area'] == 'E09000009') & (df['Family Accommodation'] == 'number-of-families-in-b-b-accommodation-for-6-or-more-weeks')].index[0])
df = df.reset_index(drop=True, inplace=True)
#Irregularity in the data (missing parenthesis), needs to be manually removed)


# In[572]:


cubes.add_cube(scraper, df, "observations")
cubes.output_all()

trace.render()

df


# In[ ]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)

