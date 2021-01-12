from Processor.TAQCleaner import TAQCleaner
from Processor.TAQAdjust import TAQAdjust
from Processor.readSP500 import readSP500
from Reader.FileManager import FileManager
from Reader.FileNames import FileNames as FM
import numpy as np
import os
from pathlib import Path

class DataProcessor(object):
    """
    DataProcessor is used to generated and save all trade and quote data of S&P500 stocks between 20070620 to 20070920
    """
    def __init__(self,dateList,**kwargs):
        """

        :param dateList: a list of date
        :param kwargs: if you enter tickerLit as parameter, then DataProcessor will just process the stocks within the list
        """
        sp500Path=str(Path(os.getcwd()).parent)+"\s_p500.xlsx"
        self.sp500=readSP500(sp500Path)
        if "tickerList" in kwargs:
            self.tickerList=kwargs["tickerList"]
        else:
            self.tickerList=self.sp500.get_tickers()

        self.dateList=dateList
        self.problemList=[]

    def run(self):
        for ticker in self.tickerList:
            try:
                """
                adjust and clean every stock and save them to seperate files
                """
                adjuster=TAQAdjust(ticker,self.dateList,self.sp500)
                trades=adjuster.runTrades()
                quotes=adjuster.runQuotes()
                cleaner=TAQCleaner(quotes,trades,ticker)
                cleanTrades=cleaner.clean_trades()
                cleanQuotes=cleaner.clean_quotes()
                np.save(FM.CleanTradeResult + '/' + ticker + '_trades.npy', cleanTrades)
                np.save(FM.CleanQuoteResult + '/' + ticker + '_quotes.npy', cleanQuotes)
            except:
                self.problemList.append(ticker)

    def showProblemTickers(self):
        print(self.problemList)


if __name__=="__main__":
    fm = FileManager(FM.TAQR)
    tickerList=["GILD"]
    dateList = fm.getQuoteDates("20070620", "20070921")
    dp=DataProcessor(dateList,tickerList=tickerList)
    dp.run()
    print(1)

