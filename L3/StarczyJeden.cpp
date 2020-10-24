#include <iostream>
#include <sstream>


int main(int argc, char* argv[]) {

    std::string line;
    while (getline(std::cin, line)) {
        for (int i = 1; i < argc; i++) {
            if (line.find(argv[i]) != std::string::npos) {
                std::cout << line << std::endl;
                break;
            }
        }
    }

}
