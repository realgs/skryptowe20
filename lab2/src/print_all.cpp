#include <iostream>

int main(const int argc, const char *const *const argv, char **env)
{
    std::cout << "Program args\n";
    for (int i = 0; i < argc; i++)
        std::cout << argv[i] << '\n';

    std::cout << "Environment\n";
    while (*env != nullptr)
        std::cout << *(env++) << '\n';
}
