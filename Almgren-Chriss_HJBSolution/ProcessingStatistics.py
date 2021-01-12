import numpy as np
from impactModel.FileManager import FileManager
from dbReaders.FileNames import FileNames
from dbReaders.TAQQuotesReader import TAQQuotesReader
from dbReaders.TAQTradesReader import TAQTradesReader
from impactModel.VWAP import VWAP
from impactModel.ReturnBuckets import ReturnBuckets
from impactModel.TickTest import TickTest
from OurCode.getBasicData import DataCollector

class Processor(object):
    def __init__(self,dataCollector):

        """
        :param dataCollector: dataCollector from getBasicData class, use of processing data
        """
        self.dataCollector=dataCollector
        self.Matrix_midQuoteReturn_2min=dataCollector.getMatrix_midQuoteReturn_2min()## 2 mins return for rolling
        self.Matrix_dailyValue=dataCollector.getMatrix_dailyValue()
        self.stockList=dataCollector.get_stockList()# stock tickers
        self.date=dataCollector.getMatrix_dailyValue()[2] # running date


    def get_ten_day_average_value_Matrix(self):
        """compute 10 day moving average for daily values
            return format np.narray
            [[moving averages...],[Tickers],[Time]]
            """
        value=self.dataCollector.getMatrix_dailyValue()[0]

        def moving_averages(lists, period):
            """take list, return its n-periof moving average"""
            result = [0] * (len(lists) - period + 1)
            for i in range(len(lists) - period + 1):
                result[i] = np.mean(lists[i:(i + period)])
            return result

        ma=[]
        for stocks in value:
                ma.append(moving_averages(stocks, 10))

        ten_day_average_value_Matrix=np.array([ma,self.stockList,self.date[9:]])

        return ten_day_average_value_Matrix

    def get_ten_day_std_Matrix(self):
        """compute 10 day std for 2 mins midQuoteReturn
            return format np.narray
            [[moving stds],[Tickers],[Time]]
            """

        def moving_std(lists, period):
            """Moving std fo 10-day window in 195*10 available points
            assume 56 days
            """
            result = [0] * (56)
            for i in range(56):
                tempdata = lists[(195 * i):(195 * i + period * 195)]
                tem = [x for x in tempdata if np.isnan(x) == False]
                result[i] = np.std(tem)
            return result
        moving_average=[]
        for stocks_return in self.Matrix_midQuoteReturn_2min[0]:
                moving_average.append(moving_std(stocks_return,10))

        ten_day_returnStd_Matrix=np.array([moving_average,self.stockList,self.date[9:]])

        return ten_day_returnStd_Matrix


    def get_sigma_Matrix(self):
        """scaled sigma from rolling 10-day std, scaled to 1 day ( original 2mins -> one day, multiply np.sqrt(195)"""
        stocks_stds=self.get_ten_day_std_Matrix()[0]
        sigma_Matrix=[]
        for stocks in stocks_stds:
            sigma_Matrix.append([x*np.sqrt(195) for x in stocks])
        return sigma_Matrix





if __name__=="__main__":
    print("start")
    dataCollector = DataCollector(['AAPL','GE','GOOG','INTC','JPM','MSFT','ORCL','PFE','XOM'])## test 9 stocks
    pro = Processor(dataCollector)
    print('done')

    ma4 = pro.get_ten_day_average_value_Matrix()
    std = pro.get_ten_day_std_Matrix()
    std_matrix=pro.get_sigma_Matrix()
    print('done processing')
    import pandas as pd
    """the following collects the required data for running regression,
    saved as csv files for import
    """
    average_value=pd.DataFrame(ma4[0])
    average_value.index=ma4[1]
    average_value.to_csv("dailyAverage_9.csv")## matrix of dailyAverage value

    sigma=pd.DataFrame(std_matrix)
    sigma.index=ma4[1]
    sigma.to_csv("SigmaMatrix_9.csv")## sigma matrix

    imbalance=pd.DataFrame(dataCollector.getMatrix_imbalance()[0],index=ma4[1])
    imbalance=imbalance.T[9:].T ## match size
    imbalance.columns=sigma.columns
    imbalance.to_csv("imbalance_9.csv")## imbalance matrix

    arrival_price = pd.DataFrame(dataCollector.getMatrix_arrivalPrice()[0], index=ma4[1])
    arrival_price=arrival_price.T[9:].T
    arrival_price.columns=sigma.columns ## match columns
    arrival_price.to_csv("ArrivalPrice_9.csv")## arrival price matrix

    terminal_price = pd.DataFrame(dataCollector.getMatrix_terminalPrice()[0], index=ma4[1])
    terminal_price=terminal_price.T[9:].T
    terminal_price.columns=sigma.columns
    terminal_price.to_csv("terminalPrice_9.csv")  ## terminal price matrix

    vwap_330 = pd.DataFrame(dataCollector.getMatrix_VWAP_to_3_30PM()[0], index=ma4[1])
    vwap_330=vwap_330.T[9:].T
    vwap_330.columns=sigma.columns
    vwap_330.to_csv("VWAP_330PM_9.csv")  ## VWAP_330 matrix








