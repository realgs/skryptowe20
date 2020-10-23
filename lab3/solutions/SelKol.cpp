#include <iostream>
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>

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

bool contains(std::vector<int> v, int s)
{
    for (int i = 0; i < v.size(); i++)
    {
        if (v.at(i) == s)
        {
            return true;
        }
    }
    return false;
}

int main(int argc, char const *argv[])
{
    std::vector<int> args = charToIntVector(argc, argv);

    std::string text;
    std::ifstream file("Zakupy.txt");

    for (int i = 0; i < args.size(); i++)
    {
        std::cout<<args.at(i)<<std::endl;
    }
    std::cout<<std::endl;

    while (getline(file, text))
    {
        std::vector<std::string> line = split(text, "\t");
        for (int i = 0; i < line.size(); i++)
        {
            if (contains(args, i))
            {
                std::cout << line.at(i) << "\t";
            }
        }
        std::cout<<std::endl;
    }

    file.close();

    return 0;
}
