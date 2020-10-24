#include <iostream>
#include <string>

int main()
{
    double sum = 0.;
    std::string userInput;
    while (std::cin >> userInput) {
        std::cout << userInput << "\t";
        try {
            sum += stod(userInput);
            std::cout << sum << "\n";
        }
        catch (const std::exception& ignored) {};
    }
    
    std::cout << "Sum = " << sum;
}
