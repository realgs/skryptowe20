#include <iostream>
#include <fstream>

int main(int argc, char *argv[]) {
    double sum = 0.0;
    std::string word;
    while (std::cin >> word) {
        try {
            sum += stod(word);
        } catch (const std::invalid_argument& e) {}
    }
    std::cout << sum << std::endl;
    return 0;
}