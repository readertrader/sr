import shutil

def prepend(text, fn):
    with open(fn, 'r+') as file:
        content = file.read()
        file.seek(0)
        file.write(text + content)

    
text_to_write = 'Date,Open,High,Low,Close\n'

typ = input("Type file ext: ")
source_file = 'C:/Users/Avi/Documents/NinjaTrader 8/MyTestFile.txt'
dump_site = "C:/Users/Avi/Documents/stock_bots/stocks/data/" + typ + '.txt'
shutil.move(source_file, dump_site)
prepend(text_to_write, dump_site)




