'''
A relatively small program that works on optimizing the portfolio variance for a two asset portfolio
from among hundreds of stock totalling a few thounsand pairings. 

The objective is to get the portfolio variance minimum when having two stocks in the same portfolio and
then allocating funds depending on such achieved minimu portfolio variance.
'''

import yfinance as yf
import numpy as np
import pandas as pd
import scipy.optimize as sco
from scipy.optimize import minimize
from itertools import combinations
import matplotlib.pyplot as plt

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

tickers = ['ANURAS.NS', 'MHRIL.NS', 'APTUS.NS', 'VARROC.NS', 'BEML.NS', 'GMMPFAUDLR.NS', 'BIRLACORPN.NS', 'MEDANTA.NS', 'IIFL.NS', 'JMFINANCIL.NS', 'VIPIND.NS']

start_date = "2021-11-01"
end_date = "2024-08-13"

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

filtered_df = sorted_df[(sorted_df['Optimal Weight 1'] >= 10.00) & (sorted_df['Optimal Weight 2'] >= 10.00)]

pairings_df = filtered_df
# Function to identify unique stock pairings
def get_unique_pairings(pairings_df):
    unique_combinations = []
    for i, row_i in pairings_df.iterrows():
        tickers_i = set([row_i['Ticker 1'], row_i['Ticker 2']])
        for j, row_j in pairings_df.iterrows():
            if i >= j: 
                continue
            tickers_j = set([row_j['Ticker 1'], row_j['Ticker 2']])
            if tickers_i.isdisjoint(tickers_j):
                unique_combinations.append((i, j))
    return unique_combinations

# Calculate the combined portfolio weights and minimum variance for unique pairings
def calculate_combined_variance(pairings_df, unique_combinations):
    results = []
    for (i, j) in unique_combinations:
        combined_weights = np.array([pairings_df.loc[i, 'Optimal Weight 1'], pairings_df.loc[i, 'Optimal Weight 2'],
                                     pairings_df.loc[j, 'Optimal Weight 1'], pairings_df.loc[j, 'Optimal Weight 2']])
        # Assuming equal weights for simplicity; you may want to optimize this further
        combined_weights /= combined_weights.sum()
        
        combined_variance = (pairings_df.loc[i, 'Minimum Variance'] + pairings_df.loc[j, 'Minimum Variance']) / 2
        results.append({
            'Pair 1': (pairings_df.loc[i, 'Ticker 1'], pairings_df.loc[i, 'Ticker 2']),
            'Pair 2': (pairings_df.loc[j, 'Ticker 1'], pairings_df.loc[j, 'Ticker 2']),
            'Combined Weights': combined_weights,
            'Combined Variance': combined_variance
        })
    return pd.DataFrame(results)

# Identify unique pairings
unique_combinations = get_unique_pairings(pairings_df)

# Calculate and rank combined variances
final_portfolios = calculate_combined_variance(pairings_df, unique_combinations)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# Rank by combined variance
final_ranked_portfolios = final_portfolios.sort_values(by='Combined Variance')
top_rows = final_ranked_portfolios.head(25)
#print(top_rows)
import itertools
def create_8_stock_portfolios(final_ranked_portfolios):
    unique_combinations = []
    for idx1, idx2 in itertools.combinations(final_ranked_portfolios.index, 2):
        stocks1 = set(final_ranked_portfolios.loc[idx1, 'Pair 1']).union(set(final_ranked_portfolios.loc[idx1, 'Pair 2']))
        stocks2 = set(final_ranked_portfolios.loc[idx2, 'Pair 1']).union(set(final_ranked_portfolios.loc[idx2, 'Pair 2']))

        combined_stocks = stocks1.union(stocks2)
        if len(combined_stocks) == 8:
            weights1 = final_ranked_portfolios.loc[idx1, 'Combined Weights']
            weights2 = final_ranked_portfolios.loc[idx2, 'Combined Weights']
            
            # Create a combined weights dictionary
            weight_dict = dict(zip(stocks1, weights1))
            weight_dict.update(dict(zip(stocks2, weights2)))
            
            # Normalize weights to sum up to 1
            total_weight = sum(weight_dict.values())
            combined_weights = [weight_dict[stock] / total_weight for stock in combined_stocks]
            
            combined_variance = (final_ranked_portfolios.loc[idx1, 'Combined Variance'] + final_ranked_portfolios.loc[idx2, 'Combined Variance']) / 2
            unique_combinations.append({
                'Pair 1': final_ranked_portfolios.loc[idx1, 'Pair 1'],
                'Pair 2': final_ranked_portfolios.loc[idx1, 'Pair 2'],
                'Pair 3': final_ranked_portfolios.loc[idx2, 'Pair 1'],
                'Pair 4': final_ranked_portfolios.loc[idx2, 'Pair 2'],
                'Combined Weights': combined_weights,
                'Combined Variance': combined_variance
            })

    return pd.DataFrame(unique_combinations)

# Get the 8-stock portfolios
final_results = create_8_stock_portfolios(final_ranked_portfolios)

# Sort the final results by Combined Variance
final_results_sorted = final_results.sort_values(by='Combined Variance')

# Display the top 10 8-stock portfolios
print(final_results_sorted.head(10))

def join_tuple_string(data):
    if isinstance(data, tuple):
        return ', '.join(str(item) for item in data)
    else:
        return str(data)

# Apply this function if combining tuples into a single label is required
for column in final_results_sorted.columns:
    final_results_sorted[column] = final_results_sorted[column].apply(join_tuple_string)

# Initial extraction of labels may include combined stocks
combined_labels = final_results_sorted.iloc[0, :-2].tolist()  # Assuming the last two entries are not labels

# Split combined stock labels into individual stocks
labels = []
for label in combined_labels:
    # Split each combined label by ', ' and extend to the labels list
    labels.extend(label.split(', '))

comb_var = final_results_sorted.iloc[0, -1]
sizes_str = final_results_sorted.iloc[0, -2]  # Correctly point to the sizes list if -2 is the right index
print("Sizes string before parsing:", sizes_str)

import ast
try:
    sizes = ast.literal_eval(sizes_str)
    print("Parsed Sizes:", sizes)
except ValueError as e:
    print(f"Error parsing sizes: {e}")
    sizes = []

print("Labels for plotting:", labels)
print("Sizes for plotting:", sizes)

if len(labels) == len(sizes):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Ensures that pie is drawn as a circle
    plt.title('Distribution of Individual Stock Contributions')
else:
    print(f"Mismatch between labels and sizes: {len(labels)} labels, {len(sizes)} sizes")


import streamlit as st 
st.title("Risk Management using optimisation.")
st.dataframe(final_results_sorted)

st.title("Portfolio Allocation")
st.write("Variance of this allocation: ", comb_var)
# Display the pie chart using Streamlit
st.pyplot(fig)