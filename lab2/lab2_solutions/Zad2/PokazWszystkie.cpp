#include <iostream>
#include <ostream>


int main(int argc, char const *argv[], char *env[])
{
    int i = 0;
    while (env[i] != nullptr)
    {
        std::cout<<env[i]<<std::endl;
        i++;
    }
    for (int i = 0; i < argc; i++)
    {
        std::cout<<argv[i]<<std::endl;
    }
    
    
    return 0;
}
