#include <iostream>
#include <string>

int main(int argc, char* argv[])
{
    std::string userInput;

    while (getline(std::cin, userInput)) {
        bool containsParameter = false;
        for (int i = 0; i < argc && !containsParameter; i++) {
            containsParameter = userInput.find(argv[i]) != std::string::npos;
            if (containsParameter) {
                std::cout << userInput << "\n";
            }
        }
    }
}
