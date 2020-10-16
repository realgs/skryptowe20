#include <iostream>


int main(int argc, char* argv[], char* env[]) {
    std::cout << "Zmienne srodowiska:" << std::endl;
    while(*env != NULL)
        std::cout << (*env++) << std::endl;

    std::cout << std::endl << "Parametry programu:" << std::endl;
    for(int i = 0; i < argc; i++)
        std::cout << argv[i] << std::endl;

    return 0;
}
