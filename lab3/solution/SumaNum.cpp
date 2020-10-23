#include <iostream>
#include <string>

double sum_from_stdin() {
    std::string token;
    double sum = 0;

    while(std::cin >> token) {
        try {
            sum += stod(token);
        }
        catch(std::invalid_argument& e) {}
    }
    return sum;
}

int main() {
    std::cout << sum_from_stdin() << std::endl;
    return 0;
}
