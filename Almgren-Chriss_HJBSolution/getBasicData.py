import numpy as np
import pandas as pd
from impactModel.FileManager import FileManager
from dbReaders.FileNames import FileNames
from dbReaders.TAQQuotesReader import TAQQuotesReader
from dbReaders.TAQTradesReader import TAQTradesReader
from impactModel.VWAP import VWAP
from impactModel.ReturnBuckets import ReturnBuckets
from impactModel.TickTest import TickTest
#This is the version without adjustments for splits

class DataCollector(object):
    def __init__(self,listOfStocks,numBuckets=195,startDate="20070620",endDate="20070921"):

        """
        :param listOfStocks: a list of stock names
        :param numBuckets: in this case, it should be 195 because (16-9.5)*60/2=195
        """

        self.listOfStocks=listOfStocks
        self.startDate=startDate
        self.endDate=endDate

        # get the date list
        self.fm=FileManager( FileNames.TAQR )
        listOfDates = self.fm.getTradeDates(startDate, endDate)
        self.listOfDates=listOfDates

        #initiate the matrix
        self.Matrix_midQuoteReturn_2min = np.empty([len(self.listOfStocks), len(self.listOfDates)*numBuckets])
        self.Matrix_totalDailyVolume = np.empty([len(self.listOfStocks), len(self.listOfDates)])
        self.Matrix_arrivalPrice = np.empty([len(self.listOfStocks), len(self.listOfDates)])
        self.Matrix_imbalance = np.empty([len(self.listOfStocks), len(self.listOfDates)])
        self.Matrix_VWAP_to_3_30PM = np.empty([len(self.listOfStocks), len(self.listOfDates)])
        self.Matrix_VWAP_to_4_00PM = np.empty([len(self.listOfStocks), len(self.listOfDates)])
        self.Matrix_terminalPrice = np.empty([len(self.listOfStocks), len(self.listOfDates)])
        self.Matrix_dailyValue = np.empty([len(self.listOfStocks), len(self.listOfDates)])

        count1=0
        for name in listOfStocks:
            print("Currently processing "+str(count1+1)+"th stock: "+name+"...")
            count2=0
            for dateStr in listOfDates:

                # access raw data
                rawTradeDataPath=FileNames.BinRTTradesDir+'/'+dateStr+'/'+name+'_trades.binRT'
                rawQuoteDataPath=FileNames.BinRQQuotesDir+'/'+dateStr+'/'+name+'_quotes.binRQ'
                quoteReader=TAQQuotesReader(rawQuoteDataPath)
                tradeReader=TAQTradesReader(rawTradeDataPath)
                start930 = 19 * 60 * 60 * 1000 / 2
                end330= 31 * 60 * 60 * 1000 / 2
                end400 = 16 * 60 * 60 * 1000

                #calculate VWAP
                try:
                    VWAP_to_4_00PM=VWAP(tradeReader,start930,end400).getVWAP()
                    self.Matrix_VWAP_to_4_00PM[count1,count2]=VWAP_to_4_00PM
                except:
                    VWAP_to_4_00PM=None
                    self.Matrix_VWAP_to_4_00PM[count1,count2]=None

                try:
                    VWAP_to_3_30PM = VWAP(tradeReader, start930, end330).getVWAP()
                    self.Matrix_VWAP_to_3_30PM[count1, count2] = VWAP_to_3_30PM
                except:
                    VWAP_to_3_30PM = None
                    self.Matrix_VWAP_to_3_30PM[count1, count2] = None

                #calculate arrival price and terminal price
                try:
                    if quoteReader.getN()<5:
                        raise ValueError("Error")
                    lastFiveMidQuote=[ (quoteReader.getAskPrice(i)+quoteReader.getBidPrice(i))/2.0for i in range(quoteReader.getN()-5,quoteReader.getN(),1)]
                    terminalPrice=np.average(lastFiveMidQuote)
                    self.Matrix_terminalPrice[count1,count2]=terminalPrice
                except:
                    self.Matrix_terminalPrice[count1, count2] = None

                try:
                    firstFiveMidQuote = [(quoteReader.getAskPrice(i) + quoteReader.getBidPrice(i)) / 2.0 for i in range(5)]
                    arrivalPrice = np.average(firstFiveMidQuote)
                    self.Matrix_arrivalPrice[count1, count2] = arrivalPrice
                except:
                    self.Matrix_arrivalPrice[count1, count2] = None
                #calculate 2 min mid quote return
                try:
                    returnsGenerator=ReturnBuckets(tradeReader,start930,end400,numBuckets)
                    midQuoteReturn_2min=[returnsGenerator.getReturn(i) for i in range(numBuckets)]
                    self.Matrix_midQuoteReturn_2min[count1,count2*numBuckets:(count2+1)*numBuckets]=midQuoteReturn_2min
                except:
                    self.Matrix_midQuoteReturn_2min[count1, count2 * numBuckets:(count2 + 1) * numBuckets] =None

                #calculate daily volume
                try:
                    totalDailyVolume=sum([tradeReader.getSize(i) for i in range(tradeReader.getN())])
                    self.Matrix_totalDailyVolume[count1,count2]=totalDailyVolume
                except:
                    totalDailyVolume=None
                    self.Matrix_totalDailyVolume[count1, count2] =None

                #calculate imbalance value
                try:
                    tickTester=TickTest()
                    classifications=tickTester.classifyAll(tradeReader,start930,end330)
                    if VWAP_to_3_30PM==None:
                        self.Matrix_imbalance[count1, count2] =None
                    else:
                        imbalance=0.
                        for i in range(len(classifications)):
                            imbalance=imbalance+classifications[i][2]*tradeReader.getSize(i)
                        self.Matrix_imbalance[count1,count2]=imbalance*VWAP_to_3_30PM
                except:
                    self.Matrix_imbalance[count1, count2] =None


                #calculate daily value
                try:
                    dailyValue=VWAP_to_4_00PM*totalDailyVolume
                    self.Matrix_dailyValue[count1,count2]=dailyValue
                except:
                    self.Matrix_dailyValue[count1, count2] =None

                count2=count2+1

            count1=count1+1


    def getMatrix_midQuoteReturn_2min(self):
        return self.Matrix_midQuoteReturn_2min,self.listOfStocks,self.listOfDates

    def getMatrix_totalDailyVolume(self):
        return self.Matrix_totalDailyVolume,self.listOfStocks,self.listOfDates

    def getMatrix_arrivalPrice(self):
        return self.Matrix_arrivalPrice,self.listOfStocks,self.listOfDates

    def getMatrix_imbalance(self):
        return self.Matrix_imbalance,self.listOfStocks,self.listOfDates

    def getMatrix_VWAP_to_3_30PM(self):
        return self.Matrix_VWAP_to_3_30PM,self.listOfStocks,self.listOfDates

    def getMatrix_VWAP_to_4_00PM(self):
        return self.Matrix_VWAP_to_4_00PM,self.listOfStocks,self.listOfDates

    def getMatrix_terminalPrice(self):
        return self.Matrix_terminalPrice,self.listOfStocks,self.listOfDates

    def getMatrix_dailyValue(self):
        return self.Matrix_dailyValue,self.listOfStocks,self.listOfDates

    def get_stockList(self):
        return self.listOfStocks

    def get_dateInterval(self):
        return (self.startDate,self.endDate)



if __name__=="__main__":
    #stockList = open("ListOfMoreStock.txt", 'r').read().splitlines()
    stockList=["IBM","VPS"]
    print(len(stockList))
    dataCollector=DataCollector(stockList)

    # data1,StockList,DateList=dataCollector.getMatrix_dailyValue()
    # pd.DataFrame(data1,index=StockList,columns=DateList).to_csv("dailyValue.csv")
    #
    # data2,StockList,DateList=dataCollector.getMatrix_arrivalPrice()
    # pd.DataFrame(data2, index=StockList, columns=DateList).to_csv("arrivalPrice.csv")
    #
    # data3, StockList, DateList = dataCollector.getMatrix_imbalance()
    # pd.DataFrame(data3, index=StockList, columns=DateList).to_csv("imbalance.csv")
    #
    # data4, StockList, DateList = dataCollector.getMatrix_midQuoteReturn_2min()
    # pd.DataFrame(data4, index=StockList).to_csv("midQuoteReturn_2min.csv")
    #
    # data5, StockList, DateList = dataCollector.getMatrix_terminalPrice()
    # pd.DataFrame(data5, index=StockList, columns=DateList).to_csv("terminalPrice.csv")
    #
    # data6, StockList, DateList = dataCollector.getMatrix_totalDailyVolume()
    # pd.DataFrame(data6, index=StockList, columns=DateList).to_csv("totalDailyVolume.csv")
    #
    # data7, StockList, DateList = dataCollector.getMatrix_VWAP_to_3_30PM()
    # pd.DataFrame(data7, index=StockList, columns=DateList).to_csv("VWAP_to_3_30PM.csv")
    #
    # data8, StockList, DateList = dataCollector.getMatrix_VWAP_to_4_00PM()
    # pd.DataFrame(data8, index=StockList, columns=DateList).to_csv("VWAP_to_4_00PM.csv")


    print("Finished!")
