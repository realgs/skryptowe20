#include <iostream>
#include <string>
#include <algorithm>

const std::string SILENT_MODE_LOWER = "/s";
const std::string SILENT_MODE_UPPER = "/S";
const char NAME_VALUE_DELIMETER = '=';
const char VALUES_DELIMETER = ';';


bool is_silent(char *param_array[], int length) {
    for (int i = 0; i < length; i++)
        if (param_array[i] == SILENT_MODE_LOWER || param_array[i] == SILENT_MODE_UPPER)
            return true;
    return false;
}

int main(int argc, char* argv[], char* env[]) {
    bool silent_mode = is_silent(argv, argc);
    bool param_found;

    for (int i = 1; i < argc; i++) {
        param_found = false;

        while (*env != nullptr) {
            std::string env_var = *env;
            std::string env_var_name = env_var.substr(0, env_var.find(NAME_VALUE_DELIMETER));
            std::string param = argv[i];

            if (env_var_name.find(param) != std::string::npos) {
                param_found = true;
                std::replace(env_var.begin(), env_var.end(), VALUES_DELIMETER, '\n');
                std::cout<<env_var;
            }
            *env++;
        }

        if (!param_found && !silent_mode)
            std::cout<<argv[i]<<"=NONE\n";
    }

    return 0;
}