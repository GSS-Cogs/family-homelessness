#!/usr/bin/env python
# coding: utf-8

# In[770]:


# -*- coding: utf-8 -*-
# # SG Housing Options  PREVENT1  Statistics in Scotland


# In[771]:


import pandas as pd
import numpy as np
import json

from gssutils import *


# In[772]:


infoFileName = 'info.json'
info    = json.load(open(infoFileName))
scraper = Scraper(seed=infoFileName)
cubes   = Cubes(infoFileName)
scraper.dataset.family = info['families']

scraper


# In[773]:


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


# In[774]:


# Table 1
tab = ws['Table 1']

geographies = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = geographies.waffle(period)
tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geographies, y_name='geography', val_bag=values)
tmp_dfCount['unit'] = 'household'

geographies = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank()
values = geographies.waffle(period)
tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geographies, y_name='geography', val_bag=values)
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period'])

tmp_df['period'] = tmp_df['period'].apply(lambda x: f"government-year/{x[:4]}-20{x[-2:]}")
tmp_df['measure'] = 'approaches'

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[775]:


# Table 2: Unique households making PREVENT1 approaches, 2019/20
tab = ws['Table 2']

geographies = tab.filter('Scotland').expand(DOWN).is_not_blank()
drop = tab.filter('Unique household approaches').expand(RIGHT).shift(DOWN)
values = geographies.waffle(drop)

tmp_df = wrap(tab=tab, x_bag=drop, x_name='drop', y_bag=geographies, y_name='geography', val_bag=values)

tmp_df['period'] = tmp_df['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")

replace = {'Number' : 'Unique approaches',
           'Rate per 1,000 population' : 'Rate of Approaches per 1,000 households'}

indexNames = tmp_df[ tmp_df['drop'] == 'As proportion of Scotland' ].index
tmp_df.drop(indexNames, inplace = True)
tmp_df.drop('measure', axis=1, inplace=True)
tmp_df = tmp_df.rename(columns={'drop' : 'measure'})
tmp_df = tmp_df.assign(measure= tmp_df['measure'].map(replace))
tmp_df['unit'] = tmp_df.apply(lambda x: 'rate' if 'Rate' in x['measure'] else 'household', axis = 1)

geographies = tab.filter('Scotland').expand(DOWN).is_not_blank()
drop = tab.filter('Rate per 1,000 population').shift(LEFT)
values = geographies.waffle(drop)
tmp_dfPercent = wrap(tab=tab, x_bag=drop, x_name='drop', y_bag=geographies, y_name='geography', val_bag=values)
tmp_dfPercent = tmp_dfPercent.drop(columns=['drop', 'measure'])
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})

tmp_df = pd.merge(tmp_df, tmp_dfPercent, how="left", on=['geography'])

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, drop, values, tmp_df


# In[776]:


# Table 3: Number of PREVENT1 approaches made by households, 2019/20
tab = ws['Table 3']

geographies = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.')
approaches = tab.filter('b) Percentage').shift(DOWN).shift(DOWN).shift(LEFT).expand(LEFT).is_not_blank()
values = geographies.waffle(approaches)

tmp_dfCount = wrap(tab=tab, x_bag=approaches, x_name='approaches', y_bag=geographies, y_name='geography', val_bag=values)
tmp_dfCount['period'] = tmp_dfCount['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

approaches = tab.filter('b) Percentage').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geographies.waffle(approaches)

tmp_dfPercent = wrap(tab=tab, x_bag=approaches, x_name='approaches', y_bag=geographies, y_name='geography', val_bag=values)
tmp_dfPercent['period'] = tmp_dfPercent['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period', 'approaches'])

replace = {'Households making one approach only' : '1',
           'Households making two approaches only' : '2',
           'Households making three or more approaches' : '3 plus',
           'All' : 'All'}

tmp_df = tmp_df.assign(approaches= tmp_df['approaches'].map(replace))
tmp_df = tmp_df.rename(columns={'approaches' : 'number of approaches'})

indexNames = tmp_df[ (tmp_df['number of approaches'] == 'All') ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, approaches, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[777]:


# Table 4: Number of open PREVENT1 approaches as at 31st March, 2015 to 2020
tab = ws['Table 4']

geographies = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = geographies.waffle(period)

tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geographies, y_name='geography', val_bag=values)

# This is a specific measurement date
tmp_dfCount['period'] = tmp_dfCount['period'].apply(lambda x: f"day/{x[:4]}-03-31")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

geographies = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank()
values = geographies.waffle(period)

tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geographies, y_name='geography', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['period'].apply(lambda x: f"day/{x[:4]}-03-31")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period'])

tmp_df['approach status'] = 'open'

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geographies, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[778]:


# Table 5: Number of PREVENT1 approaches by property of applicant, 2014/15 to 2019/20
tab = ws['Table 5']

properties = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = properties.waffle(period)

tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=properties, y_name='properties', val_bag=values)

tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

properties = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank()
values = properties.waffle(period)

tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=properties, y_name='properties', val_bag=values)
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['period', 'properties'])

# Geography is Scotland-wide
tmp_df['geography'] = 'Scotland'
tmp_df['period'] = tmp_df['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")

indexNames = tmp_df[ tmp_df['properties'] == 'All' ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, properties, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[779]:


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

tmp_dfCount = ConversionSegment(values, dimensions).topandas()

tmp_dfCount['period'] = tmp_dfCount['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

reasons = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank()
values = reasons.waffle(period)
headers = (tab.filter('All') | tab.filter('Homeless Type reasons') | tab.filter('Prevent type reasons') | tab.filter('Other')) - tab.filter('b) Percentage').expand(UP)

dimensions = [
    HDim(reasons, 'reason', DIRECTLY, LEFT),
    HDim(period, 'period', DIRECTLY, ABOVE),
    HDim(headers, 'reason classification', CLOSEST, ABOVE),
    HDimConst('measure', tab.excel_ref('A1').value)
]

tmp_dfPercent = ConversionSegment(values, dimensions).topandas()

tmp_dfPercent['period'] = tmp_dfPercent['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['period', 'reason', 'reason classification'])

tmp_df['geography'] = 'Scotland'

indexNames = tmp_df[ tmp_df['reason classification'] == 'All' ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tmp_df, tab, reasons, period, values, headers, dimensions, tmp_dfCount, tmp_dfPercent


# In[780]:


# Table 7: Reason for PREVENT1 approach by local authority, 2019/20
tab = ws['Table 7']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
reason = tab.filter('a) Number').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geography.waffle(reason)

tmp_dfCount = wrap(tab=tab, x_bag=reason, x_name='reason', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

geography = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(UP)
values = geography.waffle(reason)

tmp_dfPercent = wrap(tab=tab, x_bag=reason, x_name='reason', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period', 'reason'])

indexNames = tmp_df[ (tmp_df['reason'] == 'All') ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, reason, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[781]:


# Table 8: Number of PREVENT1 approaches by property of applicant, 2014/15 to 2019/20
tab = ws['Table 8']

prevention = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Applicants may select multiple responses, which is why total figures are greater than the number of approaches').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = prevention.waffle(period)

tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=prevention, y_name='prevention', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")

tmp_dfCount['measure'] = 'count'
tmp_dfCount['unit'] = 'prevention activity'

prevention = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Applicants may select multiple responses, which is why total figures are greater than the number of approaches').expand(UP)
values = prevention.waffle(period)

tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=prevention, y_name='prevention', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['period', 'prevention'])

tmp_df['geography'] = 'Scotland'

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, prevention, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[782]:


# Table 9: Prevention activities carried out by local authority, 2019/20
tab = ws['Table 9']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
prevention = tab.filter('a) Number').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geography.waffle(prevention)

tmp_dfCount = wrap(tab=tab, x_bag=prevention, x_name='prevention', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'count'
tmp_dfCount['unit'] = 'prevention activity'

geography = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(UP)
values = geography.waffle(prevention)

tmp_dfPercent = wrap(tab=tab, x_bag=prevention, x_name='prevention', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period', 'prevention'])

indexNames = tmp_df[ tmp_df['geography'] == 'Scotland' ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, prevention, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[783]:


# Table 10: Organisation carrying out prevention activities, 2014/15 to 2019/20
tab = ws['Table 10']

organisation = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = organisation.waffle(period)

tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=organisation, y_name='organisation involved', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'count'
tmp_dfCount['unit'] = 'prevention activity'

organisation = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(UP)
values = organisation.waffle(period)

tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=organisation, y_name='organisation involved', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['period', 'organisation involved'])

tmp_df['geography'] = 'Scotland'

indexNames = tmp_df[ tmp_df['organisation involved'] == 'All' ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, organisation, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[784]:


# Table 11: Maximum type of activity, 2014/15 to 2019/20
tab = ws['Table 11']

activity_tier = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = activity_tier.waffle(period)

tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=activity_tier, y_name='activity tier', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

activity_tier = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank()
values = activity_tier.waffle(period)

tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=activity_tier, y_name='activity tier', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['period', 'activity tier'])

tmp_df['geography'] = 'Scotland'

indexNames = tmp_df[ tmp_df['activity tier'] == 'All' ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, activity_tier, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[785]:


# Table 12: Maximum type of activity by local authority, 2019/20
tab = ws['Table 12']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
activity_tier = tab.filter('b) Percentage').shift(DOWN).shift(DOWN).shift(LEFT).expand(LEFT).is_not_blank()
values = geography.waffle(activity_tier)

tmp_dfCount = wrap(tab=tab, x_bag=activity_tier, x_name='activity tier', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
activity_tier = tab.filter('b) Percentage').shift(0, 2).expand(RIGHT).is_not_blank()
values = geography.waffle(activity_tier)

tmp_dfPercent = wrap(tab=tab, x_bag=activity_tier, x_name='activity tier', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period', 'activity tier'])

indexNames = tmp_df[ (tmp_df['geography'] == 'All')].index
tmp_df.drop(indexNames, inplace = True)

indexNames = tmp_df[ (tmp_df['activity tier'] == 'All')].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, activity_tier, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[786]:


# Table 13: Outcome of PREVENT1 approach, 2014/15 to 2019/20
tab = ws['Table 13']

outcome = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Number').shift(LEFT).expand(LEFT).is_not_blank()
values = outcome.waffle(period)

tmp_dfCount = wrap(tab=tab, x_bag=period, x_name='period', y_bag=outcome, y_name='approach outcome', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

outcome = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank()
values = outcome.waffle(period)

tmp_dfPercent = wrap(tab=tab, x_bag=period, x_name='period', y_bag=outcome, y_name='approach outcome', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['period', 'approach outcome'])

tmp_df['geography'] = 'Scotland'
tmp_df['approach status'] = 'closed'

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, outcome, period, values, tmp_df, tmp_dfCount, tmp_dfPercent


# In[787]:


# Table 14: Maximum type of activity by local authority, 2019/20
tab = ws['Table 14']

geography = tab.filter('a) Number').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(DOWN)
outcome = tab.filter('a) Number').shift(DOWN).shift(DOWN).expand(RIGHT).is_not_blank()
values = geography.waffle(outcome)

tmp_dfCount = wrap(tab=tab, x_bag=outcome, x_name='approach outcome', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfCount['period'] = tmp_dfCount['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfCount['measure'] = 'approaches'
tmp_dfCount['unit'] = 'household'

geography = tab.filter('b) Percentage').shift(DOWN).expand(DOWN).is_not_blank() - tab.filter('Note: Figures have been rounded to the nearest 5 for disclosure control purposes.').expand(UP)
values = geography.waffle(outcome)

tmp_dfPercent = wrap(tab=tab, x_bag=outcome, x_name='approach outcome', y_bag=geography, y_name='geography', val_bag=values)

tmp_dfPercent['period'] = tmp_dfPercent['measure'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_dfPercent['OBS'] = tmp_dfPercent['OBS'].apply(lambda x: round(x*100))
tmp_dfPercent = tmp_dfPercent.rename(columns={'OBS' : 'Percentage of Breakdown'})
tmp_dfPercent = tmp_dfPercent.drop(columns=['measure'])

tmp_df = pd.merge(tmp_dfCount, tmp_dfPercent, how="left", on=['geography', 'period', 'approach outcome'])

tmp_df['approach status'] = 'closed'

indexNames = tmp_df[ tmp_df['geography'] == 'Scotland' ].index
tmp_df.drop(indexNames, inplace = True)

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, outcome, values, tmp_df


# In[788]:


# Table 15: Average time taken (days) to complete PREVENT1 approach by local authority, 2019/20
tab = ws['Table 15']

geography = tab.filter('Scotland').expand(DOWN).is_not_blank() - tab.filter('b) Percentage').expand(DOWN)
period = tab.filter('Scotland').shift(UP).expand(RIGHT).is_not_blank()
values = geography.waffle(period)

tmp_df = wrap(tab=tab, x_bag=period, x_name='period', y_bag=geography, y_name='geography', val_bag=values)

tmp_df['measure'] = 'average time to resolve approach'
tmp_df['unit'] = 'days'

percent = {'2014/15' : 40,
           '2015/16' : 82,
           '2016/17' : 117,
           '2017/18' : 150,
           '2018/19' : 103,
           '2019/20' : 105}
tmp_df['percentage'] = tmp_df['period']
tmp_df = tmp_df.assign(percentage= tmp_df['percentage'].map(percent))
tmp_df['percentage'] = tmp_df.apply(lambda x: round((x['OBS']/x['percentage'])*100), axis = 1)

#Theres probably a better way to do this but my brain is soup

tmp_df['period'] = tmp_df['period'].apply(lambda x: f"government-year/{x[-7:-3]}-20{x[-2:]}")
tmp_df = tmp_df.rename(columns={'percentage' : 'Percentage of Breakdown'})

tmp_df['tab'] = tab.name

df = df.append(tmp_df, ignore_index=True, sort=False)

del tab, geography, period, values, tmp_df


# In[789]:


df[['measure', 'unit']].drop_duplicates()

for col in df.columns.values.tolist():
    if col in ['period', 'OBS', 'Percentage of Breakdown']:
        continue
    else:
        df[col] = df[col].astype(str).str.replace('/', 'or')

df


# In[790]:


df = df.rename(columns={'OBS': 'Value'})
df = df.drop(columns = ['tab'])

df = df.rename(columns=lambda x: pathify(x).replace('-', '_'))

df = df.replace({'measure' : {'approaches' : 'cumulative-approaches'}})

for col in df.columns:
    if col not in ['value', 'percentage_of_breakdown']:
        df[col] = df[col].astype('category')

# Geograpy fix
mapping = {
    'All': 'S04000001',
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
df = df.assign(geography = df['geography'].map(mapping))

rep = {'NaN' : 'All'}

for col in df.columns:
    if col not in ['value', 'geography', 'percentage_of_breakdown']:
        df[col] = df[col].cat.add_categories("NaN").fillna("NaN")

df = df.replace({'nan' : 'All'})

df = df.rename({'period' : 'Period',
           'geography' : 'Area',
           'measure' : 'Measure Type',
           'unit' : 'Unit',
           'number_of_approaches' : 'Number of Approaches',
           'approach_status' : 'Approach Status',
           'properties' : 'Property of Applicant',
           'reason' : 'Reason for Approach',
           'reason_classification' : 'Reason Classification',
           'prevention' : 'Prevention Activities Carried Out',
           'organisation_involved' : 'Organisation Involved',
           'activity_tier' : 'Prevention Activity Tier',
           'approach_outcome' : 'Approach Outcome',
           'percentage_of_breakdown' : 'Percentage of Breakdown',
           'value' : 'Value'}, axis=1)

df = df[['Period',
         'Area',
         'Reason for Approach',
         'Reason Classification',
         'Property of Applicant',
         'Prevention Activities Carried Out',
         'Prevention Activity Tier',
         'Organisation Involved',
         'Number of Approaches',
         'Approach Outcome',
         'Approach Status',
         'Percentage of Breakdown',
         'Value',
         'Measure Type',
         'Unit']]

df['Value'] = df.apply(lambda x: round(x['Value'], 1) if 'rate' in x['Unit'] else x['Value'], axis = 1)

df


# In[791]:


out = Path('codelists')
out.mkdir(exist_ok=True)

CODELISTS = False

if CODELISTS:
    for col in df.columns:
        if col not in ['Period', 'Area', 'Percentage of Breakdown', 'Measure Type', 'Unit', 'Value']:
            dfcode = df[[col]].drop_duplicates()
            dfcode['Notation'] = dfcode.apply(lambda x: pathify(x[col]), axis = 1)
            dfcode = dfcode.rename(columns={dfcode.columns[0]: 'Label'})
            dfcode['Parent Notation'] = ''
            dfcode['Sort Priority'] = np.arange(dfcode.shape[0])
            dfcode.drop_duplicates().to_csv(out / f'{pathify(col)}.csv', index = False)


# In[792]:


COLUMNS_TO_NOT_PATHIFY = ['Area', 'Percentage of Breakdown', 'Value']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err


# In[793]:


df = df.drop(columns = ['Percentage of Breakdown'])

scraper.dataset.comment = 'Some Figures have been rounded to the nearest 5 for disclosure control purposes.'                           'The PREVENT1 data specification contains the core questions to be used in the monitoring of housing options work by local authorities.'                           'Applicants may select multiple responses, which is why total reason figures are greater than the number of approaches'

# Add dataframe is in the cube
cubes.add_cube(scraper, df, scraper.title)


# In[794]:


# Write cube
cubes.output_all()


# In[795]:


from IPython.core.display import HTML
for col in df:
    if col not in ['Value']:
        df[col] = df[col].astype('category')
        display(HTML(f"<h2>{col}</h2>"))
        display(df[col].cat.categories)


# In[796]:


""""metadata_json = open("./out/housing-options-prevent1-statistics-in-scotland.csv-metadata.json", "r")
metadata = json.load(metadata_json)
metadata_json.close()

for obj in metadata["tables"][0]["tableSchema"]["columns"]:
    if obj["name"] == 'percentage_of_breakdown':
        obj.pop('valueUrl', None)

metadata_json = open("./out/housing-options-prevent1-statistics-in-scotland.csv-metadata.json", "w")
json.dump(metadata, metadata_json, indent=4)
metadata_json.close()"""

