import yfinance as yf
import pandas as np
import numpy as np
import math

premium = 0
dte = 0
delta = 0
gamma = 0
theta = 0
vega = 0
rho = 0
implied_volatility = 0
intrinsic_value = 0

def erf(x):
    A1 = 0.254829592
    A2 = -0.284496736
    A3 = 1.421413741
    A4 = -1.453152027
    A5 = 1.061405429
    P = 0.3275911

    sign = 1 if x >= 0 else -1
    x = abs(x)

    t = 1.0 / (1.0 + P * x)
    y = 1.0 - (((((A5 * t + A4) * t) + A3) * t + A2) * t + A1) * t * math.exp(-x * x)

    return sign*y

def CSN(value):
    return 0.5 * (1.0 + erf(value / math.sqrt(2.0)))

def d1(S_0, strike, risk_free_rate, volatility, time_to_maturity):
    d_1 = (math.log(S_0/strike) + (risk_free_rate + (volatility*volatility / 2)) * time_to_maturity)/(volatility * math.sqrt(time_to_maturity))
    return d_1

def d2(S_0, strike, risk_free_rate, volatility, time_to_maturity):
    d_2 = ((math.log(S_0/strike) + (risk_free_rate + (volatility*volatility / 2)) * time_to_maturity)/(volatility * math.sqrt(time_to_maturity))) - (volatility * math.sqrt(time_to_maturity))
    return d_2

def BlackScholesPricingModel(S, X, risk_free, vol, time, isCallOption):
    dte = time*365.2425

    if(isCallOption):
        d_1 = d1(S, X, risk_free, vol, time)
        d_2 = d2(S, X, risk_free, vol, time)

        premium = (S*CSN(d_1)) - (X*math.exp(-risk_free*time)*CSN(d_2))
        delta = CSN(d_1)
        gamma = CSN(d_1) / (S*vol*math.sqrt(time))
        theta = (-(S*CSN(d_1)*vol)/(2*math.sqrt(time))) - (risk_free*X*math.exp(-risk_free*time)*CSN(d_2))
        vega = S*CSN(d_1)*math.sqrt(time)
        rho = X*time*math.exp(-risk_free*time)*CSN(d_2)
        implied_volatility = vol - ((premium-(premium-0.01))/(vega))
        intrinsic_value = max(S-X, 0.0)
    else:
        d_1 = d1(S, X, risk_free, vol, time)
        d_2 = d2(S, X, risk_free, vol, time)
        premium = (X*math.exp(-risk_free*time)*CSN(-d_2)) - (S*CSN(-d_1))
        delta = CSN(d_1)-1
        gamma = CSN(d_1) / (S*vol*math.sqrt(time))
        theta = (-(S*CSN(d_1)*vol)/(2*math.sqrt(time))) - (risk_free*X*math.exp(-risk_free*time)*CSN(-d_2))
        vega = S*CSN(d_1)*math.sqrt(time)
        rho = -(X*time*math.exp(-risk_free*time)*CSN(-d_2))
        implied_volatility = vol - ((premium-0.01)-premium)/(vega)
        intrinsic_value = max(X-S, 0.0)

    return premium, dte, delta, gamma, theta, vega, rho, implied_volatility, intrinsic_value

#inputs
S0 = 100.0
K = 75.0
T = 1.0
r = 0.05
sigma = 0.2
isCallOption = True

count = 0

for i in range(21):
    if(S0<500):
        print("(Option Price, Time, DELTA, GAMMA, THETA, VEGA, RHO, IMPLIED VOLATILITY, INTRINSIC VALUE), Strike Price")
        print(BlackScholesPricingModel(S0, K, r, sigma, T, isCallOption), K)
        K += 2.5
    elif(S0<1000):
        print("(Option Price, Time, DELTA, GAMMA, THETA, VEGA, RHO, IMPLIED VOLATILITY, INTRINSIC VALUE), Strike Price")
        print(BlackScholesPricingModel(S0, K, r, sigma, T, isCallOption), K)
        K += 5
    elif(S0<2000):
        print("(Option Price, Time, DELTA, GAMMA, THETA, VEGA, RHO, IMPLIED VOLATILITY, INTRINSIC VALUE), Strike Price")
        print(BlackScholesPricingModel(S0, K, r, sigma, T, isCallOption), K)
        K += 10
    elif(S0<4000):
        print("(Option Price, Time, DELTA, GAMMA, THETA, VEGA, RHO, IMPLIED VOLATILITY, INTRINSIC VALUE), Strike Price")
        print(BlackScholesPricingModel(S0, K, r, sigma, T, isCallOption), K)
        K += 25
    else:
        print("(Option Price, Time, DELTA, GAMMA, THETA, VEGA, RHO, IMPLIED VOLATILITY, INTRINSIC VALUE), Strike Price")
        print(BlackScholesPricingModel(S0, K, r, sigma, T, isCallOption), K)
        K += 50
