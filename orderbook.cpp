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
    enum class OrderType{Market, Limit, Stop, GoodTillCanceled, FillorKillLimit};
    enum class Side{Buy, Sell};

    class Order{
    public:
        Order(int id, OrderType type, Side side, double price, int quantity)
        : id(id), type(type), side(side), price(price), quantity(quantity) {}

        //getter methods for order attributes
        int getId() const { return id; }
        OrderType getOrder() const { return type; }
        Side getSide() const { return side; }
        double getPrice() const { return price; }
        int getQuantity() const { return quantity; }

        //Method to update Order Quantity
        void setQuantity(int new_quantity) { quantity = new_quantity; }

    private:
        int id;
        OrderType type;
        Side side;
        double price;
        int quantity;
    };

    //method to add an order to the OrderBook
    void addOrder(const Order& order){
        orders.push_back(order);
    }

    //method to cancel an order
    void cancelOrder(int orderId){
        auto it = std::remove_if(orders.begin(), orders.end(), [orderId](const Order& order){
            return order.getId() == orderId;
        }
        );

        if(it!=orders.end()){
            std::cout<<"Cancelled Order ID: " << orderId << std::endl;
            orders.erase(it, orders.end());
        }
    }

    //method to match the orders in the orderbook
    void MatchOrders(){
        //market orders handling
        for (auto it = orders.begin(); it != orders.end();) {
            if (it->getOrder() == OrderType::Market) {
                auto matchIt = findMatch(it, it->getQuantity());
                if (matchIt != orders.end()) {
                    executeOrder(it, matchIt);
                    it = orders.erase(it);
                } else {
                    ++it;
                }
            } else {
                ++it;
            }
        }

        //GTC orders handling
        for (auto it = orders.begin(); it != orders.end();) {
            if (it->getOrder() == OrderType::GoodTillCanceled) {
                auto matchIt = findMatch(it, it->getQuantity());
                if (matchIt != orders.end()) {
                    executeOrder(it, matchIt);
                    it = orders.erase(it);
                } else {
                    ++it;
                }
            } else {
                ++it;
            }
        }

        //FKLmt orders handling
        for (auto it = orders.begin(); it != orders.end();) {
            if (it->getOrder() == OrderType::FillorKillLimit) {
                auto matchIt = findMatch(it, it->getQuantity(), true); // Ensure full match
                if (matchIt != orders.end() && matchIt->getQuantity() >= it->getQuantity()) {
                    executeOrder(it, matchIt);
                    it = orders.erase(it);
                } else {
                    std::cout << "Canceled FOK Order ID: " << it->getId() << std::endl;
                    it = orders.erase(it);
                }
            } else {
                ++it;
            }
        }

        //Limit orders handling
        for (auto it = orders.begin(); it != orders.end();) {
            if (it->getOrder() == OrderType::Limit) {
                auto matchIt = findMatch(it, it->getQuantity());
                if (matchIt != orders.end()) {
                    executeOrder(it, matchIt);
                    it = orders.erase(it);
                } else {
                    ++it;
                }
            } else {
                ++it;
            }
        }
    }

    //method to print the orders in the orderBook
    void printOrders() const{
        for(const auto& order : orders) {
            printOrder(order);
        }
    }

private:
    std::vector<Order> orders;

    //helper method to match the orders
     std::vector<Order>::iterator findMatch(std::vector<Order>::iterator orderIt, int quantity, bool fullMatch = false) {
        for (auto it = orders.begin(); it != orders.end(); ++it) {
            if (it->getSide() != orderIt->getSide() &&
                ((orderIt->getSide() == Side::Buy && it->getPrice() <= orderIt->getPrice()) ||
                 (orderIt->getSide() == Side::Sell && it->getPrice() >= orderIt->getPrice())) &&
                (!fullMatch || it->getQuantity() >= quantity)) {
                return it;
            }
        }
        return orders.end();
    }

    //helper method to execute the orders
    void executeOrder(std::vector<Order>::iterator& orderIt, std::vector<Order>::iterator& matchIt) {
        double fillPrice = matchIt->getPrice();
        std::cout << "Matched Order ID: " << orderIt->getId() << " with Order ID: " << matchIt->getId() << " at Price: " << std::fixed << std::setprecision(2) << fillPrice << " quantity: " << orderIt->getQuantity() << std::endl;
        matchIt->setQuantity(matchIt->getQuantity() - orderIt->getQuantity());
        if (matchIt->getQuantity() == 0) {
            orders.erase(matchIt);
        }
    }

    void printOrder(const Order& order) const {
        std::cout << "Order ID: " << order.getId() 
                  << ", Type: " << static_cast<int>(order.getOrder()) 
                  << ", Side: " << (order.getSide() == Side::Buy ? "Buy" : "Sell")
                  << ", Price: " << order.getPrice() 
                  << ", Quantity: " << order.getQuantity() << std::endl;
    }
};

int main() {
    // Create an instance of OrderBook
    OrderBook orderBook;

    // Create sample orders of different types
    OrderBook::Order order1(1, OrderBook::OrderType::Market, OrderBook::Side::Buy, 0, 10);
    OrderBook::Order order2(2, OrderBook::OrderType::Limit, OrderBook::Side::Sell, 101.0, 20);
    OrderBook::Order order3(3, OrderBook::OrderType::Limit, OrderBook::Side::Sell, 99.0, 5);
    OrderBook::Order order4(4, OrderBook::OrderType::Market, OrderBook::Side::Sell, 0, 15);
    OrderBook::Order order5(5, OrderBook::OrderType::GoodTillCanceled, OrderBook::Side::Buy, 102.0, 10);
    OrderBook::Order order6(6, OrderBook::OrderType::FillorKillLimit, OrderBook::Side::Sell, 100.0, 8);
    OrderBook::Order order7(7, OrderBook::OrderType::FillorKillLimit, OrderBook::Side::Buy, 99.0, 12);
    OrderBook::Order order8(8, OrderBook::OrderType::FillorKillLimit, OrderBook::Side::Buy, 101.0, 8);

    // Add orders to the order book
    orderBook.addOrder(order1);
    orderBook.addOrder(order2);
    orderBook.addOrder(order3);
    orderBook.addOrder(order4);
    orderBook.addOrder(order5);
    orderBook.addOrder(order6);
    orderBook.addOrder(order7);
    orderBook.addOrder(order8);

    // Print the order book before matching orders
    std::cout << "Order Book before matching:" << std::endl;
    orderBook.printOrders();

    // Match orders in the order book
    orderBook.MatchOrders();

    // Print the order book after matching
    std::cout << "Order Book after matching:" << std::endl;
    orderBook.printOrders();

    return EXIT_SUCCESS;
}