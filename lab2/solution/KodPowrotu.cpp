#include <iostream>
#include <vector>
#include <set>
#include <string>
#include "Util.h"

const std::string SILENT_SWITCHES[] = {"/s", "/S"};
constexpr int NOT_ENOUGH_ARGUMENTS = 11;
constexpr int NOT_A_DIGIT = 12;
constexpr int TOO_MANY_ARGUMENTS = 13;
constexpr int MAX_PARAM_SIZE = 1;


int get_digit(const std::string& param) {
    return param.length() == 1 && param[0] >= '0' && param[0] <= '9' ? std::stoi(param) : NOT_A_DIGIT;
}

int main(int argc, char* argv[]) {
    std::vector<std::string> params;
    std::set<std::string> switches;
    parse_args(argv, argc, params, switches);

    bool silent = false;
    for(const auto& silent_switch : SILENT_SWITCHES)
        silent = silent || switches.count(silent_switch);

    int return_code;

    if(params.empty())
        return_code = NOT_ENOUGH_ARGUMENTS;
    else if(params.size() > MAX_PARAM_SIZE)
        return_code = TOO_MANY_ARGUMENTS;
    else
        return_code = get_digit(params[0]);

    if(!silent)
        std::cout << return_code << std::endl;
    return return_code;
}
