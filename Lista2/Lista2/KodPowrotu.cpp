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
    // Other parameter
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
    // Look for "/s"
    for (int i = 0; i < argc; i++)
    {
        if (parseArgv(argv[i]) == -1)
        {
            silent = true;
        }
    }

    // First argument is always executable name
    if (argc == 1)
    {
        return returnCode(11);
    }

    if (argc == 2)
    {
        // second argument has to be digit
        int digit = parseArgv(argv[1]);

        // First arg isn't digit
        if (digit < 0)
        {
            return returnCode(12);
        }
        // Return digit
        else
        {
            return returnCode(digit);
        }
    }

    if (argc == 3)
    {
        int digit1 = parseArgv(argv[1]);
        int digit2 = parseArgv(argv[2]);

        // Two parameters
        if ((digit1 >= 0 || digit1 == -2) && (digit2 >= 0 || digit2 == -2))
        {
            return returnCode(13);
        }
        // Arg 2 is digit
        else if (digit1 == -1 && digit2 >= 0)
        {
            return returnCode(digit2);
        }
        // Arg 1 is digit
        else if (digit2 == -1 && digit1 >= 0)
        {
            return returnCode(digit1);
        }
        // No parameters
        else if (digit1 == -2 && digit2 == -2)
        {
            return returnCode(11);
        }
        // Parameter is not a digit
        else
        {
            return returnCode(12);
        }
    }

    // Argc>3 => more than 1 param for sure
    
    return returnCode(13);
}
