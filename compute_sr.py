
import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from SupResPersonal import SupResPersonal as spr
import matplotlib.pyplot as plt

def split_data_tick(df, days=3):
    idxs = []
    dfs = {}
    found_9 = False
    for i in reversed(range(len(df))):
        if ' 9:' in df.iloc[i]['Date'] and not found_9:
            idxs.append(i)
            found_9 = True
        if '8:' in df.iloc[i]['Date'] and found_9:
            found_9 = False
    for i in idxs:
        d = df.iloc[:i]
        changes = days
        set_state = False
        dat_i = d.iloc[-1]['Date'].split(' ')[0]
        for j in reversed(range(len(d))):
            if changes > 0 and j == 0:
                set_state = True
                break
            if d.iloc[j]['Date'].split(' ')[0] != dat_i and ' 18:' in d.iloc[j]['Date']:
                changes = changes - 1
                dat_i = d.iloc[j]['Date'].split(' ')[0]
            if changes == 0:
                to_append = d.iloc[j-2:]
                to_append.index = list(range(0,len(to_append)))
                dfs[d.iloc[-1]['Date'].split(' ')[0]] = to_append
                break
        if set_state:
            break
    return dfs  


def split_data(df, days=5):
    idxs = []
    dfs = {}
    for i in reversed(range(len(df))):
        if ' 9:15' in df.iloc[i]['Date']:
            idxs.append(i)
    for i in idxs:
        d = df.iloc[:i]
        changes = days
        set_state = False
        dat_i = d.iloc[-1]['Date'].split(' ')[0]
        for j in reversed(range(len(d))):
            if changes > 0 and j == 0:
                set_state = True
                break
            if d.iloc[j]['Date'].split(' ')[0] != dat_i and ' 18:' in d.iloc[j]['Date']:
                changes = changes - 1
                dat_i = d.iloc[j]['Date'].split(' ')[0]
            if changes == 0:
                to_append = d.iloc[j-2:]
                to_append.index = list(range(0,len(to_append)))
                dfs[d.iloc[-1]['Date'].split(' ')[0]] = to_append
                break
        if set_state:
            break
    return dfs  

def write_output(outputs, fn):
    with open(fn, 'w') as f:
        for key, val in outputs.items():
            f.write(str(key) + '\n')
            for item in val:
                f.write(str(item) + '\n')

def live_split(df, days=5):
    current_date = df.iloc[-1]['Date'].split(' ')[0]
    search_eod = False
    for i in reversed(range(len(df))):
        if df.iloc[i]['Date'].split(' ')[0] != current_date and not search_eod:
            days = days - 1
            current_date = df.iloc[i]['Date'].split(' ')[0]
        if days == 0:
            search_eod = True
        if search_eod:
            if ' 18:' in df.iloc[i]['Date']:
                idx = i
                break
    return df.iloc[i:]

def time_historical(df, ml=7, length=5):
    sr = spr(df)
    df = sr.df
    dfs = split_data(df,length)
    outputs = {}
    for key, val in dfs.items():
        if len(val) < 2:
            continue
        sr.set_train_df(val)
        sr.get_levels()
        if ml is not None:
            sr.get_levels(ml)
            sr.filter_distance(sr.levels + sr.ml_levels)
        else:
            sr.filter_distance(sr.levels)
        outputs[key] = sr.filtered_distance
    return outputs


def time_live(df, ml=7, length=5):
    sr = spr(df)
    df = sr.df
    new_df = live_split(df)
    outputs = {}
    sr.set_train_df(new_df)
    sr.get_levels()
    if ml is not None:
        sr.get_levels(ml)
        sr.filter_distance(sr.levels + sr.ml_levels)
    else:
        sr.filter_distance(sr.levels)
    date = new_df.iloc[-1]['Date'].split(' ')[0]
    outputs[date] = sr.filtered_distance
    return outputs

# Read Data
file_ext = 'data/12.17.2021/es15.txt'
write_file = 'C://Users/Avi/Documents/Ninjatrader 8/sr/es15.txt'
df = pd.read_csv(file_ext)

outputs = time_historical(df, None)
write_output(outputs, write_file)



"""
#Initialize Model
sr = spr(df)
df = sr.df
dfs = split_data(df,5)

outputs = {}
for key, val in dfs.items():
    if len(val) < 2:
        continue
    sr.set_train_df(val)
    sr.get_levels(ml=7)
    sr.get_levels()
    sr.filter_distance( sr.levels )
    outputs[key] = sr.filtered_distance
"""

"""
with open(write_file, 'w') as f:
    for key, val in outputs.items():
        f.write(str(key) + '\n')
        for item in val:
            f.write(str(item) + '\n')
dfs.keys()
sr.set_train_df(dfs['11/21/2021'])
sr.get_levels(ml=7)
sr.get_levels()
print(sr.filter_distance( sr.levels + sr.ml_levels ))
sr.save_levels(sr.filtered_distance, 'w')
"""

