import numpy as np
import datetime

"""
This script performs following tasks:
    1. display timestamp as seconds
    2. store endTS, startTS. Given X, divide data into bins 
    3. compute latest price for data points in each bin
"""


class getIntervalPrice(object):
    def __init__(self, quotes, trades, X,allowNaN=True):
        """

        :param quotes: dict
        :param trades: dict
        :param X: time interval
        :param allowNaN: boolean
        """
        self._quotes = quotes
        self._trades = trades
        self._X = X
        if allowNaN:
            self._filledValue=np.nan
        else:
            self._filledValue=np.nan #The replacing value has not been decided

        self._tradeTimeArray=[]
        self._quoteTimeArray=[]


    def get_time_interval(self, X, startTS=34199000, endTS=57599000):
        """
        Given X-minute interval, the method divides data into bins
        :param X:
        :param startTS:
        :param endTS:
        :return:
        """
        X_millis = X*60*1000
        num_bins = int((endTS-startTS)/X_millis)
        ts_intervals = [(startTS + i*X_millis) for i in range(num_bins+1)]
        if ts_intervals[-1]!=endTS:
            ts_intervals.append(endTS)
        return ts_intervals

    def get_trade_price(self):
        price=np.array([])
        ts_intervals = self.get_time_interval(self._X)
        for key in self._trades:
            dailyData=self._trades[key]
            tempPrice=np.array([0.]*(len(ts_intervals)-1))
            i=0
            for l,r in zip(ts_intervals[:-1],ts_intervals[1:]):
                temp=dailyData["Price"][np.logical_and(dailyData["MillisFromMidn"]>l,dailyData["MillisFromMidn"]<=r)]
                if len(temp)>0:
                    tempPrice[i]=temp[-1]
                else:
                    tempPrice[i]=self._filledValue
                i=i+1
            price=np.concatenate([price,tempPrice],axis=None)
            tempTimeList=[datetime.datetime.fromtimestamp(i/1000+datetime.datetime.strptime(key, "%Y%m%d").timestamp()) for i in ts_intervals[1:]]
            self._tradeTimeArray=self._tradeTimeArray+tempTimeList
        return  price

    def get_quote_price(self):
        askPrice=np.array([])
        bidPrice=np.array([])
        ts_intervals=self.get_time_interval(self._X)
        for key in self._quotes:
            dailyData=self._quotes[key]
            tempAskPrice=np.array([0.]*(len(ts_intervals)-1))
            tempBidPrice = np.array([0.] * (len(ts_intervals) - 1))
            i=0
            for l,r in zip(ts_intervals[:-1],ts_intervals[1:]):
                tempAsk=dailyData["AskPrice"][np.logical_and(dailyData["MillisFromMidn"]>l,dailyData["MillisFromMidn"]<=r)]
                if len(tempAsk)>0:
                    tempAskPrice[i]=tempAsk[-1]
                else:
                    tempAskPrice[i]=self._filledValue
                tempBid=dailyData["BidPrice"][np.logical_and(dailyData["MillisFromMidn"]>l,dailyData["MillisFromMidn"]<=r)]
                if len(tempBid)>0:
                    tempBidPrice[i]=tempBid[-1]
                else:
                    tempBidPrice[i]=self._filledValue
                i=i+1
            askPrice=np.concatenate([askPrice,tempAskPrice],axis=None)
            bidPrice=np.concatenate([bidPrice,tempBidPrice],axis=None)
            tempTimeList = [datetime.datetime.fromtimestamp(i/1000 + datetime.datetime.strptime(key, "%Y%m%d").timestamp())
                            for i in ts_intervals[1:]]
            self._quoteTimeArray=self._quoteTimeArray+tempTimeList
        return askPrice,bidPrice

    def returnTradeTime(self):
        return self._tradeTimeArray

    def returnQuoteTime(self):
        return self._quoteTimeArray

# if __name__=="__main__":
#     Path1=r"D:\Algo Trading & Quant Strats\Homework\Homework1_Lee\TAQClean\trades\IBM_trades.npy"
#     Path2=r"D:\Algo Trading & Quant Strats\Homework\Homework1_Lee\TAQClean\quotes\IBM_quotes.npy"
#     trades = np.load(Path1, allow_pickle=True).item()
#     quotes = np.load(Path2, allow_pickle=True).item()
#     getprice=getIntervalPrice(quotes,trades,5)
#     a=getprice.get_trade_price()
#     b=getprice.get_quote_price()
#     print(len(a),len(b[0]),len(getprice.returnQuoteTime()),len(getprice.returnTradeTime()))