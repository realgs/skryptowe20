#include <iostream>
#include <string>

int main(int argc, char** argv) {
    int number = 0;
    bool silent = false;

    std::string lastArgument = argv[argc - 1];
    if (lastArgument.compare("/s") == 0 || lastArgument.compare("/S") == 0)
    {
        silent = true;
    }

    if (silent && argc == 2) 
    {
        number = 11;
    }
    else if (!silent && argc == 1) 
    {
        number = 11;
    }
    else 
    {
        std::string firstArgument = argv[1];
        if (firstArgument.length() != 1)
        {
            number = 12;
        }
        else
        {
            if (argc == 3) 
            {   
                std::string secondArgument = argv[2];
                if (secondArgument.compare("/s") || secondArgument.compare("/S")) 
                {
                    try 
                    {
                        number = std::stoi(firstArgument);
                    }
                    catch (std::invalid_argument) 
                    {
                        number = 12;
                    }
                }
                else
                {
                    number = 13;
                }
            }
            else if (argc < 3)
            {
                try
                {
                    number = std::stoi(firstArgument);
                    if (number < 0 || number > 9)
                    {
                        number = 12;
                    }
                }
                catch (std::invalid_argument)
                {
                    number = 12;
                }
            }
            else 
            {
                number = 13;
            }
        }
    }

    if (!silent) 
    {
        std::cout << number;
    }

    return number;
}   
