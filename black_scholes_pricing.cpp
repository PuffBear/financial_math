#include<cmath>
#include<iostream>
#include<algorithm>

double norm_dist(double value){
    return 0.5 * std::erfc(-value * std::sqrt(0.5));
}

double d1(double S_0, double strike, double risk_free_rate, double volatility, double time_to_maturity){
    double d_1 = (std::log(S_0/strike) + (risk_free_rate + (volatility*volatility / 2)) * time_to_maturity)/(volatility * std::sqrt(time_to_maturity));
    return d_1;
}

double d2(double S_0, double strike, double risk_free_rate, double volatility, double time_to_maturity){
    double d_2 = ((std::log(S_0/strike) + (risk_free_rate + (volatility*volatility / 2)) * time_to_maturity)/(volatility * std::sqrt(time_to_maturity))) - (volatility * std::sqrt(time_to_maturity));
    return d_2;
}

double ComputeEuroCallPay(double S, double X, double risk_free, double vol, double time){
    double d1_value = d1(S, X, risk_free, vol, time);
    double d2_value = d2(S, X, risk_free, vol, time);
    double C = (S * norm_dist(d1_value) - X * std::exp(-risk_free * time) * norm_dist(d2_value));
    return C;
}

double ComputeEuroPutPay(double S, double X, double risk_free, double vol, double time){
    double d1_value = d1(S, X, risk_free, vol, time);
    double d2_value = d2(S, X, risk_free, vol, time);
    double P = (X * std::exp(-risk_free * time) - S * norm_dist(d1_value));
    return P;
}

int main(){
    double S = 100.0;
    double X = 100.0;
    double T = 1.0;
    double r = 0.05;
    double sigma = 0.2;

    double call_price = ComputeEuroCallPay(S, X, T, r, sigma);
    double put_price = ComputeEuroPutPay(S, X, T, r, sigma);

    std::cout << "European Call Option Price: " << call_price << std::endl;
    std::cout << "European Put Option Price: " << put_price << std::endl;

    return EXIT_SUCCESS;
}