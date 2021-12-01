import shutil
import os
from datetime import date

def prepend(text, fn):
    with open(fn, 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write(text + content)

def make_directory(ds):
    today = date.today()
    d1 = today.strftime("%m.%d.%Y")
    path = ds + d1
    if not os.path.exists(path):
        os.makedirs(path)
    return path + '/'

def move_and_prepend(source, end, fn):
    end = make_directory(end)
    text_to_write = 'Date,Open,High,Low,Close\n'
    end_fn = end + fn
    shutil.move(source, end_fn)
    prepend(text_to_write, end_fn)

source_dir = 'C:/Users/Avi/Documents/NinjaTrader 8/'
dump_site = "C:/Users/Avi/Documents/stock_bots/data/"
for file in os.listdir(source_dir):
    if '.txt' in file:
        move_and_prepend(source_dir+file, dump_site, file)








"""
typ = input("Type file ext: ")
source_file = 'C:/Users/Avi/Documents/NinjaTrader 8/MyTestFile.txt'
dump_site = "C:/Users/Avi/Documents/stock_bots/stocks/data/"
make_directory(dump_site)
dump_site = dump_site + typ + '.txt'
shutil.move(source_file, dump_site)
prepend(text_to_write, dump_site)
"""
