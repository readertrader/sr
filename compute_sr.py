
import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from SupResPersonal import SupResPersonal as spr
import matplotlib.pyplot as plt

def split_data(df):
    idxs = []
    dfs = {}
    for i in reversed(range(len(df))):
        if ' 9:15' in df.iloc[i]['Date']:
            idxs.append(i)
    for i in idxs:
        d = df.iloc[:i]
        changes = 5
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

# Read Data
file_ext = 'data/11.30.2021/nq15.txt'
write_file = 'C://Users/Avi/Documents/Ninjatrader 8/nq.txt'
df = pd.read_csv(file_ext)

#Initialize Model
sr = spr(df)
df = sr.df
dfs = split_data(df)

outputs = {}
for key, val in dfs.items():
    sr.set_train_df(val)
    sr.get_levels(ml=7)
    sr.get_levels()
    sr.filter_distance( sr.levels + sr.ml_levels )
    outputs[key] = sr.filtered_distance

with open(write_file, 'w') as f:
    for key, val in outputs.items():
        f.write(str(key) + '\n')
        for item in val:
            f.write(str(item) + '\n')


"""
dfs.keys()
sr.set_train_df(dfs['11/21/2021'])
sr.get_levels(ml=7)
sr.get_levels()
print(sr.filter_distance( sr.levels + sr.ml_levels ))
sr.save_levels(sr.filtered_distance, 'w')
"""

