// zadanie 2
#include <iostream>
#include <string>

int main()
{
    double sum = 0;
    std::string number;
    while(std::getline(std::cin, number))
        sum += std::atof(number.c_str());

    std::cout << sum; 
}
