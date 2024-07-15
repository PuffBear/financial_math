import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Fetch historical stock data
ticker = "CYIENT.NS"
data = yf.download(ticker, start="2021-01-01", end="2023-01-01")
prices = data['Close']

# Calculate log returns
log_returns = np.log(prices / prices.shift(1)).dropna()

# Calculate mean and standard deviation of log returns
mean = log_returns.mean()
std_dev = log_returns.std()

# Simulation parameters
num_simulations = 10000
num_days = 252  # 1 year of trading days

# Simulate future stock prices
simulation_results = np.zeros((num_simulations, num_days))

for i in range(num_simulations):
    simulated_prices = [prices[-1]]
    for _ in range(num_days):
        simulated_price = simulated_prices[-1] * np.exp(mean + std_dev * np.random.normal())
        simulated_prices.append(simulated_price)
    simulation_results[i, :] = simulated_prices[1:]

# Plot the simulation results
plt.figure(figsize=(10, 6))
plt.plot(simulation_results.T, color='grey', alpha=0.1)
plt.title('Monte Carlo Simulation of Stock Prices')
plt.xlabel('Days')
plt.ylabel('Price')
plt.show()
