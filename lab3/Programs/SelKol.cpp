#include <iostream>
#include <fstream>
#include <string>
#include <string.h>

bool rightColumn(int argc, char** argv, int lineNumber)
{
    std::string number = std::to_string(lineNumber);
    for (int i = 1; i < argc; i++)
    {
        std::string argument = argv[i];
        if (argument._Equal(number))
        {
            return true;
        }
    }
    return false;
}

int main(int argc, char** argv) 
{
	std::ifstream zakupFile;
    std::string line;
    while (std::getline(std::cin, line))
    {
        int i = 0;
        std::string substring = line.substr(0, line.find("\t", 0));
        std::size_t lastCut = line.find("\t") + 1;
        bool isLast = false;
        while (!substring.empty()) 
        {
            if (rightColumn(argc, argv, i))
            {
                std::cout << substring;
                std::cout << "\t";
            }
            substring = line.substr(lastCut, line.find("\t", lastCut) - lastCut);
            lastCut = line.find("\t", lastCut) + 1;

            if (isLast) 
            {
                substring = "";
            }
            else if (lastCut == 0) 
            {
                isLast = true;
            }

            i++;
        }
        std::cout << "\n";
    }
}
