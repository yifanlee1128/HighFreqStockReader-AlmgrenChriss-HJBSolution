from Reader.FileNames import FileNames as FM
from Reader.TAQTradesReader import TAQTradesReader
from Reader.TAQQuotesReader import TAQQuotesReader
import numpy as np


class TAQAdjust(object):
    def __init__(self,ticker,dateList,sp500):

        """
        :param ticker: string, the name of a stock
        :param dateList: the list of date, it is used to define the range of incoming processed data
        :param sp500: the data structure from file "readSP500.py"
        """
        self.dateList=dateList
        self.ticker=ticker
        self._sp500 = sp500

    def adjust_trades(self,tradeData,ticker):
        """
        this function is used to adjust trades data
        :param tradeData: dict with structure {{key:date(string},value:dictionary(subdict)}
                subdict with structure{{key: N,value: int};{key:MillisFromMidn,value:int};{key:Size,value: array of int};{key:Price,value:array of float}}
        :param ticker: string, the name of a stock
        :return: dict with structure {{key:date(string},value:dictionary(subdict)}
                subdict with structure{{key: N,value: int};{key:MillisFromMidn,value:int};{key:Size,value: array of int};{key:Price,value:array of float}}
        """
        # if set{factor}=1, no need to adjust
        if len(set(self._sp500.get_px_factorList(ticker))) != 1:
            # loop over dates to adjust share price and volume
            print("Processing "+ticker+"'s tading data...")
            for date in tradeData:
                px_factor = self._sp500.get_px_factor(ticker, date)
                vol_factor = self._sp500.get_vol_factor(ticker, date)
                tradeData[date]["Price"]=tradeData[date]["Price"]/float(px_factor)
                tradeData[date]["Size"]=tradeData[date]["Size"]*float(vol_factor)
        else:
            print("We do not process "+ticker+"'s trading data...")
        return tradeData

    def adjust_quotes(self,quoteData,ticker):
        """
        this function is used to adjust quotes data
        :param quoteData: dict with structure {{key:date(string},value:dictionary(subdict)}
                 subdict {{key: N,value: int};{key:MillisFromMidn,value:int};{key:AskSize,value: array of int};
                                                {key:AskPrice,value:array of float};{key:BidSize,value: array of int};
                                                {key:BidPrice,value:array of float}}
        :param ticker: string, the name of a stock
        :return: dict with structure {{key:date(string},value:dictionary(subdict)}
                subdict {{key: N,value: int};{key:MillisFromMidn,value:int};{key:AskSize,value: array of int};
                                                {key:AskPrice,value:array of float};{key:BidSize,value: array of int};
                                                {key:BidPrice,value:array of float}}
        """
        if len(set(self._sp500.get_vol_factorList(ticker))) != 1:
            print("Processing " + ticker + "'s quoting data...")
            # loop over dates to adjust quotes bid/ask price and volume
            for date in quoteData:
                px_factor = self._sp500.get_px_factor(ticker, date)
                vol_factor = self._sp500.get_vol_factor(ticker, date)
                quoteData[date]["AskPrice"]=quoteData[date]["AskPrice"]/float(px_factor)
                quoteData[date]["BidPrice"]=quoteData[date]["BidPrice"]/float(px_factor)
                quoteData[date]["AskSize"]=quoteData[date]["AskSize"]*float(vol_factor)
                quoteData[date]["BidSize"]=quoteData[date]["BidSize"]*float(vol_factor)
        else:
            print("We do not process "+ticker+"'s quoting data...")
        return quoteData

    def doTradeCalculation(self,tradeData,ticker):
        # do adjustment, or you cal also do some other calculation here
        return self.adjust_trades(tradeData,ticker)

    def doQuoteCalculation(self,quoteData,ticker):
        # do adjustment, or you cal also do some other calculation here
        return self.adjust_quotes(quoteData,ticker)

    def getQuoteData(self,Ticker):
        """
        this function is used to retrieve quote data from zipped data and convert it into dictionary
        :param Ticker: string, the name of a stock
        :return: dict with structure {{key:date(string},value:dictionary(subdict)}
                 subdict {{key: N,value: int};{key:MillisFromMidn,value:int};{key:AskSize,value: array of int};
                                                {key:AskPrice,value:array of float};{key:BidSize,value: array of int};
                                                {key:BidPrice,value:array of float}}

        """
        quotedata={}
        print("Packaging "+Ticker+"'s quoting data...")
        if len(self.dateList)<=len(self._sp500.get_dates(Ticker)):
            newDateList=self.dateList
        else:
            print(Ticker,"'s quoting data has shorter date range!")
            newDateList=self._sp500.get_dates(Ticker)
        for date in newDateList:
            path=FM.BinRQQuotesDir+'/'+date+'/'+Ticker+"_quotes.binRQ"
            dailyquotedata={}
            try:
                reader = TAQQuotesReader(path)
                dailyquotedata['N']=reader.getN()
                dailyquotedata['SecsFromEpocToMidn']=reader.getSecsFromEpocToMidn()
                dailyquotedata['MillisFromMidn']=np.array(reader._ts)
                dailyquotedata['AskSize']=np.array(reader._as)
                dailyquotedata['AskPrice']=np.array(reader._ap)
                dailyquotedata['BidSize']=np.array(reader._bs)
                dailyquotedata['BidPrice'] = np.array(reader._bp)
                quotedata[date]=dailyquotedata
            except:
                quotedata[date]=None
        return quotedata

    def getTradeData(self,Ticker):
        """
        this function is used to retrieve trade data from zipped data and convert it into dictionary
        :param Ticker: string, the name of a stock
        :return: dict with structure {{key:date(string},value:dictionary(subdict)}
                subdict with structure{{key: N,value: int};{key:MillisFromMidn,value:int};{key:Size,value: array of int};{key:Price,value:array of float}}
        """
        tradedata={}
        print("Packaging " + Ticker + "'s trading data...")
        if len(self.dateList)<=len(self._sp500.get_dates(Ticker)):
            newDateList=self.dateList
        else:
            print(Ticker, "'s trading data has shorter date range!")
            newDateList=self._sp500.get_dates(Ticker)
        for date in newDateList:
            path=FM.BinRTTradesDir+'/'+date+'/'+Ticker+"_trades.binRT"
            dailytradedata={}
            try:
                reader = TAQTradesReader(path)
                dailytradedata['N']=reader.getN()
                dailytradedata['SecsFromEpocToMidn']=reader.getSecsFromEpocToMidn()
                dailytradedata['Price']=np.array(reader._p)
                dailytradedata['MillisFromMidn']=np.array(reader._ts)
                dailytradedata['Size']=np.array(reader._s)

                tradedata[date]=dailytradedata
            except:
                tradedata[date]=None
        return tradedata

    def saveTradesNPY(self,tradedata,ticker):
        """
        this function is used to save the adjusted trade data to local files
        :param tradedata: dict
        :param ticker: string
        :return: None
        """
        np.save(FM.AdjustTradeResult+'/'+ticker+'_trades.npy',tradedata)

    def saveQuotesNPY(self,quotedata,ticker):
        """
        this function is used to save the adjusted quote data to local files
        :param quotedata: dict
        :param ticker: string
        :return: None
        """
        np.save(FM.AdjustQuoteResult + '/' + ticker + '_quotes.npy', quotedata)

    def runTrades(self):
        """
        this function is used to do all actions on trades data
        :return: dict, adjusted trade data
        """
        adjustedTradeData=self.doTradeCalculation(self.getTradeData(self.ticker),self.ticker)
        self.saveTradesNPY(adjustedTradeData,self.ticker)
        return adjustedTradeData

    def runQuotes(self):
        """
        this function is used to do all actions on quotes data
        :return: dict,adjusted quote data
        """
        adjustedQuoteData=self.doQuoteCalculation(self.getQuoteData(self.ticker),self.ticker)
        self.saveQuotesNPY(adjustedQuoteData,self.ticker)
        return adjustedQuoteData




# if __name__ == "__main__":
#     print(str(Path(os.getcwd()).parent))


