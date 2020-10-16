#include <iostream>

int main(int argc, char* argv[], char* envp[])
{
    for (int i = 0; i < argc; i++) {
        std::cout << "argv["<< i << "] = " << argv[i] << "\n";
    }

    int index = 0;
    for (; *envp; envp++) {
        std::cout << "envp[" << index++ << "] = " << * envp << "\n";
    }
}
