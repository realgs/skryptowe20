#include <iostream>
#include <sstream>


int main(int argc, char* argv[]) {

    std::string line;
    double sum = 0;
    while (getline(std::cin, line)) {
        sum += atof(line.c_str());
    }
    std::cout << sum;
}
