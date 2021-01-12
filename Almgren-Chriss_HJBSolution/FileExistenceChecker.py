import numpy as np
import os.path
from impactModel.FileManager import FileManager
from dbReaders.FileNames import FileNames

"""
This class is used to check whether a stock has both trade and quote data in our database, if not, we delete it from our stock list
"""
class FileExistenceChecker(object):
    def __init__(self,listOfStocks,startDate="20070620",endDate="20070921"):
        """

        :param listOfStocks: list of stock name
        :param startDate:  string of start date
        :param endDate: string of end date
        """

        self.listOfStocks = listOfStocks
        self.startDate = startDate
        self.endDate = endDate

        #get date list
        self.fm = FileManager(FileNames.TAQR)
        listOfDates = self.fm.getTradeDates(startDate, endDate)
        self.listOfDates = listOfDates

        #this list is used to store name of stocks with missing data
        self.missingList=[]
    def checkFile(self):
        i=1
        total=len(self.listOfStocks)
        for name in self.listOfStocks:
            print("We are processing "+str(i)+" out of "+str(total))
            for dateStr in self.listOfDates:
                rawTradeDataPath = FileNames.BinRTTradesDir + '/' + dateStr + '/' + name + '_trades.binRT'
                rawQuoteDataPath = FileNames.BinRQQuotesDir + '/' + dateStr + '/' + name + '_quotes.binRQ'
                #decide whether data are missed
                if not (os.path.isfile(rawTradeDataPath) and os.path.isfile(rawQuoteDataPath)):
                    print("we are missing data of stock: "+name)
                    self.missingList.append(name)
                    break
            i=i+1

    def getNewList(self):
        # delete stock with missing data from list, return new list
        newNameList=[i for i in self.listOfStocks if i not in self.missingList]
        print("We delete "+str(len(self.missingList))+" stocks from origin list, new list has "+str(len(newNameList))+" elements.")
        return newNameList

if __name__=="__main__":
    stockList = open("ListOfMoreStock.txt", 'r').read().splitlines()
    print(len(stockList))
    checker=FileExistenceChecker(stockList)
    checker.checkFile()
    newList=checker.getNewList()
    print(newList)
    file = open("NewListOfStock.txt", "w")
    for i in newList:
        file.write(i + '\n')
    file.close()
