import numpy as np
import pandas as pd
import scipy.stats as sp
import heapq
from Reader.FileNames import FileNames as FM
from StatsAnalysis.ReturnsCalculator import ReturnsCalculator
from StatsAnalysis.getPrice import getIntervalPrice
import os

class TAQStats(object):

    def __init__(self, trades, quotes, X):
        '''

        :param trades: trades data for the specified ticker
        :param quotes:
        '''
        self._trades = trades
        self._quotes = quotes
        self._X = X
        self._returns = ReturnsCalculator(self._quotes, self._trades, self._X)
        self._trade_return = self._returns.get_trade_returns()
        self._quote_return = self._returns.get_quote_returns()

    def get_sample_length(self):
        return len(self._trades), len(self._quotes)

    def get_trade_dates(self):
        return self._trades.keys()

    def get_num_trades(self):
        num_trades = 0
        for date in self.get_trade_dates():
            num_trades += self._trades[date]['N']
        return num_trades

    def get_quote_dates(self):
        return self._quotes.keys()

    def get_num_quotes(self):
        num_quotes = 0
        for date in self.get_quote_dates():
            num_quotes += self._quotes[date]['N']
        return num_quotes

    def get_TQ_ratio(self):
        return self.get_num_trades() / self.get_num_quotes()

    def get_mean_returns(self):
        mean_quote_ret = np.nanmean(self._quote_return) * 252*6.5*60/self._X
        mean_trade_ret = np.nanmean(self._trade_return) * 252*6.5*60/self._X
        return mean_quote_ret, mean_trade_ret

    def get_med_returns(self):
        med_quote_ret = np.nanmedian(self._quote_return) * 252*6.5*60/self._X
        med_trade_ret = np.nanmedian(self._trade_return) * 252*6.5*60/self._X
        return med_quote_ret, med_trade_ret

    def get_std(self):
        quote_std = np.nanstd(self._quote_return) * np.sqrt(252*6.5*60/self._X)
        trade_std = np.nanstd(self._trade_return) * np.sqrt(252*6.5*60/self._X)
        return quote_std, trade_std

    def get_MAD(self):
        quote_mad = sp.median_absolute_deviation(self._quote_return,nan_policy='omit') * 252
        trade_mad = sp.median_absolute_deviation(self._trade_return,nan_policy='omit') * 252
        return quote_mad, trade_mad

    def get_skew(self):
        quote_skew = sp.skew(self._quote_return,nan_policy='omit')
        trade_skew = sp.skew(self._trade_return,nan_policy='omit')
        return quote_skew, trade_skew

    def get_kurtosis(self):
        quote_kurt = sp.kurtosis(self._quote_return,nan_policy='omit')
        trade_kurt = sp.kurtosis(self._trade_return,nan_policy='omit')
        return quote_kurt, trade_kurt

    def get_max_returns(self, n=10):
        max_quote_ret = heapq.nlargest(n, self._quote_return)
        max_trade_ret = heapq.nlargest(n, self._trade_return)
        return max_quote_ret, max_trade_ret

    def get_min_returns(self, n=10):
        min_quote_ret = heapq.nsmallest(n, self._quote_return)
        min_trade_ret = heapq.nsmallest(n, self._trade_return)
        return min_quote_ret, min_trade_ret

    def get_max_drawdown(self):
        getprice = getIntervalPrice(self._quotes,self._trades,self._X)
        tradePrice = getprice.get_trade_price()
        roll_t_max = pd.DataFrame(tradePrice).cummax().to_numpy().T
        daily_t_drawdown = tradePrice / roll_t_max - 1.
        #max_t_drawdown = pd.DataFrame(daily_t_drawdown).cummin().to_numpy().T

        askPrice,bidPrice = getprice.get_quote_price()
        midquote = (askPrice+bidPrice)/2
        roll_q_max = pd.DataFrame(midquote).cummax().to_numpy().T
        daily_q_drawdown = midquote / roll_q_max - 1.
        #max_q_drawdown = pd.DataFrame(daily_q_drawdown).cummin().to_numpy().T
        return np.nanmin(daily_q_drawdown), np.nanmin(daily_t_drawdown)


if __name__ == "__main__":
    dict={}
    for x,symbol in zip([1 / 6, 0.5, 1, 5, 10, 30],["10s","30s","1m","5m","10m","30m"]):
        print(symbol)
        tempdict={}
        path1 = FM.CleanTradeResult + '/GILD_trades.npy'
        path2 = FM.CleanQuoteResult + '/GILD_quotes.npy'
        GILD_trades = np.load(path1, allow_pickle=True).item()
        GILD_quotes = np.load(path2, allow_pickle=True).item()
        # cleaner1 = TAQCleaner(quotes=GILD_quotes, trades=GILD_trades, ticker="GILD")
        # cleaner1.clean_trades()
        # cleaner1.clean_quotes()
        stats = TAQStats(GILD_trades, GILD_quotes, x)
        tempdict["samplelength"]=stats.get_sample_length()
        #print('Sample length in days for trades and quotes:', stats.get_sample_length())
        tempdict["totalquotes"]=stats.get_num_quotes()
        #print('Total number of quotes:', stats.get_num_quotes())
        tempdict["totaltrades"]=stats.get_num_trades()
        #print('Total number of trades:', stats.get_num_trades())
        tempdict["TQratio"]=stats.get_TQ_ratio()
        #print('Trades to quotes ratio:', stats.get_TQ_ratio())
        tempdict["meanreturn"]= stats.get_mean_returns()
        #print('Annualized mean returns for mid-quotes and trades:', stats.get_mean_returns())
        tempdict["medianreturn"]=stats.get_med_returns()
        #print('Annualized median returns for mid-quotes and trades:', stats.get_med_returns())
        tempdict["std"]=stats.get_std()
        #print('Annualized standard deviation of returns for mid-quotes and trades:', stats.get_std())
        tempdict["MAD"]=stats.get_MAD()
        #print('Annualized median absolute deviation for mid-quotes and trades:', stats.get_MAD())
        tempdict["skew"]=stats.get_skew()
        #print('Skew of returns for mid-quotes and trades:', stats.get_skew())
        tempdict["kurt"]=stats.get_kurtosis()
        #print('Kurtosis for mid-quotes and trades:', stats.get_kurtosis())
        tempdict["maxreturns"]=stats.get_max_returns()
        #print('10 largest returns for mid-quotes and trades:', stats.get_max_returns())
        tempdict["minreturns"]=stats.get_min_returns()
        #print('10 smallest returns for mid-quotes and trades:', stats.get_min_returns())
        tempdict["maxdrawdown"]=stats.get_max_drawdown()
        #print('Maximum drawdown of mid-quotes and trades:', stats.get_max_drawdown())
        dict[symbol]=tempdict
    np.save(os.getcwd() + '/stats_clean.npy', dict)



