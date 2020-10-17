#include <iostream>
#include <algorithm>
#include <vector>
#include <set>
#include <string>
#include "Util.h"

const std::string SILENT_SWITCH = "/S";
const std::string NOT_FOUND_STRING = " = NONE";
constexpr char KEY_VALUE_SEPARATOR = '=';
constexpr char VALUES_DELIMITER = ';';


void print_var(const std::string& var) {
    int separator_index = var.find(KEY_VALUE_SEPARATOR);
    std::string name = var.substr(0, separator_index);
    std::cout << name << "\n" << KEY_VALUE_SEPARATOR << "\n";

    std::string values = var.substr(separator_index + 1);
    std::replace(values.begin(), values.end(), VALUES_DELIMITER, '\n');
    std::cout << values << "\n\n";
}

void find_and_print(char** vars, const std::vector<std::string>& to_find, bool silent) {
    char** initial_vars = vars;
    for(int i = 0; i < to_find.size(); ++i) {
        bool none_found = true;

        while(*vars != NULL) {
            std::string var(*vars++);

            if(var.find(to_find[i]) != std::string::npos) {
                print_var(var);
                none_found = false;
            }
        }
        if(none_found && !silent)
            std::cout << to_find[i] << NOT_FOUND_STRING << "\n\n";

        vars = initial_vars;
    }
}

int main(int argc, char* argv[], char* env[]) {
    std::vector<std::string> params;
    std::set<std::string> switches;
    parse_args(argv, argc, params, switches);

    bool silent = switches.count(SILENT_SWITCH);

    find_and_print(env, params, silent);

    return 0;
}
