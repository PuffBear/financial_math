import scipy.optimize as sco
import numpy as np

def portfolio_variance(weight_1, variance_1, weight_2, variance_2, cov_12):
    port_var = ((weight_1)**2 * variance_1) + ((weight_2)**2 * variance_2) + 2*(weight_1*weight_2)*cov_12
    return port_var

