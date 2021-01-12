import numpy as np



stats_clean = np.load('stats_clean.npy', allow_pickle=True).item()
stats_adjust = np.load( 'stats_adjust.npy', allow_pickle=True).item()


print('----------------Output statistics for X = 10s, using cleaned GILD data--------------')
print('Annualized mean returns for mid-quotes and trades:', stats_clean['10s']['meanreturn'])
print('Annualized median returns for mid-quotes and trades:', stats_clean['10s']['medianreturn'])
print('Annualized standard deviation of returns for mid-quotes and trades:', stats_clean['10s']['std'])
print('Annualized median absolute deviation for mid-quotes and trades:', stats_clean['10s']['MAD'])
print('Skew of returns for mid-quotes and trades:', stats_clean['10s']['skew'])
print('Kurtosis for mid-quotes and trades:', stats_clean['10s']['kurt'])
print('10 largest returns for mid-quotes and trades:', stats_clean['10s']['maxreturns'])
print('10 smallest returns for mid-quotes and trades:', stats_clean['10s']['minreturns'])
print('Maximum drawdown of mid-quotes and trades:',  stats_clean['10s']['maxdrawdown'])

print('\n----------------Output statistics for X = 30s, using cleaned GILD data--------------')
print('Annualized mean returns for mid-quotes and trades:', stats_clean['30s']['meanreturn'])
print('Annualized median returns for mid-quotes and trades:', stats_clean['30s']['medianreturn'])
print('Annualized standard deviation of returns for mid-quotes and trades:', stats_clean['30s']['std'])
print('Annualized median absolute deviation for mid-quotes and trades:', stats_clean['30s']['MAD'])
print('Skew of returns for mid-quotes and trades:', stats_clean['30s']['skew'])
print('Kurtosis for mid-quotes and trades:', stats_clean['30s']['kurt'])
print('10 largest returns for mid-quotes and trades:', stats_clean['30s']['maxreturns'])
print('10 smallest returns for mid-quotes and trades:', stats_clean['30s']['minreturns'])
print('Maximum drawdown of mid-quotes and trades:',  stats_clean['30s']['maxdrawdown'])

print('\n----------------Output statistics for X = 1-minute, using cleaned GILD data--------------')
print('Annualized mean returns for mid-quotes and trades:', stats_clean['1m']['meanreturn'])
print('Annualized median returns for mid-quotes and trades:', stats_clean['1m']['medianreturn'])
print('Annualized standard deviation of returns for mid-quotes and trades:', stats_clean['1m']['std'])
print('Annualized median absolute deviation for mid-quotes and trades:', stats_clean['1m']['MAD'])
print('Skew of returns for mid-quotes and trades:', stats_clean['1m']['skew'])
print('Kurtosis for mid-quotes and trades:', stats_clean['1m']['kurt'])
print('10 largest returns for mid-quotes and trades:', stats_clean['1m']['maxreturns'])
print('10 smallest returns for mid-quotes and trades:', stats_clean['1m']['minreturns'])
print('Maximum drawdown of mid-quotes and trades:',  stats_clean['1m']['maxdrawdown'])

print('\n----------------Output statistics for X = 5-minute, using cleaned GILD data--------------')
print('Annualized mean returns for mid-quotes and trades:', stats_clean['5m']['meanreturn'])
print('Annualized median returns for mid-quotes and trades:', stats_clean['5m']['medianreturn'])
print('Annualized standard deviation of returns for mid-quotes and trades:', stats_clean['5m']['std'])
print('Annualized median absolute deviation for mid-quotes and trades:', stats_clean['5m']['MAD'])
print('Skew of returns for mid-quotes and trades:', stats_clean['5m']['skew'])
print('Kurtosis for mid-quotes and trades:', stats_clean['5m']['kurt'])
print('10 largest returns for mid-quotes and trades:', stats_clean['5m']['maxreturns'])
print('10 smallest returns for mid-quotes and trades:', stats_clean['5m']['minreturns'])
print('Maximum drawdown of mid-quotes and trades:',  stats_clean['5m']['maxdrawdown'])

print('\n----------------Output statistics for X = 10-minute, using cleaned GILD data--------------')
print('Annualized mean returns for mid-quotes and trades:', stats_clean['10m']['meanreturn'])
print('Annualized median returns for mid-quotes and trades:', stats_clean['10m']['medianreturn'])
print('Annualized standard deviation of returns for mid-quotes and trades:', stats_clean['10m']['std'])
print('Annualized median absolute deviation for mid-quotes and trades:', stats_clean['10m']['MAD'])
print('Skew of returns for mid-quotes and trades:', stats_clean['10m']['skew'])
print('Kurtosis for mid-quotes and trades:', stats_clean['10m']['kurt'])
print('10 largest returns for mid-quotes and trades:', stats_clean['10m']['maxreturns'])
print('10 smallest returns for mid-quotes and trades:', stats_clean['10m']['minreturns'])
print('Maximum drawdown of mid-quotes and trades:',  stats_clean['10m']['maxdrawdown'])

print('\n----------------Output statistics for X = 30-minute, using cleaned GILD data--------------')
print('Annualized mean returns for mid-quotes and trades:', stats_clean['30m']['meanreturn'])
print('Annualized median returns for mid-quotes and trades:', stats_clean['30m']['medianreturn'])
print('Annualized standard deviation of returns for mid-quotes and trades:', stats_clean['30m']['std'])
print('Annualized median absolute deviation for mid-quotes and trades:', stats_clean['30m']['MAD'])
print('Skew of returns for mid-quotes and trades:', stats_clean['30m']['skew'])
print('Kurtosis for mid-quotes and trades:', stats_clean['30m']['kurt'])
print('10 largest returns for mid-quotes and trades:', stats_clean['30m']['maxreturns'])
print('10 smallest returns for mid-quotes and trades:', stats_clean['30m']['minreturns'])
print('Maximum drawdown of mid-quotes and trades:',  stats_clean['30m']['maxdrawdown'])