import numpy as np
import pandas as pd
from Processor.readSP500 import readSP500
pd.options.mode.chained_assignment = None
"""
This code is for mean variance optimization on S&P500 stocks 
"""
# Load SP500 data
sp500 = readSP500("s_p500.xlsx")
tickerList = sp500.get_tickers()
print(tickerList)
sp500_df = sp500.get_sp500()
print(sp500_df.columns)

# calculate portfolio holdings on June 20, 2007
df0620 = sp500_df[sp500_df['Names Date']=='20070620']
adj_shares0620 = np.array(df0620['Shares Outstanding']) * np.array(df0620['Cumulative Factor to Adjust Shares/Vol'])
adj_price0620 = np.array(df0620['Price or Bid/Ask Average']) / np.array(df0620['Cumulative Factor to Adjust Prices'])
df0620['weights0620'] = adj_price0620 * adj_shares0620 / sum(adj_price0620 * adj_shares0620)
df0620 = df0620.sort_values(by=['weights0620'], ascending=False)
print(df0620.head())

# calculate portfolio holdings on September 20, 2007
df0920 = sp500_df[sp500_df['Names Date']=='20070920']
adj_shares0920 = np.array(df0920['Shares Outstanding']) * np.array(df0920['Cumulative Factor to Adjust Shares/Vol'])
adj_price0920 = np.array(df0920['Price or Bid/Ask Average']) / np.array(df0920['Cumulative Factor to Adjust Prices'])
df0920['weights0920'] = adj_price0920 * adj_shares0920 / sum(adj_price0920 * adj_shares0920)
df0920 = df0920.sort_values(by=['weights0920'], ascending=False)
print(df0920.head())