#include <iostream>
#include <string>

static int constexpr NOT_ENOUGHT_ARGUMENTS = 1;
static int constexpr ARGUMENT_NOT_A_NUMBER = 2;
static int constexpr FILE_NOT_FOUND = 3;

int main(int const argc, char const *const *const argv)
{
    if(argc < 2)
    {
        std::cout << "Program needs at least one argument";
        exit(NOT_ENOUGHT_ARGUMENTS);
    }

    std::string input;
    while(std::getline(std::cin, input))
    {
        bool if_printed = false;
        for(int i = 1; i < argc && !if_printed; i++)
            if(input.find(argv[i]) != std::string::npos)
            {
                std::cout << input << '\n';
                if_printed = true;
            }
    }
}
