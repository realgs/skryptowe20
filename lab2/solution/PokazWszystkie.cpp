#include <iostream>
#include <vector>
#include <set>
#include <string>
#include "Util.h"


int main(int argc, char* argv[], char* env[]) {
    std::vector<std::string> params;
    std::set<std::string> switches;
    parse_args(argv, argc, params, switches);

    std::cout << "Zmienne srodowiska:" << std::endl;
    while(*env != NULL)
        std::cout << (*env++) << std::endl;

    std::cout << std::endl << "Parametry programu:" << std::endl;
    for(int i = 0; i < params.size(); i++)
        std::cout << params[i] << std::endl;

    return 0;
}
