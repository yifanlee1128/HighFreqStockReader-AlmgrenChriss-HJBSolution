from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from scipy import stats as st
from scipy.stats import stats
from sklearn.preprocessing import StandardScaler
from dbReaders.FileNames import FileNames
from statsmodels.stats.diagnostic import het_white

def func(X, eta, beta):
    X_sigma, X_X_V = X
    return eta * X_sigma * ((6.5 / 6.0 * X_X_V) ** beta)

def OLS(X, Y):
    X = sm.add_constant(X)
    results = sm.OLS(Y, X).fit()
    return results # contains results.params, _.tvalues, _.resid

def WLS(X, Y):
    ols = OLS(X, Y)
    u2 = np.log(ols.resid ** 2)
    ols2 = OLS(X, u2)
    w = np.exp(ols2.fittedvalues)
    X = sm.add_constant(X)
    results = sm.GLS(Y, X, weights=1/w).fit()
    return results

class nonlinearRegressionProcessor(object):
    def __init__(self, Matrix_arrivalPrice, Matrix_terminalPrice, Matrix_VWAP_330, Matrix_sigma, Matrix_imbalanceValue,
                 Matrix_avgdailyValue,func=func):
        g=(Matrix_terminalPrice-Matrix_arrivalPrice)/2
        # following variables should be nparray
        self._h=(((Matrix_VWAP_330-Matrix_arrivalPrice)-g).values).flatten()
        self._X=((Matrix_imbalanceValue).values).flatten()
        self._V = (Matrix_avgdailyValue.values).flatten()
        self._X_V=self._X/self._V
        self._X_V=abs(self._X_V)
        # get the sign of values in the imbalance value matrix
        self._signal=np.sign(Matrix_imbalanceValue)
        self._sigma = ((Matrix_sigma*self._signal).values).flatten()

        # if values do not satisfy certain conditions, we delete them from our samples
        deleteList=[]
        for i in range(len(self._X_V)):
            if  (self._sigma[i]==0. or self._X_V[i]==0):
                deleteList.append(i)
        # self._h[i] * self._sigma[i] < 0 or
        self._sigma=np.delete(self._sigma,deleteList)
        self._X_V=np.delete(self._X_V,deleteList)
        self._h=np.delete(self._h,deleteList)

        self._sigma=np.array(self._sigma, dtype=np.float64)
        self._X_V=np.array(self._X_V,dtype=np.float64)
        self._h=np.array(self._h,dtype=np.float64)


        self._beta=None
        self._eta=None
        self._residuals=None
        self._regularError=None
        self._heteroRobustError=None
        # following variable is a function
        self._func=func

    def doNonlinearRegression(self):
        #print(func((self._sigma,self._X_V),0.142,0.6))
        popt, _ = curve_fit(func, (self._sigma, self._X_V), self._h, p0=[0.142, 0.6],bounds=([-5.,-5],[1000.,4.]))
        self._eta=popt[0]
        self._beta=popt[1]
        self._residuals=self._h-func((self._sigma,self._X_V),self._eta,self._beta)
        self._stdError=np.sum(self._residuals*self._residuals)/(len(self._sigma)-2.)
        self._t_eta = self._eta/self._stdError
        self._t_beta = self._beta/self._stdError
        print('eta, beta, t_eta, t_beta', popt[0], popt[1], self._t_eta, self._t_beta)
        return popt


if __name__=="__main__":
    ActivePath1 = FileNames.ActiveDir
    LessActivePath2 = FileNames.LessActiveDir
    TotalPath3 = FileNames.TotalStockDir
    arrivalPrice1 = pd.read_csv(ActivePath1 + "ArrivalPrice_478.csv",index_col=0)
    terminalPrice1 = pd.read_csv(ActivePath1 + "terminalPrice_478.csv",index_col=0)
    VWAP_3301 = pd.read_csv(ActivePath1 + "VWAP_330PM_478.csv",index_col=0)
    sigma1 = pd.read_csv(ActivePath1 + "SigmaMatrix_478.csv",index_col=0)
    imbalanceValue1 = pd.read_csv(ActivePath1 + "imbalance_478.csv",index_col=0)
    avgDailyValue1 = pd.read_csv(ActivePath1 + "dailyAverage_478.csv",index_col=0)
    RP1 = nonlinearRegressionProcessor(arrivalPrice1,terminalPrice1,VWAP_3301,sigma1,imbalanceValue1,avgDailyValue1)

    print('\n=================================Active Stocks Analysis==============================\n')
    RP1.doNonlinearRegression()
    print('NLS standard error', RP1._stdError)
    print('NLS residuals', RP1._residuals)
    print("NLS Finished!")
    print('length of h, sigma, XV', len(RP1._h), len(RP1._sigma), len(RP1._X_V))
    wls1 = WLS(np.column_stack([RP1._sigma, RP1._X_V]), RP1._h)
    print(wls1.summary())
    print('\nWLS parameters', wls1.params)
    print('WLS residuals', wls1.resid)
    print('WLS t-values', wls1.tvalues)

    arrivalPrice2 = pd.read_csv(LessActivePath2 + "ArrivalPrice_734.csv", index_col=0)
    terminalPrice2 = pd.read_csv(LessActivePath2 + "terminalPrice_734.csv", index_col=0)
    VWAP_3302 = pd.read_csv(LessActivePath2 + "VWAP_330PM_734.csv", index_col=0)
    sigma2 = pd.read_csv(LessActivePath2 + "SigmaMatrix_734.csv", index_col=0)
    imbalanceValue2 = pd.read_csv(LessActivePath2 + "imbalance_734.csv", index_col=0)
    avgDailyValue2 = pd.read_csv(LessActivePath2 + "dailyAverage_734.csv", index_col=0)
    RP2 = nonlinearRegressionProcessor(arrivalPrice2, terminalPrice2, VWAP_3302, sigma2, imbalanceValue2,
                                       avgDailyValue2)

    print('\n=============================Less Active Stocks Analysis================================\n')
    RP2.doNonlinearRegression()
    print('NLS standard error', RP2._stdError)
    print('NLS residuals', RP2._residuals)
    print("NLS Finished!")
    print('length of h, sigma, XV', len(RP2._h), len(RP2._sigma), len(RP2._X_V))
    wls2 = WLS(np.column_stack([RP2._sigma, RP2._X_V]), RP2._h)
    print(wls2.summary())
    print('\nWLS parameters', wls2.params)
    print('WLS residuals', wls2.resid)
    print('WLS t-values', wls2.tvalues)

    arrivalPrice3 = pd.read_csv(TotalPath3 + "ArrivalPrice_1212.csv", index_col=0)
    terminalPrice3 = pd.read_csv(TotalPath3 + "terminalPrice_1212.csv", index_col=0)
    VWAP_3303 = pd.read_csv(TotalPath3 + "VWAP_330PM_1212.csv", index_col=0)
    sigma3 = pd.read_csv(TotalPath3 + "SigmaMatrix_1212.csv", index_col=0)
    imbalanceValue3 = pd.read_csv(TotalPath3 + "imbalance_1212.csv", index_col=0)
    avgDailyValue3 = pd.read_csv(TotalPath3 + "dailyAverage_1212.csv", index_col=0)
    RP3 = nonlinearRegressionProcessor(arrivalPrice3, terminalPrice3, VWAP_3303, sigma3, imbalanceValue3,
                                       avgDailyValue3)

    print('\n===============================Total Stocks Analysis===============================\n')
    eta, beta = RP3.doNonlinearRegression()
    print('NLS standard error', RP3._stdError)
    print('NLS residuals', RP3._residuals)
    print("NLS Finished!")
    print('length of h, sigma, XV', len(RP3._h), len(RP3._sigma), len(RP3._X_V))
    wls3 = WLS(np.column_stack([RP3._sigma, RP3._X_V]), RP3._h)
    print(wls3.summary())
    print('\nWLS parameters', wls3.params)
    print('WLS residuals', wls3.resid)
    print('WLS t-values', wls3.tvalues)

    print('Residuals stats from NLS std error:', st.describe(RP3._residuals))
    print('Residuals stats from WLS std error:', st.describe(wls3.resid))
    wls3.testAssumption()
    plt.hist(RP3._residuals, bins=100, range=(-2.,2.))
    plt.savefig('NLS_residuals.png')
    plt.close()
    y_hat_NLS = func((RP3._sigma, RP3._X_V), eta, beta)
    plt.scatter(y_hat_NLS, RP3._residuals)
    plt.savefig('NLS_resid_scatter.png')
    plt.close()
    plt.hist(wls3.resid, bins=100, range=(-2.,2.))
    plt.savefig('WLS_residuals.png')
    plt.close()
    plt.scatter(wls3.fittedvalues, wls3.resid)
    plt.savefig('WLS_resid_scatter.png')
    plt.close()
