import pandas as pd
import numpy as np
from math import sqrt
from cvxopt import matrix
from cvxopt.solvers import qp, options
from cvxopt.blas import dot
import matplotlib.pyplot as plt
import os
from pathlib import Path
pd.options.mode.chained_assignment = None

def run_cvxoptOnSP500():


    sp500Path="s_p500.xlsx"
    sp500 = pd.read_excel(sp500Path)
    sp500=sp500[["Names Date","Ticker Symbol","Trading Symbol","Return on the S&P 500 Index","Returns"]]
    sp500.dropna(inplace=True)
    sp500 = sp500[sp500['Ticker Symbol'] == sp500['Trading Symbol']]
    sp500.drop(columns=['Trading Symbol'],inplace=True)
    sp500.loc[sp500['Ticker Symbol'] == "SUNW", 'Ticker Symbol'] = "JAVA"
    indexList=[]
    for ticker in set(sp500["Ticker Symbol"]):
        if len(sp500[sp500["Ticker Symbol"]==ticker])!=65:
            indexList=indexList+sp500[sp500["Ticker Symbol"]==ticker].index.values.tolist()
    sp500.drop(indexList,inplace=True)
    sp500["Names Date"]=[str(int(i)) for i in sp500["Names Date"].values]


    # sp500_withNormalReturn=sp500.drop(columns=['Return on the S&P 500 Index'])
    # NormalReturn=np.empty([len(set(sp500_withNormalReturn["Names Date"])), len(set(sp500_withNormalReturn["Ticker Symbol"]))])
    # dates=list(set(sp500_withNormalReturn["Names Date"]))
    # dates.sort()
    # tickers=list(set(sp500_withNormalReturn["Ticker Symbol"]))
    # tickers.sort()
    # for i in range(len(tickers)):
    #     NormalReturn[:,i]=sp500_withNormalReturn[sp500_withNormalReturn["Ticker Symbol"]==tickers[i]]["Returns"].values
    # NormalReturn=pd.DataFrame(NormalReturn)
    # NormalReturn.index=dates
    # NormalReturn.columns=tickers
    # cov_Normal=NormalReturn.cov()
    # return_Normal=((NormalReturn+1).cumprod().iloc[-1,:]-1).values
    #
    # matrix_cov_Normal=matrix(cov_Normal.values)
    # vector_return_Normal=matrix(return_Normal)




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
    cov_Excess=ExcessReturn.cov()
    return_Excess=((ExcessReturn+1).cumprod().iloc[-1,:]-1).values

    matrix_cov_Excess=matrix(cov_Excess.values)
    vector_return_Excess=matrix(return_Excess)


    n = 500
    G = matrix(0.0, (n,n))
    G[::n+1] = -1.0
    h = matrix(0.0, (n,1))
    A = matrix(1.0, (1,n))
    b = matrix(1.0)
    N = 100
    mus = [ 10**(7.0*t/N-1.0) for t in range(N) ]
    options['show_progress'] = False


    weights_Excess = [ qp(mu*matrix_cov_Excess, -vector_return_Excess, G, h, A, b)['x'] for mu in mus ]
    result_Excessreturns = [ dot(vector_return_Excess,x) for x in weights_Excess ]
    result_Excessrisks = [ sqrt(dot(x, matrix_cov_Excess*x)) for x in weights_Excess ]



    # weights_Normal = [ qp(mu*matrix_cov_Normal, -vector_return_Normal, G, h, A, b)['x'] for mu in mus ]
    # result_Normalreturns = [ dot(vector_return_Normal,x) for x in weights_Normal ]
    # result_Normalrisks = [ sqrt(dot(x, matrix_cov_Normal*x)) for x in weights_Normal ]



    Excess_turnover=[0.]*N
    for k in range(N):
        tempturnover=0.
        for i,j in zip(weights_Excess[k],weights_Excess[-1]):
            if j>i:
                tempturnover=tempturnover+(j-i)
        Excess_turnover[k]=tempturnover
    plt.plot(mus,Excess_turnover)
    plt.xlabel("penalizing parameter started with")
    plt.ylabel("turnover rate")
    plt.title("trends of turnover rate")
    plt.savefig("turnover rate trends.png")
    plt.show()
