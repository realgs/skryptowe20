#include <iostream>

int main(int argc, char* argv[], char** env)
{
    std::cout << "Arguments of program\n";
    for (int i = 0; i < argc; i++)
        std::cout << argv[i] << '\n';

    std::cout << "Variables of environment \n";
    while (*env != nullptr)
        std::cout << *(env++) << '\n';
}