#include <iostream>

int main(int argc, char* argv[], char* env[]) {
    std::cout << "Arguments:" << std::endl;
    for (int i = 0; i < argc; ++i)
        std::cout << argv[i] << std::endl;

    std::cout << "\nEnvironment:" << std::endl;
    while (*env != NULL)
        std::cout << *env++ << std::endl;
    return 0;
}
