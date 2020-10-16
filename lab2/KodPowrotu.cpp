#include<iostream>

bool isSilentModeOn(int argc, char** argv)
{
    for (int i = 1; i < argc; i++)
    {
        if (strcmp(argv[i], "/s") == 0 || strcmp(argv[i], "/S") == 0)
            return true;
    }

    return false;
}
bool isDigitNumber(char* argv)
{
    if (argv[1] == '\0' && isdigit(argv[0]))
        return true;
    return false;
}
int main(int argc, char** argv)
{
    int NO_PARAM = 11;
    int NOT_DIGIT = 12;
    int MULTIPLE_PARAMS = 13;
    bool is_silent = isSilentModeOn(argc, argv);
    if (is_silent)
        argc--;

    if (argc == 1)
    {
        if (!is_silent)
            std::cout << NO_PARAM;
        return NO_PARAM;
    }
        

    if (argc > 2)
    {
        if (!is_silent)
            std::cout << MULTIPLE_PARAMS;
        return MULTIPLE_PARAMS;
    }

    if (!isDigitNumber(argv[1]))
    {
        if (!is_silent)
            std::cout << NOT_DIGIT;
        return NOT_DIGIT;
    }
    
    char digit = argv[1][0];
    if(!is_silent)
        std::cout << digit;

    return digit;

}