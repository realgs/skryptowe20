#include <iostream>
#include <string>
int main(int argc, char *argv[]) {

    for(std::string line; getline(std::cin, line);) {
        for (int i = 1; i < argc; ++i) {
            if (line.find(argv[i]) != std::string::npos) {
                std::cout << line << std::endl;
                break;
            }
        }
    }
    return 0;
}
