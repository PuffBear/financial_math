#include<iostream>
#include<cmath>

double addition(double x, double y){
    double sum = x + y;
    return sum;
}

double subtraction(double x, double y){
    double diff = x - y;
    return diff;
}

double multiplication(double x, double y){
    double product = x*y;
    return product;
}

double division(double x, double y){
    double quotient = x/y;
    return quotient;
}

double operation(int operations, int var_x, int var_y){
    if(operations == 1){
        return addition(var_x, var_y);
    }
    else if(operations == 2){
        return subtraction(var_x, var_y);
    }
    else if(operations == 3){
        return multiplication(var_x, var_y);
    }
    else{
        return division(var_x, var_y);
    }
}

int main(){
    std::string line(40, '=');
    std::cout << line << std::endl;
    std::cout << "1. Addition" << std::endl;
    std::cout << "2. Subtraction" << std::endl;
    std::cout << "3. Multiplication" << std::endl;
    std::cout << "4. Division" << std::endl;
    std::cout << line << std::endl;
    std::cout << "Enter the first variable: " << std::endl;
    int var_1;
    std::cin >> var_1;
    std::cout << "Enter the second variable: " << std::endl;
    int var_2;
    std::cin >> var_2;
    std::cout << line << std::endl;
    std::cout << "Enter the operation you want to perform either by writing the number of the operation" << std::endl;
    int operation_number;
    std::cin >> operation_number;
    double result = operation(operation_number, var_1, var_2);
    std::cout << "Result: " << result << std::endl;
    return EXIT_SUCCESS;
}