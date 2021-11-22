import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from SupResPersonal import SupRes
import matplotlib.pyplot as plt

def split_data(df):
    idxs = []
    dfs = {}
    for i in reversed(range(len(df))):
        if ' 9:30' in df.iloc[i]['Date']:
            idxs.append(i)

    for i in reversed(idxs):
        d = df.iloc[:i]
        changes = 5
        set_state = False
        dat_i = d.iloc[-1]['Date'].split(' ')[0]
        for j in reversed(range(len(d))):
            if changes > 0 and j == 0:
                set_state = True
                break
            if d.iloc[j]['Date'].split(' ')[0] != dat_i:
                changes = changes - 1
                dat_i = d.iloc[j]['Date'].split(' ')[0]
            if changes == 0:
                dfs[d.iloc[-1]['Date'].split(' ')[0]] = d.iloc[j:]
                break
        if set_state:
            break
    return dfs  

# Read Data
file_ext = 'data/es15.txt'
df = pd.read_csv(file_ext)

#Initialize Model
sr = SupRes(df)
df = sr.df
dfs = split_data(df)

"""
skey = '11/18/2021 18:'
ekey = '11/19/2021 9:30'
sr.set_search_key(skey)
sr.set_end_key(ekey)
sr.get_levels(ml=7)
sr.get_levels()
print(sr.filter_distance(sr.levels + sr.ml_levels))
#print(sr.filter_levels(sr.levels))
#print(sr.filtered_distance)
#sr.set_search_key(ekey)
#sr.set_end_key('10/26/2021 10:1')
#d = sr.get_train_data()
#sr.plot_all(d, sr.filtered_distance)
sr.save_levels(sr.filtered_distance, 'w')
#sr.save_data()
#sr.save_levels(sr.ml_levels + sr.levels, 'w', 'nq')

"""