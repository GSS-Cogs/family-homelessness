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

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'

df = df.append(tmp_df, ignore_index=True, sort=False)

del tmp_df, tab, reasons, period, values, headers, dimensions

# -

df

tab.excel_ref('A8')


