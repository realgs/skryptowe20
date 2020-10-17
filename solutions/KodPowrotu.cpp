#include <iostream>
#include <cstring>

using namespace std;

bool isSilent(int argc, char *argv[])
{  
    for (int i = 0; i < argc; i++)
    {
        if ((string) argv[i] == "/s" || (string) argv[i] == "/S")
        {
            return true;
        }
    }
    return false;
}

int check_code(char* value)
{
    if (isdigit(value[0]) && strlen(value) == 1)
    {
        return atoi(value);
    }
    else
    {
        return 12;
    }
}

int main(int argc, char *argv[])
{ 
    int return_code = 11;
    bool is_in_silent_mode = isSilent(argc, argv);
    switch (argc)
    {
        case 1:
            return_code = 11;
            break;
        case 2:
            if (is_in_silent_mode)
            {
                return_code = 11;
            }
            else
            {
                return_code = check_code(argv[1]);
            }
            break;
        case 3:
            return_code = 13;
            if (is_in_silent_mode)
            {
                return_code = 12;
                for (int i = 1; i < argc; i++)
                {
                    int code = check_code(argv[i]);
                    if (code != 12)
                    {
                        return_code = code;
                    }
                }
            }
            break;
        default:
            return_code = 13;
    }
    if (!is_in_silent_mode)
    {
        cout << return_code;
    }

    return return_code;
}