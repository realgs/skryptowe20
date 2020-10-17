#include <iostream>

using namespace std;

bool silent = false;

int parseArgv(char str[])
{
    // First char is ascii digit, second null => return digit
    if (str[0] >= 48 && str[0] <= 57 && str[1] == 0)
    {
        // Return digit converted to int
        return str[0] - 48;
    }
    // Silent parameter => return -1
    else if (str[0] == 47 && (str[1] == 83 || str[1] == 115) && str[2] == 0)
    {
        return -1;
    }
    // Other parameter => -2
    else
    {
        return -2;
    }
}

int returnCode(int val)
{
    if (!silent)
    {
        cout << val << endl;
    }
    return val;
}

int main(int argc, char* argv[])
{   
    int* paramsParsed = new int[argc - 1];
    int arrayLength = argc - 1;

    for (int i = 0; i < arrayLength; i++)
    {
        // This function assigns 0..9 to digits, -1 to silent switches and -2 to incorrect parameters
        paramsParsed[i] = parseArgv(argv[i + 1]);
    }

    for (int i = 0; i < arrayLength; i++)
    {
        if (paramsParsed[i] == -1)
        {
            silent = true;
        }
    }

    // Check for number of parameters
    int allParamsCount = 0;
    for (int i = 0; i < arrayLength; i++)
    {
        if (paramsParsed[i] != -1)
        {
            allParamsCount++;
        }
    }

    if (allParamsCount == 0)
    {
        return returnCode(11);
    }
    else if (allParamsCount > 1)
    {
        return returnCode(13);
    }

    for (int i = 0; i < arrayLength; i++)
    {
        // Only potential digit
        if (paramsParsed[i] != -1)
        {
            // Error
            if (paramsParsed[i] == -2)
            {
                return returnCode(12);
            }
            else
            {
                return returnCode(paramsParsed[i]);
            }
        }
    }
}
