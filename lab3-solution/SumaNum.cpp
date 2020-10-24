#include <iostream>
#include <sstream>

int main(int argc, char* argv[]) {

    double sum = 0.0;
    std::string line;

    while (std::cin >> line){
        try {
            sum += stod(line);
        }
        catch (std::exception & e) {
        }
    }
    std::cout<<sum<<'\n';

    return 0;
}