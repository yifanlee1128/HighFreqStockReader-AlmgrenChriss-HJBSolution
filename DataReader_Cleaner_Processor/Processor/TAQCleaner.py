import numpy as np
import copy

class TAQCleaner(object):

    def __init__(self, quotes, trades, ticker, k=25, gamma=.0005):
        '''

        :param quotes:dict with structure {{key:date(string},value:dictionary(subdict)}
                subdict {{key: N,value: int};{key:MillisFromMidn,value:int};{key:AskSize,value: array of int};
                                                {key:AskPrice,value:array of float};{key:BidSize,value: array of int};
                                                {key:BidPrice,value:array of float}}
        :param trades: dict with structure {{key:date(string},value:dictionary(subdict)}
                subdict with structure{{key: N,value: int};{key:MillisFromMidn,value:int};{key:Size,value: array of int};{key:Price,value:array of float}}
        :param ticker: string
        :param k: parameter to identify outliers
        :param gamma: parameter to identify outliers
        '''
        self._quotes = quotes
        self._trades = trades
        self._ticker = ticker
        self._k = k
        self._gamma = gamma
        self._dictForTradePloting={} #the dict is used to pinpoint outliers when plotting
        self._dictForQuotePloting={} #the dict is used to pinpoint outliers when plotting

    def get_indexList(self,index, number, length):
        """
        this function is used to generate the index list of neighbors of a price (then we can get the neighbors to calculate the mean and std to identify outliers)
        :param index:
        :param number:
        :param length: length of the indexlist
        :return:
        """
        res = [i + index for i in list(range(int(-1 * number / 2 + 0.01), int(number / 2 + 1)))]
        if res[0] < 0:
            temp = abs(res[0])
            res = [i + temp for i in res]
        if res[-1] >= length:
            temp = res[-1] - length + 1
            res = [i - temp for i in res]
        return res

    def calculateMeanStd(self,indexList, price):
        """
        this function is used to calculate the mean and std of all neighbors of a price
        :param indexList:  from above function
        :param price: list of price
        :return: mean and std
        """
        sum_X = 0.
        sum_XX = 0.
        n = len(indexList)
        for i in indexList:
            sum_X = sum_X + price[i]
            sum_XX = sum_XX + price[i] ** 2
        mean = sum_X / n
        if ((sum_XX / n - (mean) ** 2))>=0.:
            std = np.sqrt((sum_XX / n - (mean) ** 2))
        elif ((sum_XX / n - (mean) ** 2))<-1.e-10:
            raise ValueError("negative value occurs in square root function")
        else:
            std=0.
        return mean, std

    def getMeanandStd(self,price, number):
        """
        this function is used to get the list of mean and std corresponding to the list of price
        :param price: list of price
        :param number: the length of required neighbors
        :return:
        """
        length = len(price)
        mean = []
        std = []
        for i in range(length):
            tempmean, tempstd = self.calculateMeanStd(self.get_indexList(i, number, length), price)
            mean.append(tempmean)
            std.append(tempstd)
        return np.array(mean), np.array(std)

    def clean_trades(self):
        """
        this function is used to clean trade data
        :return: cleaned trade data
        """
        print("Cleaning "+self._ticker+"'s trading data...")

        for key in self._trades:
            trade_copy = copy.deepcopy(self._trades[key])
            trade_px = trade_copy["Price"]
            #if length of trade date is less than the parameter k ,we cannot identify outlier for this data
            if len(trade_px)>self._k:
                rolling_mean, rolling_std = self.getMeanandStd(trade_px, self._k)

                trade_px = trade_px
                rolling_mean = rolling_mean
                rolling_std =rolling_std
                #identify outliers
                result = abs(trade_px - rolling_mean) <= (2 * rolling_std + self._gamma * rolling_mean)
                index = []
                for i, j in enumerate(result):
                    if not j:
                        index.append(i)
                print("On " + key, ",find " + str(len(index)) + " outlier(s)")
                #delete outliers
                trade_copy["Price"]=np.delete(trade_px,index)
                trade_copy["Size"] = np.delete(trade_copy["Size"], index)
                trade_copy["MillisFromMidn"]=np.delete(trade_copy["MillisFromMidn"],index)
                trade_copy["N"]=trade_copy["N"]-len(index)
                self._trades[key]=trade_copy

                self._dictForTradePloting[key]=~result
                #print(len(self._dictForTradePloting[key][self._dictForTradePloting[key]]))
            else:
                print("On " + key,", we do not have enough data to identify outliers for",self._ticker,"trading data")
                self._dictForTradePloting[key]=np.array([False] * len(trade_px))
        return self._trades

    def clean_quotes(self):
        """
        same explaination with clean_trades
        :return:
        """
        print("Cleaning " + self._ticker + "'s quoting data...")
        for key in self._quotes:
            quote_copy = copy.deepcopy(self._quotes[key])
            quote_px = (quote_copy["AskPrice"]+quote_copy["BidPrice"])/2
            if len(quote_px)>self._k:
                rolling_mean, rolling_std = self.getMeanandStd(quote_px, self._k)

                rolling_mean =rolling_mean
                rolling_std = rolling_std
                result = abs(quote_px- rolling_mean) <= (2 * rolling_std + self._gamma * rolling_mean)
                index = []
                for i, j in enumerate(result):
                    if not j:
                        index.append(i)
                print("On " + key, ",find " + str(len(index)) + " outlier(s)")
                quote_copy["AskPrice"]=np.delete(quote_copy["AskPrice"],index)
                quote_copy["AskSize"] = np.delete(quote_copy["AskSize"], index)
                quote_copy["BidPrice"] = np.delete(quote_copy["BidPrice"], index)
                quote_copy["BidSize"] = np.delete(quote_copy["BidSize"], index)
                quote_copy["MillisFromMidn"]=np.delete(quote_copy["MillisFromMidn"],index)
                quote_copy["N"]=quote_copy["N"]-len(index)
                self._quotes[key]=quote_copy

                self._dictForQuotePloting[key]=~result
            else:
                print("On " + key, ", we do not have enough data to identify outliers for", self._ticker,
                      "quoting data")
                self._dictForQuotePloting[key]=np.array([False]*len(quote_px))

        return self._quotes

    def get_quoteOutlierSymbol(self):
        return self._dictForQuotePloting

    def get_tradeOutlierSymbol(self):
        return self._dictForTradePloting


# if __name__ == "__main__":
#     Path1=r"D:\Algo Trading & Quant Strats\Homework\Homework1_Lee\TAQAdjust\trades\UIS_trades.npy"
#     Path2=r"D:\Algo Trading & Quant Strats\Homework\Homework1_Lee\TAQAdjust\quotes\UIS_quotes.npy"
#     RTN_trades = np.load(Path1, allow_pickle=True).item()
#     RTN_quotes=np.load(Path2, allow_pickle=True).item()
#
#     cleaner1 = TAQCleaner(quotes=RTN_quotes, trades=RTN_trades, ticker="RTN")
#     cleaner1.clean_trades()
#     print(1)
#     cleaner1.clean_quotes()