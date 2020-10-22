#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

int main(int argc, char *argv[]) {
    if (argc > 4)
        return 1;
    for (int i = 0; i < argc; i++) {
        if (atoi(argv[i]) > 4)
            return 2;
    }

    std::string line;
    std::vector<std::string> output;

    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        std::string word;
        while (iss >> word)
            output.push_back(word);

        for (int i = 1; i < argc; i++)
            std::cout << output[atoi(argv[i]) - 1] << '\t';

        std::cout << std::endl;
        output.clear();
    }
    return 0;
}