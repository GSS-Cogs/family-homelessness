# -*- coding: utf-8 -*-
# # SG Housing Options  PREVENT1  Statistics in Scotland 

# +
import pandas as pd
import numpy as np
import json 

from gssutils import * 

# -

infoFileName = 'info.json'
info    = json.load(open(infoFileName))
scraper = Scraper(seed=infoFileName)
cubes   = Cubes(infoFileName)
scraper.dataset.family = info['families']

scraper

scraper.distribution(latest=True)

ws = {tab.name: tab for tab in scraper.distribution(latest=True).as_databaker()}


def wrap(tab: xypath.xypath.Table, x_bag: xypath.xypath.Bag, y_bag: xypath.xypath.Bag, val_bag: xypath.xypath.Bag, x_name: str, y_name: str):
    cd_title = tab.excel_ref('A1').value

    dimensions = [
        HDim(y_bag, y_name, DIRECTLY, LEFT),
        HDim(x_bag, x_name, DIRECTLY, ABOVE),
        HDimConst('measure', cd_title)
    ]

    return ConversionSegment(tab, dimensions, val_bag).topandas()


df = pd.DataFrame()

# +
# Table 1
tab = ws['Table 1']

geographies = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = geographies.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geographies, y_name='geography', val_bag=values)

tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[:4]}-20{x[-2:]}")
tmp_df['measure'] = 'Households making PREVENT1 approaches'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, period, values, tmp_df

# +
# Table 2: Unique households making PREVENT1 approaches, 2019/20
tab = ws['Table 2']

geographies = tab.filter('Scotland').expand(DOWN).is_not_blank()
drop = tab.filter('Unique household approaches').shift(DOWN)
values = geographies.waffle(drop)

tmp_df = wrap(tab=tab, x_bag=drop, x_name='drop', y_bag=geographies, y_name='geography', val_bag=values)

tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_df['measure'] = 'Unique households making PREVENT1 approaches'
tmp_df.drop('drop', axis=1, inplace=True)

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, drop, values, tmp_df



# +
# Table 3: Number of PREVENT1 approaches made by households, 2019/20
tab = ws['Table 3']

geographies = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.')
approaches = tab.filter('b) Percentage').shift(DOWN).shift(DOWN).shift(LEFT).expand(LEFT).is_not_blank()
values = geographies.waffle(approaches)

tmp_df = wrap(tab=tab, x_bag=approaches, x_name='approaches', y_bag=geographies, y_name='geography', val_bag=values)

tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_df['measure'] = tmp_df['approaches']
tmp_df.drop('approaches', axis=1, inplace=True)

tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, approaches, values, tmp_df


# +
# Table 4: Number of open PREVENT1 approaches as at 31st March, 2015 to 2020
tab = ws['Table 4']

geographies = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = geographies.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geographies, y_name='geography', val_bag=values)

# This is a specific measurement date
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/date/{x[:4]}-03-31")

tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, period, values, tmp_df

# +
# Table 5: Number of PREVENT1 approaches by property of applicant, 2014/15 to 2019/20
tab = ws['Table 5']

properties = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = properties.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=properties, y_name='properties', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'Number of PREVENT1 approaches'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, properties, period, values, tmp_df

# +
# Table 6: Reason for PREVENT1 approach, 2014/15 to 2019/20
# This one is nested, so have to do it the old way
tab = ws['Table 6']

reasons = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = reasons.waffle(period)
headers = (tab.filter('All') | tab.filter('Homeless Type reasons') | tab.filter('Prevent type reasons') | tab.filter('Other')) - tab.filter('b) Percentage').expand(DOWN)

dimensions = [
    HDim(reasons, 'reason', DIRECTLY, LEFT),
    HDim(period, 'period', DIRECTLY, ABOVE),
    HDim(headers, 'reason classification', CLOSEST, ABOVE),
    HDimConst('measure', tab.excel_ref('A1').value)
]

tmp_df = ConversionSegment(values, dimensions).topandas()

# Date format
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clean up the measure a bit
tmp_df['measure'] = 'Reason for PREVENT1 approach'

# Marker
tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tmp_df, tab, reasons, period, values, headers, dimensions


# +
# Table 7: Reason for PREVENT1 approach by local authority, 2019/20
tab = ws['Table 7']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
reason = tab.filter('a) Number').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geography.waffle(reason)

tmp_df = wrap(tab=tab, x_bag=reason, x_name='reason', y_bag=geography, y_name='geography', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'Reason of PREVENT1 approaches'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

# Marker
tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, reason, values, tmp_df

# +
# Table 8: Number of PREVENT1 approaches by property of applicant, 2014/15 to 2019/20
tab = ws['Table 8']

prevention = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Applicants may select multiple responses, which is why total figures are greater than the number of approaches').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = prevention.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=prevention, y_name='prevention', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'Prevention activities carried out'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, prevention, period, values, tmp_df

# +
# Table 9: Prevention activities carried out by local authority, 2019/20
tab = ws['Table 9']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
prevention = tab.filter('a) Number').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geography.waffle(prevention)

tmp_df = wrap(tab=tab, x_bag=prevention, x_name='prevention', y_bag=geography, y_name='geography', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'Prevention activities carried out'

# Marker
tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, prevention, values, tmp_df

# +
# Table 10: Organisation carrying out prevention activities, 2014/15 to 2019/20
tab = ws['Table 10']

organisation = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('NNote: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = organisation.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=organisation, y_name='organisation', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'Organisation carrying out prevention activites'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

# Marker
tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, organisation, period, values, tmp_df

# +
# Table 11: Maximum type of activity, 2014/15 to 2019/20
tab = ws['Table 11']

activity_tier = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = activity_tier.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=activity_tier, y_name='activity_tier', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'maximum-activity-tier'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, activity_tier, period, values, tmp_df

# +
# Table 12: Maximum type of activity by local authority, 2019/20
tab = ws['Table 12']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
activity_tier = tab.filter('b) Percentage').shift(DOWN).shift(DOWN).shift(LEFT).expand(LEFT).is_not_blank()
values = geography.waffle(activity_tier)

tmp_df = wrap(tab=tab, x_bag=activity_tier, x_name='activity tier', y_bag=geography, y_name='geography', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'maximum-activity-tier'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

# Marker
tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, activity_tier, values, tmp_df

# +
# Table 13: Outcome of PREVENT1 approach, 2014/15 to 2019/20
tab = ws['Table 13']

outcome = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = outcome.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=outcome, y_name='outcome', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'outcomes'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, outcome, period, values, tmp_df

# +
# Table 14: Maximum type of activity by local authority, 2019/20
tab = ws['Table 14']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
outcome = tab.filter('a) Number').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geography.waffle(outcome)

tmp_df = wrap(tab=tab, x_bag=outcome, x_name='outcome', y_bag=geography, y_name='geography', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'outcomes'

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

# Marker
tmp_df['marker'] = 'Figures have been rounded to the nearest 5 for disclosure control purposes'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, outcome, values, tmp_df

# +
# Table 15: Average time taken (days) to complete PREVENT1 approach by local authority, 2019/20
tab = ws['Table 15']

geography = tab.filter('Scotland').expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Scotland').shift(UP).expand(RIGHT).is_not_blank()
values = geography.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geography, y_name='geography', val_bag=values)

# Date format
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"/id/government-year/{x[-7:-3]}-20{x[-2:]}")

# Clear up the measure a bit
tmp_df['measure'] = 'days to complete PREVENT1 approach'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, period, values, tmp_df
# -

df

# Column name formatting
df.rename({'OBS': 'Value'}, axis=1, inplace=True)
df.rename(columns=lambda x: pathify(x), inplace=True)

for col in df.columns:
    if col != 'Value':
        df[col] = df[col].astype('category')

# Geograpy fix
map = {
    'Scotland': 'S04000001',
    'Aberdeen City': 'S05000001',
    'Aberdeenshire': 'S05000002',
    'Angus': 'S05000003',
    'Argyll & Bute': 'S05000004',
    'Clackmannanshire': 'S05000005',
    'Dumfries & Galloway': 'S05000006',
    'Dundee City': 'S05000007',
    'East Ayrshire': 'S05000008',
    'East Dunbartonshire': 'S05000009',
    'East Lothian': 'S05000010',
    'East Renfrewshire': 'S05000011',
    'Edinburgh': 'S05000012',
    'Eilean Siar': 'S12000013',
    'Falkirk': 'S05000013',
    'Fife': 'S05000014',
    'Glasgow City': 'S05000015',
    'Highland': 'S05000016',
    'Inverclyde': 'S05000017',
    'Midlothian': 'S05000018',
    'Moray': 'S12000020',
    'North Ayrshire': 'S05000019',
    'North Lanarkshire': 'S05000020',
    'Orkney': 'S08000025',
    'Perth & Kinross': 'S05000021',
    'Renfrewshire': 'S05000022',
    'Scottish Borders': 'S12000026',
    'Shetland': 'S05000023',
    'South Ayrshire': 'S05000025',
    'South Lanarkshire': 'S05000026',
    'Stirling': 'S05000024',
    'West Dunbartonshire': 'S05000027',
    'West Lothian': 'S05000028'
}
df['geography'].cat.rename_categories(lambda x: f"http://statistics.data.gov.uk/id/statistical-geography/{map[x]}", inplace=True)

df.geography.value_counts()

for col in df.columns:
    if col not in ('value','geography','period'):
        df[col].cat.rename_categories(lambda x: pathify(x), inplace=True)

# Add dataframe is in the cube
cubes.add_cube(scraper, df, scraper.title)

# Write cube
cubes.output_all()


