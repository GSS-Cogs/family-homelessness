#!/usr/bin/env python
# coding: utf-8

# In[95]:


# # MHCLG Rough sleeping

from gssutils import *
import json

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]


# In[96]:


#### Add transformation script here ####

trace = TransformTrace()

scraper = Scraper(seed="info.json")
wanted = [x.title for x in scraper.distributions if "rough sleeping" in x.title.lower()]
assert len(wanted) == 1, 'Aborting, more than 1 "Rough sleeping" source file found'
distro = scraper.distribution(title=wanted[0])
distro


# In[97]:


cubes = Cubes("info.json")

# We're expecting exactly 4 sheets, track them and blow up if we're
# mising any
sheets_transformed = 0

for tab in distro.as_databaker():
    try:
        if tab.name == "Table 1 Total":

            trace.start("mhclg-rough-sleeping", tab.name, ["Value", "Period", "Region", "Area"], distro.downloadURL)

            trace.Area("Everything below the cell 'Local authority ONS code'.")
            area = tab.filter("Local authority ONS code").assert_one().fill(DOWN)

            trace.Region("Everything below the cell 'Region ONS code'.")
            region = tab.filter("Region ONS code").assert_one().fill(DOWN).is_not_blank().is_not_whitespace()

            trace.Period('Everything to the right of "Region ONS code"')
            period = tab.filter("Region ONS code").assert_one().fill(RIGHT)
            [int(x.value) for x in period] # If this blows up, one of our selected "period" values aint a year

            obs = period.waffle(region).is_not_blank().is_not_whitespace()

            dimensions = [
                HDim(period, "Period", DIRECTLY, ABOVE),
                HDim(area, "Area", DIRECTLY, LEFT),
                HDim(region, "Region", DIRECTLY, LEFT)
            ]

            cs = ConversionSegment(tab, dimensions, obs)
            df = cs.topandas()
            df = df.fillna('')

            # Where the data is at Region level, bring over the Area then
            # drop the unnecessary Region column
            df["Area"][df["Area"] == ""] = df["Region"]
            df = df.drop("Region", axis=1)

            df = df.rename(columns={"OBS": "Value"})

            df["Sex"] = "all"
            df["Nationality"] = "all"
            df["Age"] = "all"

            df["Measure Type"] = "people"
            df["Unit"] = "count"

            trace.store("MHCLG Rough Sleeping Final", df)


        # All the Table2's are the same structure, we're just going to take
        # the "metric" (thing what its talking about) from the tab name
        if tab.name.lower().strip().startswith("table 2"):

            metric_name = tab.name.split(" ")[-1].strip()
            metric_name = "Sex" if metric_name == "Gender" else metric_name

            trace.start("mhclg-rough-sleeping", tab.name, ["Value", "Period", "Region", "Area", metric_name], distro.downloadURL)

            trace.Area("Everything below the cell 'Local authority ONS code'.")
            area = tab.filter("Local authority ONS code").assert_one().fill(DOWN)

            trace.Region("Everything below the cell 'Region ONS code'.")
            region = tab.filter("Region ONS code").assert_one().fill(DOWN).is_not_blank().is_not_whitespace()

            trace.Period('From the single year values above the obvious header row')
            period = tab.filter("Region ONS code").assert_one().shift(UP).fill(RIGHT).is_not_blank().is_not_whitespace()
            [int(x.value) for x in period] # If this blows up, one of our selected "period" values aint a year

            metric_data = tab.filter("Region ONS code").assert_one().fill(RIGHT)
            trace.multi([metric_name], 'Taken as the values to the right of "Region ONs code".')

            obs = region.waffle(metric_data).is_not_blank().is_not_whitespace()

            dimensions = [
                HDim(period, "Period", CLOSEST, LEFT),
                HDim(area, "Area", DIRECTLY, LEFT),
                HDim(region, "Region", DIRECTLY, LEFT),
                HDim(metric_data, metric_name, DIRECTLY, ABOVE)
            ]

            cs = ConversionSegment(tab, dimensions, obs)
            df = cs.topandas()
            df = df.fillna('')

            df[metric_name] = df[metric_name].apply(pathify)
            trace.multi([metric_name], f"Pathified all values in the {metric_name} column")

            # Where the data is at Region level, bring over the Area then
            # drop the unnecessary Region column
            df["Area"][df["Area"] == ""] = df["Region"]
            df = df.drop("Region", axis=1)

            # Fill out the alls
            if "Sex" not in df.columns.values:
                df["Sex"] = "all"

            if "Nationality" not in df.columns.values:
                df["Nationality"] = "all"

            if "Age" not in df.columns.values:
                df["Age"] = "all"

            df["Measure Type"] = "people"
            df["Unit"] = "count"

            indexNames = df[ df['Sex'] == 'total' ].index
            df.drop(indexNames, inplace = True)

            indexNames = df[ df['Nationality'] == 'total' ].index
            df.drop(indexNames, inplace = True)

            indexNames = df[ df['Age'] == 'total' ].index
            df.drop(indexNames, inplace = True)

            #The total values are all included in the table 1 tab

            df = df.rename(columns={"OBS": "Value"})
            trace.store("MHCLG Rough Sleeping Final", df)

    except Exception as err:
        raise Exception(f'Issue encountered on tab {tab.name}, see above for details.') from err


# In[98]:


df = trace.combine_and_trace("MHCLG Rough Sleeping Final", "MHCLG Rough Sleeping Final")
df["Period"] = df["Period"].map(lambda x: "year/"+left(x, 4))

df = df.rename(columns={'Area' : 'Region'})

indexNames = df[ df['Region'] == '-' ].index
df.drop(indexNames, inplace = True)

df = df.replace({'Sex' : {'male' : 'm',
                          'female' : 'f',
                          'all' : 't',
                          'total' : 't'},
                 'Nationality' : {'total' : 'all'},
                 'Age' : {'total' : 'all'}})

df['Value'] = df['Value'].astype(float).astype(int)

df = df.drop(['Measure Type', 'Unit'], axis=1)


# In[99]:


scraper.dataset.title = 'Rough Sleeping Snapshot in England'
scraper.dataset.comment = 'Annual statistical release evaluating the extent of rough sleeping'

cubes.add_cube(scraper, df, "observations")
cubes.output_all()
trace.output()


# In[100]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)








