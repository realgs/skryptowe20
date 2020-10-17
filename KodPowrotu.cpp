#include <iostream>
#include <string.h>

using namespace std;

bool isSilenceArgument(char argument[]);
bool isDigitArgument(char argument[]);

int main(int argc, char *argv[])
{
    const int NO_ARGUMENTS = 11;
    const int ARGUMENT_IS_NOT_A_DIGIT = 12;
    const int TOO_MANY_ARGUMENTS = 13;

    int resultCode = 0;
    bool isSilent = false;
    int firstExpectedArgumentIndex = 1;

    if (argc > 1)
    {
        if (isSilenceArgument(argv[1]))
        {
            isSilent = true;
            firstExpectedArgumentIndex++;
        }
    }

    if (firstExpectedArgumentIndex == argc)
    {
        resultCode = NO_ARGUMENTS;
    }
    else if (firstExpectedArgumentIndex + 1 == argc)
    {
        if (isDigitArgument(argv[firstExpectedArgumentIndex]))
        {
            resultCode = argv[firstExpectedArgumentIndex][0] - '0';
        }
        else
        {
            resultCode = ARGUMENT_IS_NOT_A_DIGIT;
        }
    }
    else
    {
        resultCode = TOO_MANY_ARGUMENTS;
    }

    if (!isSilent)
    {
        cout << resultCode << endl;
    }

    return resultCode;
}

bool isSilenceArgument(char argument[])
{
    if (strcmp(argument, "/s") == 0 || strcmp(argument, "/S") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool isDigitArgument(char argument[])
{
    if (strlen(argument) == 1 && isdigit((char)argument[0]))
    {
        return true;
    }
    else
    {
        return false;
    }
}

