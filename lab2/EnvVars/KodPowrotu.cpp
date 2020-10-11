#include <iostream>
#include <string>
using namespace std;

bool TryParseInt(const char* val, int& out)
{
    try
    {
        out = stoi(val);
        return true;
    }
    catch (const invalid_argument&)
    {
        return false;
    }
}

void PrintCode(int code, bool isSilent)
{
    if (!isSilent)
    {
        cout << code << endl;
    }
}

int main(int argc, char** argv)
{
    bool is_silent = argv[1] != NULL && (strcmp(argv[1], "/S") == 0 || strcmp(argv[1], "/s") == 0);

    if (is_silent)
    {
        --argc;
        ++argv;
    }

    if (argc == 1)
    {
        PrintCode(11, is_silent);
        return 11;
    }
    else if (argc > 2)
    {
        PrintCode(13, is_silent);
        return 13;
    }
    else
    {
        int number;

        if (TryParseInt(argv[1], number))
        {
            PrintCode(number, is_silent);
            return number;
        }
        PrintCode(12, is_silent);
        return 12;
    }
}

