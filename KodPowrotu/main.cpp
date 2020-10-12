#include <iostream>
#include <cstring>

#define NOT_DIGIT 12
#define NO_ARGUMENTS 11
#define TOO_MANY_ARGUMENTS 13

const char SILENT_MODE_ARG_UPPER[]  = "/S";
const char SILENT_MODE_ARG_LOWER[]  = "/s";

int main(int argc, char* argv[])
{
    bool silent_mode = false;
    int arg_count = 0;
    int main_arg;

    for (int i = 1; i < argc; ++i)
    {
        if ( strcmp(argv[i],SILENT_MODE_ARG_LOWER) == 0 || strcmp(argv[i],SILENT_MODE_ARG_UPPER) == 0)
            silent_mode = true;
        else
        {
            try {
                main_arg = std::stoi(argv[i]);
                if (main_arg > 9 || main_arg < 0)
                    throw std::exception();
                ++arg_count;
            } catch (std::exception const &err) {
                if (!silent_mode)
                    std::cout << NOT_DIGIT << std::endl;
                return NOT_DIGIT;
            }
        }
    }
    if (arg_count > 1)
        main_arg = TOO_MANY_ARGUMENTS;
    if (arg_count == 0)
        main_arg = NO_ARGUMENTS;

    if (!silent_mode)
        std::cout << main_arg << std::endl;
    return main_arg;
}
