#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    std::string input;

    while (getline(std::cin, input)) {
        bool containsParameter = false;
        for (int i = 0; i < argc && !containsParameter; i++) {
            containsParameter = input.find(argv[i]) != std::string::npos;
            if (containsParameter) {
                std::cout << input << "\n";
            }
        }
    }
}
