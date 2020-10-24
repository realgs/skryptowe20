#include <iostream>
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>
#include "utils.h"

int main(int argc, char const *argv[])
{

    std::vector<int> args = charToIntVector(argc, argv);

    std::string text;

    while (std::getline(std::cin, text))
    {
        std::vector<std::string> line = split(text, "\t");
        for (int j = 0; j < args.size(); j++)
        {
            for (int i = 0; i < line.size(); i++)
            {
                if (args.at(j) == i)
                {
                    std::cout << line.at(i) << "\t";
                }
            }
        }

        std::cout << std::endl;
    }

    return 0;
}
