import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
import os
from pathlib import Path

"""
This file is used to generate matrix of normal return and excess return to do convex optimization
the index of matrix(DataFrame) is date, the column is tickers of stocks
"""

"""
Please adjust the path of s_p500.xlsx here
"""
def sp500Return():
    sp500Path="s_p500.xlsx"

    #read file, delete useless columns
    sp500 = pd.read_excel(sp500Path)
    sp500=sp500[["Names Date","Ticker Symbol","Trading Symbol","Return on the S&P 500 Index","Returns"]]
    #drop nan
    sp500.dropna(inplace=True)
    #delete incomplete data
    sp500 = sp500[sp500['Ticker Symbol'] == sp500['Trading Symbol']]
    sp500.drop(columns=['Trading Symbol'],inplace=True)
    sp500.loc[sp500['Ticker Symbol'] == "SUNW", 'Ticker Symbol'] = "JAVA"

    indexList=[]
    for ticker in set(sp500["Ticker Symbol"]):
        if len(sp500[sp500["Ticker Symbol"]==ticker])!=65:
            indexList=indexList+sp500[sp500["Ticker Symbol"]==ticker].index.values.tolist()

    sp500.drop(indexList,inplace=True)
    sp500["Names Date"]=[str(int(i)) for i in sp500["Names Date"].values]


    #process and format excess return
    sp500_withNormalReturn=sp500.drop(columns=['Return on the S&P 500 Index'])

    sp500_withExcessReturn=sp500
    sp500_withExcessReturn["Excess Returns"]=sp500_withExcessReturn["Returns"]-sp500_withExcessReturn["Return on the S&P 500 Index"]
    sp500_withExcessReturn.drop(columns=['Return on the S&P 500 Index','Returns'],inplace=True)



    ExcessReturn=np.empty([len(set(sp500_withExcessReturn["Names Date"])), len(set(sp500_withExcessReturn["Ticker Symbol"]))])
    dates=list(set(sp500_withExcessReturn["Names Date"]))
    dates.sort()
    tickers=list(set(sp500_withExcessReturn["Ticker Symbol"]))
    tickers.sort()
    for i in range(len(tickers)):
        ExcessReturn[:,i]=sp500_withExcessReturn[sp500_withExcessReturn["Ticker Symbol"]==tickers[i]]["Excess Returns"].values
    ExcessReturn=pd.DataFrame(ExcessReturn)
    ExcessReturn.index=dates
    ExcessReturn.columns=tickers

    #process and format normal return
    NormalReturn=np.empty([len(set(sp500_withNormalReturn["Names Date"])), len(set(sp500_withNormalReturn["Ticker Symbol"]))])
    dates=list(set(sp500_withNormalReturn["Names Date"]))
    dates.sort()
    tickers=list(set(sp500_withNormalReturn["Ticker Symbol"]))
    tickers.sort()
    for i in range(len(tickers)):
        NormalReturn[:,i]=sp500_withNormalReturn[sp500_withNormalReturn["Ticker Symbol"]==tickers[i]]["Returns"].values
    NormalReturn=pd.DataFrame(NormalReturn)
    NormalReturn.index=dates
    NormalReturn.columns=tickers

    NormalReturn.to_csv("NormalReturn.csv")
    ExcessReturn.to_csv("ExcessReturn.csv")


