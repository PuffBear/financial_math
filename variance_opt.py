'''
A relatively small program that works on optimizing the portfolio variance for a two asset portfolio.

The objective is to get the portfolio variance minimum when having two stocks in the same portfolio and
then allocating funds depending on such achieved minimu portfolio variance.
'''

import scipy.optimize as sco
import numpy as np
import yfinance as yf

# Function to calculate portfolio variance
def portfolio_variance(weight_1, variance1, weight_2, variance2, cov_12):
    port_var = ((weight_1)**2 * variance1) + ((weight_2)**2 * variance2) + 2*(weight_1*weight_2)*cov_12
    return port_var

# Function to calculate variance
def variance(returns):
    mean_return = np.mean(returns)
    squared_deviations = [(r - mean_return) ** 2 for r in returns]
    sum_squared_deviations = np.sum(squared_deviations)
    variance = sum_squared_deviations / (len(returns) - 1)
    return variance

# Function to calculate covariance
def covariance(returns1, returns2):
    mean_return1 = np.mean(returns1)
    mean_return2 = np.mean(returns2)
    deviations1 = returns1 - mean_return1
    deviations2 = returns2 - mean_return2
    products_of_deviations = deviations1 * deviations2
    sum_products_of_deviations = np.sum(products_of_deviations)
    covariance = sum_products_of_deviations / (len(returns1) - 1)
    return covariance

# Download data
data_1 = yf.download('PATELENG.NS', start="2021-11-01", end="2024-06-30")
data_1 = data_1.drop(["High", "Low", "Open", "Adj Close", "Volume"], axis=1)
data_1 = data_1.dropna()
returns_1 = data_1['Close'].pct_change().dropna()
variance_1 = variance(returns_1)

data_2 = yf.download('CAPACITE.NS', start="2021-11-01", end="2024-06-30")
data_2 = data_2.drop(["High", "Low", "Open", "Adj Close", "Volume"], axis=1)
data_2 = data_2.dropna()
returns_2 = data_2['Close'].pct_change().dropna()
variance_2 = variance(returns_2)

covariance_assets = covariance(returns_1, returns_2)

# Objective function to minimize
def objective_function(w1, variance1, variance2, cov_12):
    w2 = 1 - w1
    return portfolio_variance(w1, variance1, w2, variance2, cov_12)

# Optimize the portfolio variance using Brent's method
result = sco.minimize_scalar(objective_function, bounds=(0, 1), args=(variance_1, variance_2, covariance_assets), method='bounded')

# Optimal weight for asset 1
optimal_w1 = result.x
# Optimal weight for asset 2
optimal_w2 = 1 - optimal_w1

print(f"Optimal weight for asset 1: {optimal_w1}")
print(f"Optimal weight for asset 2: {optimal_w2}")
print(f"Minimum portfolio variance: {result.fun}")
