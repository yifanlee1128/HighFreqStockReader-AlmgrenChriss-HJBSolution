import numpy as np
from impactModel.FileManager import FileManager
from dbReaders.FileNames import FileNames
from dbReaders.TAQQuotesReader import TAQQuotesReader
from dbReaders.TAQTradesReader import TAQTradesReader
from impactModel.VWAP import VWAP
from impactModel.ReturnBuckets import ReturnBuckets
from impactModel.TickTest import TickTest
from OurCode.getBasicData import DataCollector
import pandas as pd
class StockSelection(object):
    """perform stockselection given the active stock list and less_active stock list
    we choose stocks that have less than 5% missing data in 2-mins returns,
    active stocks are from sp500 and less-active stocks are from the TAQ data, with full length of 65 days of 2-mins returns
    less-active stocks are chosen from the TAQ data, removed stocks from sp500, both have less than 5% missings"""

    def __init__(self, returnFile,significance):
        """
               :param returnFile: csv file directory with 2-mins returns, can be list
               :param significance: condition for number of missings, e.g significance*195*65 in total 195*65
               """

        #self.listOfStocks=listOfStocks
        self.returnFile=returnFile
        self.significance=significance

        selection=[]
        for file in returnFile:
            data=pd.read_csv(file,index_col=0)
            num=data.T.isna().sum()## number of missings
            index=num[num<significance*195*65].index.tolist()
            selection.append(index)
        self.selection=selection

    def getSelection(self):
        return self.selection














