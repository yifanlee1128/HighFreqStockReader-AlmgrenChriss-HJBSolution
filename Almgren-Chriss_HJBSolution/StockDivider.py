import numpy as np
from dbReaders.TAQTradesReader import TAQTradesReader
from impactModel.FileManager import FileManager
from dbReaders.FileNames import FileNames

"""
This class is used to divide the whole stocks into two parts: high volume stocks and low volume stocks
"""

class StockDivider(object):
    def __init__(self,stockList,startDate="20070620",endDate="20070921"):
        """

        :param stockList: list of stock names
        :param startDate: string of start date
        :param endDate:  string of end date
        """
        self.stockList=stockList
        self.fm = FileManager(FileNames.TAQR)
        listOfDates = self.fm.getTradeDates(startDate, endDate)
        self.listOfDates = listOfDates
        self.highVolumeStockList=[]
        self.lowVolumeStockList=[]
        self.dict={}

    def doSummary(self):
        """
        this fucntion is used to gather the total volume of stocks
        """
        for name in self.stockList:
            tempVolume=0.
            for dateStr in self.listOfDates:
                rawTradeDataPath = FileNames.BinRTTradesDir + '/' + dateStr + '/' + name + '_trades.binRT'
                tradeReader = TAQTradesReader(rawTradeDataPath)
                tempVolume=tempVolume+np.nansum(tradeReader._s)/10000.0 # divide 10000 because otherwise the sum could exceed the range of int32
            self.dict[name]=tempVolume

    def doClassification(self):
        """
        this function is used to rank the volume and divide the whole stock into two parts
        """
        halfIndex=int(len(self.dict)/2)
        i=0
        for k, v in sorted(self.dict.items(), key=lambda item: item[1]):
            if i<halfIndex:
                self.lowVolumeStockList.append(k)
            else:
                self.highVolumeStockList.append(k)
            i=i+1

    def returnTwoList(self):
        return (self.lowVolumeStockList,self.highVolumeStockList)

if __name__=="__main__":
    stockList = open("NewListOfStock.txt", 'r').read().splitlines()
    stockDivider=StockDivider(stockList)
    stockDivider.doSummary()
    stockDivider.doClassification()
    list1,list2=stockDivider.returnTwoList()
    file1 = open("LowVolumeStockList.txt", "w")
    for i in list1:
        file1.write(i + '\n')
    file1.close()
    print(list1)
    file2 = open("HighVolumeStockList.txt", "w")
    for i in list2:
        file2.write(i + '\n')
    file2.close()
    print(list2)
    print("Finishied!")



