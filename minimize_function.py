import scipy.optimize as sco

# Define the function to be minimized
def func(x):
    return (x - 4)**2 + 1

# Use minimize_scalar to find the minimum
result = sco.minimize_scalar(func)

# Print the result
print("Optimal value of x:", result.x)
print("Function value at the optimal x:", result.fun)
