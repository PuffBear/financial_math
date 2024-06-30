import numpy as np
from scipy.optimize import minimize_scalar

# Define the returns and covariance matrix of two assets
mean_returns = np.array([0.1, 0.2])  # Mean returns of the two assets
cov_matrix = np.array([[0.005, -0.010], [-0.010, 0.040]])  # Covariance matrix

# Define the portfolio variance function
def portfolio_variance(w1):
    w2 = 1 - w1
    weights = np.array([w1, w2])
    return weights.T @ cov_matrix @ weights

# Perform Brent's line search to minimize the portfolio variance
result = minimize_scalar(portfolio_variance, bounds=(0, 1), method='Brent')

# Optimal weight for the first asset
optimal_w1 = result.x
optimal_w2 = 1 - optimal_w1

# Optimal portfolio variance
optimal_variance = result.fun

# Print the results
print(f"Optimal weight for asset 1: {optimal_w1:.4f}")
print(f"Optimal weight for asset 2: {optimal_w2:.4f}")
print(f"Optimal portfolio variance: {optimal_variance:.6f}")
