#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[])
{
    system("set");
    for (int i = 1; i < argc; i++) {
        std::cout << argv[i] << std::endl;
    }
}
