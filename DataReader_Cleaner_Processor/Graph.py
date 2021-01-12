import matplotlib.pyplot as plt
from Reader.FileManager import FileManager
from Reader.FileNames import FileNames as FM
from Processor.readSP500 import readSP500
from Processor.TAQAdjust import TAQAdjust
from StatsAnalysis.FileStuctureConvertor import QuotesConvertor
from StatsAnalysis.FileStuctureConvertor import TradesConvertor
from Processor.TAQCleaner import TAQCleaner
import numpy as np
import os
from pathlib import Path
def convert_date():
    """convert all quotes date to date type object, for plotting use"""
    date1 = ['2007-06-20', '2007-06-21', '2007-06-22', '2007-06-25', '2007-06-26', '2007-06-27', '2007-06-28',
             '2007-06-29',
             '2007-07-02', '2007-07-03', '2007-07-05', '2007-07-06', '2007-07-09', '2007-07-10', '2007-07-11',
             '2007-07-12',
             '2007-07-13', '2007-07-16', '2007-07-17', '2007-07-18', '2007-07-19', '2007-07-20', '2007-07-23',
             '2007-07-24',
             '2007-07-25', '2007-07-26', '2007-07-27', '2007-07-30', '2007-07-31', '2007-08-01', '2007-08-02',
             '2007-08-03',
             '2007-08-06', '2007-08-07', '2007-08-08', '2007-08-09', '2007-08-10', '2007-08-13', '2007-08-14',
             '2007-08-15',
             '2007-08-16', '2007-08-17', '2007-08-20', '2007-08-21', '2007-08-22', '2007-08-23', '2007-08-24',
             '2007-08-27',
             '2007-08-28', '2007-08-29', '2007-08-30', '2007-08-31', '2007-09-04', '2007-09-05', '2007-09-06',
             '2007-09-07',
             '2007-09-10', '2007-09-11', '2007-09-12', '2007-09-13', '2007-09-14', '2007-09-17', '2007-09-18',
             '2007-09-19', '2007-09-20']
    from datetime import datetime
    date_list = []
    for date in date1:
        date_list.append(datetime.strptime(date, '%Y-%m-%d'))
    return date_list


def quote_closeprice(ticker, adjusted):
    """Take ticker, return daily closed price of all trading periods, True with adjusted close"""
    fm = FileManager(FM.TAQR)
    dateList = fm.getQuoteDates("20070620", "20070921")
    sp500 = readSP500("s_p500.xlsx")
    print("Dates range from:", dateList[0], "to", dateList[-1])
    quote = TAQAdjust(ticker, dateList, sp500).getQuoteData(ticker)
    if adjusted == False:
        quote = QuotesConvertor(quote)
        price = [quote[i][3] for i in range(len(quote) - 1) if
                 quote[i][0] != quote[i + 1][0]]
        price.append(quote[-1][3])

    if adjusted == True:
        quote = QuotesConvertor(TAQAdjust(ticker, dateList, sp500).adjust_quotes(quote, ticker))
        price = [quote[i][3] for i in range(len(quote) - 1) if
                 quote[i][0] != quote[i + 1][0]]
        price.append(quote[-1][3])

    return price

def trade_closeprice(ticker, adjusted):
    """Take ticker, return daily trades closed price of all trading periods, True with adjusted close"""
    fm = FileManager(FM.TAQR)
    dateList = fm.getQuoteDates("20070620", "20070921")
    sp500 = readSP500("s_p500.xlsx")
    print("Dates range from:", dateList[0], "to", dateList[-1])
    trade = TAQAdjust(ticker, dateList, sp500).getTradeData(ticker)
    if adjusted == False:
        trade = TradesConvertor(trade)
        price = [trade[i][2] for i in range(len(trade) - 1) if
                 trade[i][0] != trade[i + 1][0]]
        price.append(trade[-1][2])

    if adjusted == True:
        trade = TradesConvertor(TAQAdjust(ticker, dateList, sp500).adjust_trades(trade, ticker))
        price = [trade[i][2] for i in range(len(trade) - 1) if
                 trade[i][0] != trade[i + 1][0]]
        price.append(trade[-1][2])

    return price


def graph_quotes(ticker):
    plt.figure(figsize=(20, 10))
    plt.plot(convert_date(), quote_closeprice(ticker, False), label='before adjust')
    plt.plot(convert_date(), quote_closeprice(ticker, True), label='after adjust')
    plt.xlabel('date')
    plt.ylabel('BidPrices')
    plt.title(str(ticker + ' Adjustment'))
    plt.legend()
    plt.grid()
    plt.show()

def graph_trades(ticker):
    plt.figure(figsize=(20, 10))
    plt.plot(convert_date(), trade_closeprice(ticker, False), label='before adjust')
    plt.plot(convert_date(), trade_closeprice(ticker, True), label='after adjust')
    plt.xlabel('date')
    plt.ylabel('Trades Prices')
    plt.title(str(ticker + ' Adjustment'))
    plt.legend()
    plt.grid()
    plt.show()

def graph_cleaning(quote_path,trade_path,ticker,date,type):
    """take adjusted quote and trade and specific date, return cleaning result plot"""
    trades = np.load(trade_path, allow_pickle=True).item()
    quotes = np.load(quote_path, allow_pickle=True).item()
    cleaner1 = TAQCleaner(quotes=quotes, trades=trades, ticker=ticker)
    if type=='trades':
        clean_before = trades[date]['Price']
    #cleaner1.clean_quotes()
        cleaner1.clean_trades()
        outlier = np.where(cleaner1.get_tradeOutlierSymbol()[date] == True)[0]
        out_index = [n for n in outlier]
        out_price = [clean_before[i] for i in out_index]
    if type=='quotes':
        clean_before = quotes[date]['BidPrice']
        cleaner1.clean_quotes()
        outlier = np.where(cleaner1.get_quoteOutlierSymbol()[date] == True)[0]
        out_index = [n for n in outlier]
        out_price = [clean_before[i] for i in out_index]
    x = range(0, len(clean_before))
    plt.figure(figsize=(20, 10))
    plt.plot(x, clean_before, label='Normal')
    plt.plot(out_index, out_price, 'ro', label='Outlier')
    plt.xlabel('time')
    plt.ylabel('adjusted price')
    plt.title(str(ticker+' Cleaning at '+date))
    plt.legend()
    plt.grid()
    plt.show()




