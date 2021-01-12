from MyCode.ReturnsCalculator import ReturnsCalculator
import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox


class LjungBoxTest(object):
    """
    This script finds the optimal bucket size (for a given ticker) so that the return series (trade & mid-quote)
    exhibit no serial correlations.
    """
    def __init__(self, trades, quotes, X):
        """

        :param trades: adjusted & cleaned trades
        :param quotes: adjusted & cleaned quotes
        :param X: a range of values to search for the optimal bucket size
        """
        self._trades = trades
        self._quotes = quotes
        try:
            if len(X) > 1:
                self._X = sorted(X)
        except:
            raise Exception('Input X should be a list')

    def tuneParam(self):
        minX = 0
        for i in self._X:
            ret = ReturnsCalculator(self._quotes, self._trades, i)
            df_q = acorr_ljungbox(ret.get_quote_returns(), lags=np.arange(1,11),return_df=True)
            pval_q = np.array(df_q['lb_pvalue'])
            df_t = acorr_ljungbox(ret.get_trade_returns(), lags=np.arange(1,11),return_df=True)
            pval_t = np.array(df_t['lb_pvalue'])
            print('LB test for mid-quote returns with ' + str(i) + '-minute bucket size: ' + str(pval_q))
            print('LB test for trade returns with ' + str(i) + '-minute bucket size: ' + str(pval_t))
            if ((pval_q > .05) & (pval_t > .05)).all():
                minX = i
                break # found the smallest bucket size s.t. there's no serial correlation for all lags used
        return minX
#
# if __name__=="__main__":
#     Path1 = r"D:\Algo Trading & Quant Strats\Homework\Homework1_Lee\TAQClean\trades\GILD_trades.npy"
#     Path2 = r"D:\Algo Trading & Quant Strats\Homework\Homework1_Lee\TAQClean\quotes\GILD_quotes.npy"
#     trades = np.load(Path1, allow_pickle=True).item()
#     quotes = np.load(Path2, allow_pickle=True).item()
#     bucket = np.arange(1, 60, 5)
#     LB = LjungBoxTest(trades, quotes, bucket)
#     minX = LB.tuneParam()
#     print('Optimal bucket size for zero serial correlation', minX)

