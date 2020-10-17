#include <iostream>

int main(int argc, char** argv, char** envp)
{
    char* arg = argv[1];
    int i = 1;
    bool silentMode = false;
    std::string lastArgument = argv[argc - 1];
    if (lastArgument.compare("/s") == 0 || lastArgument.compare("/S") == 0)
    {
        silentMode = true;
    }

    while (arg != 0)
    {
        if (i == argc - 1 && silentMode)
        {
            break;
        }

        std::string argument = arg;
        bool exist = false;
        char* envVar = envp[0];
        int j = 0;
        while (envVar != 0)
        {
            std::string variable = envVar;
            std::string variableName = variable.substr(0, variable.find("="));
            std::size_t found = variableName.find(arg);
            if (found != std::string::npos)
            {
                std::size_t lastCut = variable.find("=") + 1;
                std::string substring = variable.substr(lastCut, variable.find(";", lastCut) - lastCut);
                while (!substring.empty())
                {
                    std::cout << variableName;
                    std::cout << " = ";
                    std::cout << substring;
                    std::cout << "\n";
                    lastCut = variable.find(";", lastCut) + 1;
                    if (lastCut != 0)
                    {
                        std::size_t newCut = variable.find(";", lastCut);
                        substring = variable.substr(lastCut, newCut - lastCut);
                    }
                    else
                    {
                        substring = "";
                    }
                }
                exist = true;
            }
            j++;
            envVar = envp[j];
        }
        if (!exist && !silentMode)
        {
            std::cout << arg;
            std::cout << " = NONE";
        }
        i++;
        arg = argv[i];
    }

    return 0;
}