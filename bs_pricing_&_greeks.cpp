#include<iostream>
#include<cmath>

struct Contract
{
    double premium;
    int dte;
    double delta;
    double gamma;
    double theta;
    double vega;
    double rho;
    double implied_volatility;
    double intrinsic_value;
};

// Error function approximation
double erf(double x) {
    const double A1 = 0.254829592;
    const double A2 = -0.284496736;
    const double A3 = 1.421413741;
    const double A4 = -1.453152027;
    const double A5 = 1.061405429;
    const double P = 0.3275911;

    // Save the sign of x
    int sign = (x >= 0) ? 1 : -1;
    x = fabs(x);

    // A&S formula 7.1.26
    double t = 1.0 / (1.0 + P * x);
    double y = 1.0 - (((((A5 * t + A4) * t) + A3) * t + A2) * t + A1) * t * exp(-x * x);

    return sign * y;
}

double CSN(double value) {
    return 0.5 * (1.0 + erf(value / sqrt(2.0)));
}

double d1(double S_0, double strike, double risk_free_rate, double volatility, double time_to_maturity){
    double d_1 = (std::log(S_0/strike) + (risk_free_rate + (volatility*volatility / 2)) * time_to_maturity)/(volatility * std::sqrt(time_to_maturity));
    return d_1;
}

double d2(double S_0, double strike, double risk_free_rate, double volatility, double time_to_maturity){
    double d_2 = ((std::log(S_0/strike) + (risk_free_rate + (volatility*volatility / 2)) * time_to_maturity)/(volatility * std::sqrt(time_to_maturity))) - (volatility * std::sqrt(time_to_maturity));
    return d_2;
}

Contract BlackScholesPricingModel(double S, double X, double risk_free, double vol, double time, bool isCallOption){
    Contract con;
    int days_till_expiry = time*365.2425;
    con.dte = days_till_expiry;

    if(isCallOption)
    {
        double d_1 = d1(S, X, risk_free, vol, time);
        double d_2 = d2(S, X, risk_free, vol, time);

        con.premium = (S*CSN(d_1)) - (X*std::exp(-risk_free*time)*CSN(d_2));
        con.delta = CSN(d_1);
        con.gamma = CSN(d_1) / (S*vol*std::sqrt(time));
        con.theta = (-(S*CSN(d_1)*vol)/(2*std::sqrt(time))) - (risk_free*X*std::exp(-risk_free*time)*CSN(d_2));
        con.vega = S*CSN(d_1)*std::sqrt(time);
        con.rho = X*time*std::exp(-risk_free*time)*CSN(d_2);
        con.implied_volatility = vol - ((con.premium-(con.premium-0.01))/(con.vega));
        con.intrinsic_value = std::max(S-X, 0.0);
    }

    else
    {
        double d_1 = d1(S, X, risk_free, vol, time);
        double d_2 = d2(S, X, risk_free, vol, time);
        con.premium = (X*std::exp(-risk_free*time)*CSN(-d_2)) - (S*CSN(-d_1));
        con.delta = CSN(d_1)-1;
        con.gamma = CSN(d_1) / (S*vol*std::sqrt(time));
        con.theta = (-(S*CSN(d_1)*vol)/(2*std::sqrt(time))) - (risk_free*X*std::exp(-risk_free*time)*CSN(-d_2));
        con.vega = S*CSN(d_1)*std::sqrt(time);
        con.rho = -(X*time*std::exp(-risk_free*time)*CSN(-d_2));
        con.implied_volatility = vol - ((con.premium-0.01)-con.premium)/(con.vega);
        con.intrinsic_value = std::max(X-S, 0.0);
    }

    return con;
}

int main(){
    double S0 = 100.0;
    double K = 100.0;
    double T = 1.0;
    double r = 0.05;
    double sigma = 0.2;

    //Calculate Option Prices
    auto callContract = BlackScholesPricingModel(S0, K, r, sigma, T, true);
    auto putContract = BlackScholesPricingModel(S0, K, r, sigma, T, false);

    std::cout << "European Call Option Price: " << callContract.premium << ", dte: " << callContract.dte << ", delta: " << callContract.delta << ", gamma: " << callContract.gamma << ", theta: " << callContract.theta << ", vega: " << callContract.vega  << ", rho: " << callContract.rho << ", implied volatility: " << callContract.implied_volatility  << ", intrinsic value: " << callContract.intrinsic_value << std::endl;
    std::cout << "European Put Option Price: " << putContract.premium << ", dte: " << putContract.dte << ", delta: " << putContract.delta << ", gamma: " << putContract.gamma << ", theta: " << putContract.theta << ", vega: " << putContract.vega << ", rho: " << putContract.rho << ", implied volatility: " << putContract.implied_volatility  << ", intrinsic value: " << putContract.intrinsic_value << std::endl;

    return EXIT_SUCCESS;
}