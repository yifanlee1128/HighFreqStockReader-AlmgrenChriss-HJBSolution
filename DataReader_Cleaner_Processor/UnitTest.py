import unittest
from Reader.FileManager import FileManager
from Reader.FileNames import FileNames as FM
from Processor.readSP500 import readSP500
from Processor.TAQAdjust import TAQAdjust
from Processor.TAQCleaner import TAQCleaner
from StatsAnalysis.sp500 import *
from StatsAnalysis.ReturnsCalculator import ReturnsCalculator
from StatsAnalysis.getPrice import getIntervalPrice
from StatsAnalysis.LjungBoxTest import LjungBoxTest
from StatsAnalysis.TAQStats import TAQStats
from StatsAnalysis.cvxoptOnSP500 import run_cvxoptOnSP500
from Graph import *
import numpy as np
import pandas as pd

class UnitTest(unittest.TestCase):


    def testAll(self):
        #test readSP500
        df = readSP500('s_p500.xlsx')
        a = df.get_vol_factor("PH", "20070627")
        self.assertEqual(a, 1.5)

        #test TAQAdjust
        """
                before running this test, please make sure your FileNames contains all required paths described in the File
                """
        fm = FileManager(FM.TAQR)
        dateList = fm.getQuoteDates("20070620", "20070921")
        print("Dates range from:", dateList[0], "to", dateList[-1])
        tickerList = ['GILD']
        sp500 = readSP500("s_p500.xlsx")
        for i in tickerList:
            test = TAQAdjust(i, dateList, sp500)
            test.runQuotes()
            test.runTrades()
        try:
            Path1 = FM.AdjustTradeResult + "\GILD_trades.npy"
            Path2 = FM.AdjustQuoteResult + "\GILD_quotes.npy"
            trade = np.load(Path1, allow_pickle=True).item()
            quote = np.load(Path2, allow_pickle=True).item()

        except:
            raise FileNotFoundError("Test Failed, we cannot find the adjusted files")

        self.assertIsInstance(trade, dict)
        self.assertIsInstance(quote, dict)
        self.assertEqual(list(trade.keys()), dateList)
        self.assertEqual(list(quote.keys()), dateList)

        #test TAQClean
        Path1 = FM.AdjustTradeResult + "\GILD_trades.npy"
        Path2 = FM.AdjustQuoteResult + "\GILD_quotes.npy"
        GILD_trades = np.load(Path1, allow_pickle=True).item()
        GILD_quotes = np.load(Path2, allow_pickle=True).item()
        cleaner1 = TAQCleaner(quotes=GILD_quotes, trades=GILD_trades, ticker="GILD")
        cleanTrades = cleaner1.clean_trades()
        cleanQuotes = cleaner1.clean_quotes()
        np.save(FM.CleanTradeResult + '/' + "GILD" + '_trades.npy', cleanTrades)
        np.save(FM.CleanQuoteResult + '/' + "GILD" + '_quotes.npy', cleanQuotes)

        #test DataProcessor
        """
                We do not need to test Data Processor because it only use TAQAdjust and TAQCleaner which are tested above,
                DataProcessor is used to generate adjusted and cleaned data from all S&P500 stocks
                :return: None
        """

        #test sp500
        sp500Return()

        try:
            a = pd.read_csv("NormalReturn.csv", index_col=0)
            b = pd.read_csv("ExcessReturn.csv", index_col=0)

        except:
            raise FileNotFoundError("Test Failed, we cannot find the adjusted files")

        self.assertEqual(len(a.columns.values), 500)  # 500 stocks
        self.assertEqual(len(a.index.values), 65)  # 65 trading day in the period

        #test ReturnsCalculator & getPrice
        trade = np.load(FM.CleanTradeResult + '/' + "GILD" + '_trades.npy', allow_pickle=True).item()
        quote = np.load(FM.CleanQuoteResult + '/' + "GILD" + '_quotes.npy', allow_pickle=True).item()

        returnCalculator = ReturnsCalculator(quote, trade, 5)
        ar = returnCalculator.get_trade_returns()
        br = returnCalculator.get_quote_returns()
        getprice = getIntervalPrice(quote, trade, 5)
        ap = getprice.get_trade_price()
        bpa, bpb = getprice.get_quote_price()
        print(ar)
        print(br)
        print(ap)
        print(bpa)
        print(bpb)
        self.assertEqual(len(bpb), len(bpa))
        self.assertEqual(len(ar), len(ap))
        self.assertEqual(len(br), len(bpa))

        #test LjungBoxTest
        Path1 = FM.CleanTradeResult + "\GILD_trades.npy"
        Path2 = FM.CleanQuoteResult + "\GILD_quotes.npy"
        trades = np.load(Path1, allow_pickle=True).item()
        quotes = np.load(Path2, allow_pickle=True).item()
        bucket = np.arange(1, 60, 5)
        LB = LjungBoxTest(trades, quotes, bucket)
        minX = LB.tuneParam()
        print('Optimal bucket size for zero serial correlation', minX)

        #test TAQStats
        path1 = FM.CleanTradeResult + '/GILD_trades.npy'
        path2 = FM.CleanQuoteResult + '/GILD_quotes.npy'
        GILD_trades = np.load(path1, allow_pickle=True).item()
        GILD_quotes = np.load(path2, allow_pickle=True).item()
        # cleaner1 = TAQCleaner(quotes=GILD_quotes, trades=GILD_trades, ticker="GILD")
        # cleaner1.clean_trades()
        # cleaner1.clean_quotes()
        stats = TAQStats(GILD_trades, GILD_quotes, 5)
        print('Sample length in days for trades and quotes:', stats.get_sample_length())
        print('Total number of quotes:', stats.get_num_quotes())
        print('Total number of trades:', stats.get_num_trades())
        print('Trades to quotes ratio:', stats.get_TQ_ratio())
        print('Annualized mean returns for mid-quotes and trades:', stats.get_mean_returns())
        print('Annualized median returns for mid-quotes and trades:', stats.get_med_returns())
        print('Annualized standard deviation of returns for mid-quotes and trades:', stats.get_std())
        print('Annualized median absolute deviation for mid-quotes and trades:', stats.get_MAD())
        print('Skew of returns for mid-quotes and trades:', stats.get_skew())
        print('Kurtosis for mid-quotes and trades:', stats.get_kurtosis())
        print('10 largest returns for mid-quotes and trades:', stats.get_max_returns())
        print('10 smallest returns for mid-quotes and trades:', stats.get_min_returns())
        print('Maximum drawdown of mid-quotes and trades:', stats.get_max_drawdown())

        #test cvxoptOnSP500
        run_cvxoptOnSP500()

        #test graph
        ticker = ['GILD']
        trade_path = FM.AdjustTradeResult + '/GILD_trades.npy'
        quotes_path = FM.AdjustQuoteResult + '/GILD_quotes.npy'
        for ticker in ticker:
            graph_trades(ticker)
            graph_quotes(ticker)
        graph_cleaning(quotes_path, trade_path, 'GILD', '20070816', 'trades')
