#include <iostream>
#include <string>
#include <string.h>

bool contains(int argc, char** argv, std::string line)
{
    for (int i = 1; i < argc; i++)
    {
        std::string argument = argv[i];
        if (line.find(argument) != std::string::npos)
        {
            return true;
        }
    }
    return false;
}

int main(int argc, char** argv)
{
    std::string line;
    while (std::getline(std::cin, line))
    {
        if (contains(argc, argv, line)) 
        {
            std::cout << line + "\n";
        }
    }
}
