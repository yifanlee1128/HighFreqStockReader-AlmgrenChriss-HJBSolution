import numpy as np

"""
This script performs following tasks:
    1. display timestamp as seconds
    2. store endTS, startTS. Given X, divide data into bins 
    3. compute returns for data points in each bin
"""


class ReturnsCalculator(object):
    def __init__(self, quotes, trades, X,allowNaN=False):
        """

        :param quotes: dict
        :param trades: dict
        :param X: tiem interval
        :param allowNaN: boolean
        """
        self._quotes = quotes
        self._trades = trades
        self._X = X
        if allowNaN:
            self._filledValue=np.nan
        else:
            self._filledValue=0.

    def get_time_interval(self, X, startTS=34199000, endTS=57599000):
        """
        Given X-minute interval, the method divides data into bins
        :param X: time interval
        :param startTS: corresponding to 9:29:59 of each day
        :param endTS: corresponding to 15:59:59 of each day
        :return: list of timestamp
        """
        X_millis = X*60*1000
        num_bins = int((endTS-startTS)/X_millis)
        ts_intervals = [(startTS + i*X_millis) for i in range(num_bins+1)]
        if ts_intervals[-1]!=endTS:
            ts_intervals.append(endTS)
        return ts_intervals

    def get_trade_returns(self):
        """
        this function is to calculate returns in each timestamp
        :return: list of returns
        """
        totalReturns=np.array([])
        ts_intervals = self.get_time_interval(self._X)
        for key in self._trades:
            dailyData=self._trades[key]
            tempReturns=np.array([0.]*(len(ts_intervals)-1))
            i=0
            for l,r in zip(ts_intervals[:-1],ts_intervals[1:]):
                tempPrice=dailyData["Price"][np.logical_and(dailyData["MillisFromMidn"]>l,dailyData["MillisFromMidn"]<=r)]
                if len(tempPrice)>0:
                    tempReturns[i]=np.log(tempPrice[-1]/tempPrice[0])
                else:
                    tempReturns[i]=self._filledValue
                i=i+1
            totalReturns=np.concatenate([totalReturns,tempReturns],axis=None)
        return  totalReturns

    def get_quote_returns(self):
        """
        this function is to calculate returns in each timestamp
        :return: list of returns
        """
        totalReturns=np.array([])
        ts_intervals=self.get_time_interval(self._X)
        for key in self._quotes:
            dailyData=self._quotes[key]
            tempReturns=np.array([0.]*(len(ts_intervals)-1))
            i=0
            for l,r in zip(ts_intervals[:-1],ts_intervals[1:]):
                tempPrice=((dailyData["AskPrice"]+dailyData["BidPrice"])/2)[np.logical_and(dailyData["MillisFromMidn"]>l,dailyData["MillisFromMidn"]<=r)]
                if len(tempPrice)>0:
                    tempReturns[i]=np.log(tempPrice[-1]/tempPrice[0])
                else:
                    tempReturns[i]=self._filledValue
                i=i+1
            totalReturns=np.concatenate([totalReturns,tempReturns],axis=None)
        return totalReturns

# if __name__=="__main__":
#     fm = FileManager(FM.TAQR)
#     dateList = fm.getQuoteDates("20070620", "20070704")
#     tickerList = ['GILD',"IBM","PH"]
#     for ticker in tickerList:
#         sp500 = readSP500("s_p500.xlsx")
#         adjuster = TAQAdjust(ticker, dateList, sp500)
#         trades = adjuster.runTrades()
#         quotes = adjuster.runQuotes()
#         cleaner = TAQCleaner(quotes, trades, ticker)
#         newTrades=cleaner.clean_trades()
#         newQuotes=cleaner.clean_quotes()
#         returnCalculator=ReturnsCalculator(newQuotes, newTrades, 5)
#         print(returnCalculator.get_trade_returns())
#         print(returnCalculator.get_quote_returns())