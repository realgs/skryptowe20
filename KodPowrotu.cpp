#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <vector>

using namespace std;

bool isStringASingleDigit(char *argv);
bool isSilencedMode(int argc, char *argv[]);
vector<char *> returnSingleDigits(int argc, char *argv[]);

int main(int argc, char *argv[])
{
    int exitCode = 11;
    bool isSilenced = isSilencedMode(argc, argv);
    vector<char *> singleDigits = returnSingleDigits(argc, argv);
    int numberOfSingleDigits = singleDigits.size();

    if ((argc > 2 && !isSilenced) || (argc > 3 && isSilenced))
    {
        exitCode = 13;
    }
    else if (numberOfSingleDigits == 1)
    {
        exitCode = atoi(singleDigits[0]);
    }
    else if ((argc == 2 && !isSilenced) || (argc == 3 && isSilenced))
    {
        exitCode = 12;
    }

    if (!isSilenced)
    {
        cout << exitCode;
    }
    return exitCode;
}

bool isStringASingleDigit(char *arg)
{
    bool isSingleDigitResult = true;
    for (int i = 0; i < strlen(arg); i++)
    {
        if (!isdigit(arg[i]))
        {
            isSingleDigitResult = false;
        }
        else if (isdigit(arg[i]) && i > 0)
        {
            isSingleDigitResult = false;
        }
    }
    return isSingleDigitResult;
}

bool isSilencedMode(int argc, char *argv[])
{
    for (int i = 0; i < argc; i++)
    {
        if (!strcmp(argv[i], "/S") || !strcmp(argv[i], "/s"))
        {
            return true;
        }
    }
    return false;
}

vector<char *> returnSingleDigits(int argc, char *argv[])
{
    vector<char *> singleDigits;
    for (int i = 0; i < argc; i++)
    {
        if (isStringASingleDigit(argv[i]))
        {
            singleDigits.push_back(argv[i]);
        }
    }
    return singleDigits;
}
 