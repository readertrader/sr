import pandas as pd
import numpy as np
import mplfinance

def set_datetime(df):
    df['Date'] = convert_to_datetime(df['Date'])
    return df

def convert_to_datetime(date):
    new_date = []
    for item in date:
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

def get_train_data(df, sk, ek=None, skew=30):
    start = df[df['Date'].str.contains(sk)].iloc[[0,]].index[0] 
    if start >= skew:
        start = start - skew
    else:
        start = 0
    end = len(df)
    if ek is not None:
        end = df[df['Date'].str.contains(ek)].iloc[[0, ]].index[0]
    return df.iloc[start:end]

def flatten(t):
    return [item for sublist in t for item in sublist]

def save_data(df, fn):
    df.to_csv(fn)

def plot_all(d, hlines):
    d['Date'] = pd.to_datetime(d['Date'])
    d.set_index(d['Date'], inplace=True)
    d.drop('Date', axis=1, inplace=True)
    mplfinance.plot(d,hlines=dict(hlines=hlines,linestyle='-.'),type='candle')
