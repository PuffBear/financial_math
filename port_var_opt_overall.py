import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
from multi_var_opt import sorted_df

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

import streamlit as st 
st.dataframe(final_results_sorted)