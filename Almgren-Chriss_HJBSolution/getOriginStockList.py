import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None

"""
IMPORTANT!!! Before running this code, please revise the following path of "All-CRSP-2007.xlsx", and the file is huge, please be patient!
"""
path=r"C:\Users\liyf4\Desktop\F盘\NYU\2020 Spring Semester\Algo Trading & Quant Strats\Homework\Homework2\All-CRSP-2007.xlsx"

stocks = pd.read_excel(path)
#delete unimportant infomation
stocks_new=stocks[["Names Date","Trading Symbol","Ticker Symbol","Cumulative Factor to Adjust Prices","Cumulative Factor to Adjust Shares/Vol"]]
stocks_new.dropna(inplace=True)
#delete stocks with invalid Ticker Symbol
stocks_new = stocks_new[stocks_new['Ticker Symbol'] == stocks_new['Trading Symbol']]
stocks_new.drop(columns=['Trading Symbol'],inplace=True)
# if stock miss data durin the year we delete it from our stock list
indexList=[]
for ticker in set(stocks_new["Ticker Symbol"]):
    if len(stocks_new[stocks_new["Ticker Symbol"]==ticker])!=251:
        indexList=indexList+stocks_new[stocks_new["Ticker Symbol"]==ticker].index.values.tolist()
stocks_new.drop(indexList,inplace=True)
listOfStock=list(set(stocks_new["Ticker Symbol"].values))
# write the stock list to txt file
file= open("ListOfMoreStock.txt","w")
for i in listOfStock:
    file.write(i+'\n')
file.close()