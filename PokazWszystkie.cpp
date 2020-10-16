#include <iostream>

int main( int argc, char* argv[], char** env)
{
    std::cout << "-|-|-|-|-|-|-|-|-|-|-\n";
    std::cout << "Program args\n";
    for (int i = 0; i < argc; i++)
        std::cout << argv[i] << '\n';

    std::cout << "-|-|-|-|-|-|-|-|-|-|-\n";
    std::cout << "Environment variables\n";
    while (*env != nullptr)
        std::cout  << *(env++) << '\n';
}
