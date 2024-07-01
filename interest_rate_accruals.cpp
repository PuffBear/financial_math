#include <iostream>
#include <cmath>

double simple_yield(double LTP_t, double t, double T){
    double r_a = (1-LTP_t)/(LTP_t*(T-t));
    return r_a;
}

double effective_yield(double LTP_t, double t, double T){
    double y_e = 1/pow(LTP_t, (1/(T-t))) - 1;
    return y_e;
}

double continuous_yield(double LTP_t, double t, double T){
    double y = - log(LTP_t)/(T-t);
    return y;
}

int main(){
    double LTP = 0.9;
    double maturity_one = 2;
    double maturity_two = 3;
    double maturity_three = 4;

    double simple_interest_rate = simple_yield(LTP, 0, maturity_one);
    double effective_interest_rate = effective_yield(LTP, 0, maturity_two);
    double continuously_compunded_interest_rate = continuous_yield(LTP, 0, maturity_three);

    std::cout << "The Simple Interest Rate on a Zero Coupon with 2 year maturity, in the start is: "<< simple_interest_rate*100<<std::endl;
    std::cout << "The Effective Interest Rate on a Zero Coupon with 3 year maturity, in the start is: "<< effective_interest_rate*100<<std::endl;
    std::cout << "The Continuous Interest Rate on a Zero Coupon with 4 year maturity, in the start is: "<< continuously_compunded_interest_rate*100<<std::endl;

    return EXIT_SUCCESS;
}