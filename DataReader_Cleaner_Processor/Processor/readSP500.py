import pandas as pd
import numpy as np


class readSP500(object):
    '''
    Reads s_p500.xlsx and uses the ticker info to filter TAQ data
    '''

    def __init__(self, filePathName):
        self._filePathName = filePathName
        self._sp500 = pd.read_excel(self._filePathName)
        cols = ['Names Date', 'Ticker Symbol', 'Trading Symbol', 'Cumulative Factor to Adjust Prices',
                'Cumulative Factor to Adjust Shares/Vol', 'Shares Outstanding', 'Price or Bid/Ask Average']
        # select useful columns
        self._sp500 = self._sp500[cols]
        # drop missing rows
        self._sp500.dropna(subset=['Names Date', 'Ticker Symbol', 'Trading Symbol'], inplace=True)
        # use only the primary trading securities
        self._sp500 = self._sp500[self._sp500['Ticker Symbol'] == self._sp500['Trading Symbol']].reset_index(drop=True)
        self._sp500.drop(columns=['Trading Symbol'], inplace=True)
        # convert date to string type
        self._sp500['Names Date'] = self._sp500['Names Date'].astype(int).astype('str')


    def get_px_factor(self, ticker, date):
        """
        get factor value of a stock on a specific date
        :param ticker: string
        :param date: string
        :return: factor value
        """
        return self._sp500[(self._sp500["Names Date"] == date) & (self._sp500["Ticker Symbol"] == ticker)] \
            ['Cumulative Factor to Adjust Prices'].values[0]

    def get_vol_factor(self, ticker, date):
        """
        get factor value of a stock on a specific date
        :param ticker: string
        :param date: string
        :return: factor value
        """
        # return self._tickersDict[ticker][date][1]
        return self._sp500[(self._sp500["Names Date"] == date) & (self._sp500["Ticker Symbol"] == ticker)] \
            ['Cumulative Factor to Adjust Shares/Vol'].values[0]

    def get_sp500(self):
        return self._sp500

    def get_tickers(self):
        return np.array(list(set(self._sp500['Ticker Symbol'])))

    def get_dates(self, ticker):
        """
        get available dates of a stock
        :param ticker: string
        :return: list of dates
        """
        return self._sp500[self._sp500['Ticker Symbol']==ticker]['Names Date'].values

    def get_px_factorList(self, ticker):
        """
        get factor list of a stock
        :param ticker: string
        :return: list of factor
        """
        return self._sp500[self._sp500['Ticker Symbol']==ticker]['Cumulative Factor to Adjust Prices'].values

    def get_vol_factorList(self, ticker):
        """
        get factor list of a stock
        :param ticker: string
        :return: list of factor
        """
        return self._sp500[self._sp500['Ticker Symbol']==ticker]['Cumulative Factor to Adjust Prices'].values

# if __name__=="__main__":
#     df=readSP500('s_p500.xlsx')
#     a=df.get_vol_factor("PH","20070627")
#     print(a)

