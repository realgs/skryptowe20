#include "utils.h"
#include <iostream>
#include <string>

int main(int argc, char const *argv[])
{
    std::vector<std::string> input;
    std::string line;

    while (std::getline(std::cin, line))
    {
        input.push_back(line);
    }
    
    for (int i = 0; i < input.size(); i++)
    {
        for (int j = 1; j < argc; j++)
        {
            if (contains(input.at(i), argv[j]))
            {
                std::cout << input.at(i) << std::endl;
                break;
            }
        }
    }

    return 0;
}
