#include <iostream>

int main(int argc, char* argv[], char* env[]) {
    std::cout<<("Environmental variables:\n");
    while (*env != NULL)
        std::cout<<(*env++)<<std::endl;

    std::cout<<("Program parameters:\n");
    for (int i = 0; i < argc; i++)
        std::cout<<(argv[i])<<std::endl;

    return 0;
}