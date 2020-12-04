#include <iostream>

int main(int argc, char* argv[], char* env[])
{   
    std::cout << "Environmental variables:" << std::endl;
    while (*env != nullptr) {
        std::cout << (*env++) << std::endl;
    }
    
    std::cout << "Program parameters:" << std::endl;
    for (int i = 0; i < argc; i++) {
        std::cout << argv[i] << std::endl;
    }
}

