import pandas as pd
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from SupRes import SupRes
import matplotlib.pyplot as plt


# Read Data
file_ext = '10_25_2021.txt'
df = pd.read_csv('stocks/data/' + file_ext)

#Initialize Model
sr = SupRes(df)
skey = '10/25/2021 18:'
ekey = '10/26/2021 10:3'
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


