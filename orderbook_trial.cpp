/*
OrderBook Matching without TimeStamp; Order of matching will be type rather than time.
*/
#include<iostream>
#include<iomanip>
#include<algorithm>
#include<vector>
#include<string>

class OrderBook{
public:
    enum class OrderType{Buy_Order, Sell_Order};

    class Order{
    public:
        Order(double Price, double Amount);

    private:
    };

private:

};