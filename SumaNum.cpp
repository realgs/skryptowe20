#include <iostream>
#include <string>

int main()
{
    double sum = 0.;
    std::string input;
    while (std::cin >> input) {
        std::cout << input << "\t";
        try {
            sum += stod(input);
            std::cout << sum << "\n";
        }
        catch (const std::exception& ignored) {};
    }
    
    std::cout << "Sum = " << sum;
}
