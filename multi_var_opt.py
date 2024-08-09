'''
A relatively small program that works on optimizing the portfolio variance for a two asset portfolio
from among hundreds of stock totalling a few thounsand pairings. 

The objective is to get the portfolio variance minimum when having two stocks in the same portfolio and
then allocating funds depending on such achieved minimu portfolio variance.
'''

import yfinance as yf
import numpy as np
import scipy.optimize as sco
from itertools import combinations

def portfolio_variance(weight_1, variance1, weight_2, variance2, cov_12):
    port_var = ((weight_1)**2 * variance1) + ((weight_2)**2 * variance2) + 2*(weight_1*weight_2)*cov_12
    return port_var

def variance(returns):
    mean_return = np.mean(returns)
    squared_deviations = [(r - mean_return) ** 2 for r in returns]
    sum_squared_deviations = np.sum(squared_deviations)
    variance = sum_squared_deviations / (len(returns) - 1)
    return variance

def covariance(returns1, returns2):
    mean_return1 = np.mean(returns1)
    mean_return2 = np.mean(returns2)
    deviations1 = returns1 - mean_return1
    deviations2 = returns2 - mean_return2
    products_of_deviations = deviations1 * deviations2
    sum_products_of_deviations = np.sum(products_of_deviations)
    covariance = sum_products_of_deviations / (len(returns1) - 1)
    return covariance

def download_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data['Close'].dropna()
    returns = data.pct_change().dropna()
    return returns

tickers = ['FINPIPE.NS', 'PRINCEPIPE.NS', 'MAXHEALTH.NS', 'BOSCHLTD.NS', 'EICHERMOT.NS', 'INDUSINDBNK.NS', 'LICHSGFIN.NS', 'SHREECEM.NS', 'MAHSEAMLES.NS', 'TITAGARH.NS', 'BEML.NS', 'ICICIBANK.NS', 'SBIN.NS', 'NESTLEIND.NS', 'RELIANCE.NS']

start_date = "2021-11-01"
end_date = "2024-08-09"

returns_data = {}
for ticker in tickers:
    returns_data[ticker] = download_data(ticker, start_date, end_date)

results = []
for (ticker1, ticker2) in combinations(tickers, 2):
    returns1 = returns_data[ticker1]
    returns2 = returns_data[ticker2]

    variance1 = variance(returns1)
    variance2 = variance(returns2)
    cov_12 = covariance(returns1, returns2)

    def objective_function(w1):
        w2 = 1 - w1
        return portfolio_variance(w1, variance1, w2, variance2, cov_12)

    result = sco.minimize_scalar(objective_function, bounds=(0, 1), method='bounded')
    
    optimal_w1 = result.x
    optimal_w2 = 1 - optimal_w1
    min_variance = result.fun

    results.append({
        'Ticker 1': ticker1,
        'Ticker 2': ticker2,
        'Optimal Weight 1': optimal_w1*100,
        'Optimal Weight 2': optimal_w2*100,
        'Minimum Variance': min_variance*100
    })

import pandas as pd
df_results = pd.DataFrame(results)
print(df_results)

sorted_df = df_results.sort_values(by='Minimum Variance')
pd.set_option('display.max_rows', None)
print(sorted_df)