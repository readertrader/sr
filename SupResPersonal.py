import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import mplfinance

class SupResPersonal:

    def __init__(self, dataframe) -> None:
        self.df = dataframe
        self.date = self.df['Date']
        self.set_datetime()
        self.levels = []
        self.ml_levels = []
        self.train_df = None
        self.filtered_range = []
        self.filtered_distance = []
        self.ml_data = None
        self.search_key = None
        self.end_key = None
    
    def set_train_df(self, key):
        self.train_df = key
    
    def set_search_key(self, key):
        self.search_key = key
    
    def set_end_key(self, key):
        self.end_key = key
    
    def get_train_data(self):
        assert self.search_key is not None, "Need to set a search key first"
        start = self.df[self.df['Date'].str.contains(self.search_key)].iloc[[0,]].index[0]
        end = len(self.df)
        if self.end_key is not None:
            end = self.df[self.df['Date'].str.contains(self.end_key)].iloc[[0, ]].index[0]
        self.end_key = None
        self.search_key = None
        return self.df.iloc[start:end]
    
    def get_levels(self, ml=False):
        if self.train_df is None:
            self.train_df = self.get_train_data()
            self.train_df.index = list(range(0,len(self.train_df)))
            #self.ml_data = np.array(list(self.train_df['Close']) + list(self.train_df['High']) + list(self.train_df['Low']) + list(self.train_df['Open']))
        self.ml_data = np.array(list(self.train_df['Close']))
        self.compute_sr(ml)

    def convert_to_datetime(self):
        new_date = []
        for item in self.date:
            split_date = item.split(' ')
            hour = split_date[1].split(':')[0]
            if int(hour) == 12:
                hour = '0'
            if 'PM' in item:
                hour = str(int(hour) + 12)
            split_date[1] = hour + ':' + ':'.join(split_date[1].split(':')[1:])
            item =' '.join(split_date[:2])
            new_date.append(item)
        return new_date
    
    def set_datetime(self):
        self.df['Date'] = self.convert_to_datetime()
        #self.df.set_index('Date', inplace=True)

    def isSupport(self,my_df,i):
        support = my_df['Low'][i] < my_df['Low'][i-1]  and my_df['Low'][i] < my_df['Low'][i+1] \
        and my_df['Low'][i+1] < my_df['Low'][i+2] and my_df['Low'][i-1] < my_df['Low'][i-2]

        return support

    def isResistance(self,my_df,i):
        resistance = my_df['High'][i] > my_df['High'][i-1]  and my_df['High'][i] > my_df['High'][i+1] \
        and my_df['High'][i+1] > my_df['High'][i+2] and my_df['High'][i-1] > my_df['High'][i-2] 

        return resistance

    def filter_levels(self, ll):
        final = []
        ll.sort()
        ll = list(set(ll))
        temp = []
        for i in range(len(ll)-1):
            if ll[i+1] <= ll[i] + 1:
                temp = [ll[i+1], ll[i]]
                final.append(temp)
            if ll[i] in temp:
                continue
            else:
                temp = [ll[i]]
                final.append(temp)
        final.append([ll[-1]])
        final = self.flatten(final)
        self.filtered_range = final
        return self.filtered_range

    def return_levels(self, ml=False):
        if ml:
            return self.ml_levels
        elif type(ml) == str:
            return (self.levels, self.ml_levels)
        else:
            return self.levels
    
    def append_both(self, i, type):
        if type == 'support':
            self.levels.append(self.train_df['Low'][i])
            self.levels.append(self.train_df['Close'][i])
        if type == 'resistance':
            self.levels.append(self.train_df['High'][i])
            self.levels.append(self.train_df['Close'][i])
    
    def compute_sr(self, ml=False):
        if not ml:
            self.levels = []
            for i in range(2,self.train_df.shape[0]-2):
                if self.isSupport(self.train_df, i):
                    self.levels.append(self.train_df['Low'][i])
                    self.levels.append(self.train_df['Close'][i])
                elif self.isResistance(self.train_df,i):
                    self.levels.append(self.train_df['High'][i])
                    self.levels.append(self.train_df['Close'][i])
            self.levels.sort()
        else:
            ml = int(ml)
            self.ml_levels = []
            kmeans = KMeans(n_clusters=ml).fit(self.ml_data.reshape(-1,1))
            c = kmeans.predict(self.ml_data.reshape(-1,1))
            for i in range(int(ml)):
                self.ml_levels.append([-np.inf,np.inf])
            for i in range(len(self.ml_data)):
                cluster = c[i]
                if self.ml_data[i] > self.ml_levels[cluster][0]:
                    self.ml_levels[cluster][0] = self.ml_data[i]
                if self.ml_data[i] < self.ml_levels[cluster][1]:
                    self.ml_levels[cluster][1] = self.ml_data[i]
            self.ml_levels = self.flatten(self.ml_levels)

    
    def filter_distance(self, levels_to_filter):
        self.filtered_distance = []
        s =  np.mean(self.train_df['High'] - self.train_df['Low'])
        def isFarFromLevel(l,s):
            return np.sum([abs(l-x) < s for x in self.filtered_distance]) == 0
        for l in levels_to_filter:
            if isFarFromLevel(l,s):
                self.filtered_distance.append(l)
        return self.filtered_distance
    
    def return_filtered_levels(self):
        return (self.filtered_distance, self.filtered_range)
    
    def flatten(self, t):
        return [item for sublist in t for item in sublist]

    def save_data(self):
        self.train_df.to_csv('training.csv')
        
    def save_levels(self, lev, write='w', market='es'):
        assert write == 'a' or write =='w', "Need w for write to new file or a for append"
        if market == 'es':
            fn = 'sr.txt'
        else:
            fn = 'sr_nq.txt'
        with open('C://Users/Avi/Documents/Ninjatrader 8/' + fn, write) as f:
            for obj in lev:
                f.write(str(obj) + '\n')

    def plot_all(self, d, hlines):  
        d['Date'] = pd.to_datetime(d['Date'])
        d.set_index(d['Date'], inplace=True)
        d.drop('Date', axis=1, inplace=True)
        mplfinance.plot(d,hlines=dict(hlines=hlines,linestyle='-.'),type='candle')