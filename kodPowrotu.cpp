#include <iostream>
#include <string>

bool isSilent(char* argtab[])
{
    std::string arg;
    while (*argtab != nullptr)
    {
        arg = *argtab++;
        if (arg == "-s" || arg == "-S")
        {
            return true;
        }
    }
    return false;
}

int main(int argc, char* argv[])
{

    bool silent = isSilent(argv);
    int i = 1;
    if (silent)
    {
        argc--;
        i++;
    }

    int returnCode = 11;

    if (argc == 2 )
    {
        if ( isdigit(*argv[i]) && strlen(argv[i]) == 1)
            returnCode = atoi(argv[i]);
        else
            returnCode = 12;
    }
    else if (argc > 2)
    {
        returnCode = 13;
    }
    if (!silent)
    {
        std::cout << returnCode << std::endl;
    }
    return returnCode;
}
