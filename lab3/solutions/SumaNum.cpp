#include <iostream>
#include <string>
#include <vector>
#include "utils.h"

int main(int argc, char *argv[])
{
    std::vector<std::string> input;

    std::string line;
    while (std::getline(std::cin, line))
    {
        std::vector<std::string> temp = split(line, "\t");
        for (int i = 0; i < temp.size(); i++)
        {
           input.push_back(temp.at(i));
        }        
    }
    std::vector<double> v = convertToDoubleVector(input);
    double out = 0;
    for (int i = 0; i < v.size(); i++)
    {
        out+= v.at(i);
    }
    std::cout<<out<<std::endl;

    return 0;
}
