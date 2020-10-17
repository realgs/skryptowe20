#include <iostream>

int main(int argc, char** argv, char** envp)
{
    char* envVar = envp[0];
    int i = 0;
    while (envVar != 0)
    {
        std::cout << envVar;
        std::cout << "\n";
        i++;
        envVar = envp[i];
    }

    char* arg = argv[0];
    i = 0;
    while (arg != 0)
    {
        std::cout << arg;
        std::cout << "\n";
        i++;
        arg = argv[i];
    }

    return 0;
}
