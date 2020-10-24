#include "utils.h"

std::vector<int> charToIntVector(int argc, char const *argv[])
{
    std::vector<int> args;
    for (int i = 1; i < argc; i++)
    {
        int a = *argv[i] - '0';
        args.push_back(a);
    }
    return args;
}

std::vector<std::string> split(std::string s, std::string splitter)
{
    std::vector<std::string> seglist;
    size_t pos = 0;
    std::string token;

    while ((pos = s.find(splitter)) != std::string::npos)
    {
        token = s.substr(0, pos);
        seglist.push_back(token);
        s.erase(0, pos + splitter.length());
    }
    seglist.push_back(s);
    return seglist;
}

double convertToDouble(std::string s)
{
    try
    {
        double value = std::stof(s);
        return value;
    }
    catch (std::invalid_argument e)
    {
        return NULL;
    }
}

std::vector<double> convertToDoubleVector(std::vector<std::string> vector){
    
    std::vector<double> v;
    for (int i = 0; i < vector.size(); i++)
    {
        double value = convertToDouble(vector.at(i));
        if(value)
        v.push_back(value);
    }
    return v;
}

bool contains(std::string source, std::string sub)
{
    size_t a = source.find(sub);
    return (a != std::string::npos);
}
