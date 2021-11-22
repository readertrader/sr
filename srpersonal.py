import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from SupRes import SupRes
import matplotlib.pyplot as plt


# Read Data
#file_ext = '11_09_2021.txt'
file_ext = '11.19.2021/es2k.txt'
df = pd.read_csv('stocks/data/' + file_ext)

#Initialize Model
sr = SupRes(df)
skey = '11/18/2021 18:'
ekey = '11/19/2021 9:30'
sr.set_search_key(skey)
sr.set_end_key(ekey)
sr.get_levels(ml=7)
sr.get_levels()
#print(sr.ml_levels)
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

