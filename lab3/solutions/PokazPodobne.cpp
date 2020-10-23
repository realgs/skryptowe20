#include <iostream>
#include <ostream>
#include <cstring>
#include <stdlib.h>
#include <vector>

#define SILENT_MODE_UPPER "/S"
#define SILENT_MODE_LOWER "/s"

bool checkIfSilent(char *arg)
{
    return (!abs(strcmp(arg, SILENT_MODE_LOWER)) ||
            !abs(strcmp(arg, SILENT_MODE_UPPER)));
}

bool contains(std::string path, std::string sub)
{
    std::string seg = path.substr(0, path.find('='));
    size_t a = seg.find(sub);
    bool b = (a != std::string::npos);
    return b;
}

std::vector<std::string> substring(std::string s, std::string splitter)
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
    if (seglist.size() == 0)
    {
        seglist.push_back(s);
    }
    return seglist;
}

int main(int argc, char *argv[], char *env[])
{
    bool silent = false;
    int omit = 0;
    for (int i = 1; i < argc; i++)
    {
        if (checkIfSilent(argv[i]))
        {
            silent = true;
            omit = i;
        }
    }
    for (int i = 1; i < argc; i++)
    {
        bool found = false;

        if (i != omit)
        {
            int j = 0;
            while (env[j] != nullptr)
            {
                if (contains(env[j], argv[i]))
                {
                    std::vector<std::string> v;
                    v = substring(std::string(env[j]), std::string(";"));
                    for (std::vector<std::string>::size_type k = 0; k < v.size(); k++)
                    {
                        std::cout << v.at(k) << std::endl;
                    }
                    found = true;
                }
                j++;
            }

            if (!found && !silent)
            {
                std::cout << argv[i] << " = NONE" << std::endl;
            }
        }
    }

    return 0;
}
