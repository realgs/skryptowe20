#include <ostream>
#include <iostream>
#include <cstring>
#include <stdlib.h>

#define NO_INPUT_RETURN_CODE 11
#define INPUT_NOT_A_NUMBER 12
#define TOO_MANY_ARGUMENTS_RETURN_CODE 13

#define SILENT_MODE_UPPER "/S"
#define SILENT_MODE_LOWER "/s"

bool checkIfSilent(char *arg)
{

    if (!abs(strcmp(arg, SILENT_MODE_LOWER)) ||
        !abs(strcmp(arg, SILENT_MODE_UPPER)))
    {
        return true;
    }
    return false;
}

bool checkIfNumber(char *c)
{
    if (isdigit(*c) && strlen(c) == 1)
    {
        return true;
    }
    return false;
}

int main(int argc, char *argv[])
{
    int silent = false;
    int return_code = 0;
    int counter = 0;
    bool notANum = false;

    for (int i = 1; i < argc; i++)
    {
        // std::cout<<argv[i]<<std::endl;
        if (checkIfSilent(argv[i]))
        {
            // std::cout<<"silent"<<std::endl;
            silent = true;
        }
        else if (checkIfNumber(argv[i]))
        {
            // std::cout<<"number"<<std::endl;
            counter++;
            return_code = *argv[i]-'0';
        }
        else
        {
            // std::cout<<"NaN"<<std::endl;
            notANum = true;
        }
        
    }

    if (counter == 0)
    {
        return_code = NO_INPUT_RETURN_CODE;
    }
    else if (counter > 1)
    {
        return_code = TOO_MANY_ARGUMENTS_RETURN_CODE;
    }
    if(notANum){
        return_code = INPUT_NOT_A_NUMBER;
    }

    if (silent)
    {
        return return_code;
    }

    std::cout << return_code << std::endl;
    return return_code;
}
