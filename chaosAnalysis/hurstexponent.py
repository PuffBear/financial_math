'''
rolling windows to hurst exponents
hurst exponents can detect fractal trends, inherent in chaos dynamics
The chaos analysis framework:

1. PreReqs and Standard Tests:
noise reduction(wavelet-filter)
stationarity(ADF-,KPSS-test)
distribution(KS-test)
non-linearity(BDS-test)
correlation structure(ACFs)
sample entropy
detrended fluctional analysis
significance tests(bootstrap)

2. Recurrence Quantificaiton Analysis
recurrence plots(with binary colours)
recurrence quantificaiton measures

3. Multi-Resolution Analysis
rolling window averages
wavelet power spectrum of underlying time series
discrete wavelet transform (DWT)

4. Distribution and Power Laws
multifractal detrended fluctuation analysis
disturbance coherence tests

Dataset(SNP 500 return series): orig log returns and log returns with wavelet filtered
Variant1: apply bootstraping algorithm, calculate for each iteration, apply hurst exponent, 
Variant2:divide into three rolling windows (H100, H1000, H2500) and apply each window as data basis


implication: market efficiency hypothesis is dead.

link: https://www.youtube.com/watch?v=pmE2lO5rzYw
'''

# CHAOS ANALYSIS IN FINANCIAL MARKETS

