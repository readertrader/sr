# Import variables
from utils import *
import pandas as pd
import numpy as np 

def read_data(fn, clean=True):
    if not clean:
        return pd.read_csv(fn)
    else:
        return clean_data(pd.read_csv(fn))

def clean_data(df):
    df = set_datetime(df)
    df['Dates'] = pd.to_datetime(df['Date']).dt.date
    df['Time'] = pd.to_datetime(df['Date']).dt.time
    grouping = df.groupby('Dates')
    return df, grouping

def sort_groupings(grouping, n, start='09:30', end='15:00'):
    dfl = []
    start = pd.to_datetime(start).time()
    end = pd.to_datetime(end).time()
    for _, itemdf in grouping:
        a = itemdf['Time']
        # Check if bars exist in this time period
        if len(a[(a > start) & (a < end)]) != 0:
            # ReIndex
            itemdf.index = list(range(0,len(itemdf)))
            # Compute nbar
            itemdf['nhigh'] = itemdf['High'].rolling(n).max()
            itemdf['nlow'] = itemdf['Low'].rolling(n).min()
            # Transform nulls
            itemdf['nhigh'][itemdf['nhigh'].isnull()] = 100000
            itemdf['nlow'][itemdf['nlow'].isnull()] = 1
            # Filter only RTH
            s = itemdf[itemdf['Time'] >= start].iloc[[0,]].index[0]
            e = itemdf[itemdf['Time'] <= end].iloc[[-1,]].index[0]
            if s > n+1:
                s = s - n - 1
            else:
                s = 0
            itemdf = itemdf.iloc[s:e]
            itemdf.index = list(range(0,len(itemdf)))
            itemdf = compare_nbar(itemdf)
            if len(itemdf[itemdf['compare'] != 0]) > 0:
                dfl.append(itemdf)
    return dfl

def compare_nbar(df):
    l = [0]
    val = 0
    for i in range(1,len(df)):
        if df.iloc[i]['Close'] > df.iloc[i-1]['nhigh']:
            val = 1
        elif df.iloc[i]['Close'] < df.iloc[i-1]['nlow']:
            val = -1
        else:
            val = 0
        l.append(val)
    df['compare'] = l
    return df

def stop_tp(row, factor=1):
    if row['compare'] == 1:
        s = row['Low'] - 0.25
        ran = abs(row['Close'] - row['Low'])
        p = row['Close'] + (ran*factor)
    if row['compare'] == -1:
        s = row['High'] + 0.25
        ran = abs(row['High'] - row['Close'])
        p = row['Close'] - (ran*factor)
    return s,p,ran

def run_backtest(dfl, factor):
    trades_per_day = []
    winners = 0 
    losers = 0 
    total_trades = 0
    profit = 0
    for day in dfl:
        in_trade = True
        idx = day[day['compare'] != 0].iloc[[0,]].index[0]
        pos_type = day.iloc[idx]['compare']
        sl, tp, ticks = stop_tp(day.iloc[idx], factor)
        trades = 1
        dp = 0
        for i in range(idx, len(day) - 1):
            if trades == 100:
                break
            if in_trade:
                if pos_type == 1:
                    if day.iloc[i]['High'] >= tp:
                        winners += 1
                        profit = profit + (ticks * factor)
                        dp = dp + (ticks * factor)
                        in_trade = False
                    elif day.iloc[i]['Low'] <= sl:
                        losers += 1
                        profit = profit - ticks
                        dp = dp - ticks
                        in_trade = False
                else:
                    if day.iloc[i]['Low'] <= tp:
                        winners += 1
                        profit = profit + (ticks * factor)
                        dp = dp + (ticks * factor)
                        in_trade = False
                    elif day.iloc[i]['High'] >= sl:
                        losers += 1
                        profit = profit - ticks
                        dp = profit - ticks
                        in_trade = False
            else:
                if day.iloc[i]['compare'] != 0:
                    pos_type = day.iloc[i]['compare']
                    sl, tp, ticks = stop_tp(day.iloc[i], factor)
                    trades +=1
                    in_trade = True
        if in_trade:
            trades = trades - 1
            in_trade = False
        trades_per_day.append(trades)
        total_trades = total_trades + trades
    return [profit, winners, losers]


# Initialize variables
fn = 'stocks/data/nq.txt'
n = 21
# Initialize Metrics to Compute
factor=4
trades_per_day = []
winners = 0 
losers = 0 
total_trades = 0
capital = 5000
profit = 0

# Get days
df, grp = read_data(fn)
dfl = sort_groupings(grp, n)


ps = {}
li = [0.5,1,1.5,2]
for factor in li:
    ps[factor] = run_backtest(dfl, factor)