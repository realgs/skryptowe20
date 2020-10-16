#include <iostream>
#include <vector>

bool mode_is_silent_for_parameter(char* parameter) {
    return  parameter[0] == '/' && (parameter[1] == 's' || parameter[1] == 'S') && std::strlen(parameter) == 2;
}

void print_environment_variable(std::string name, std::string content) {
    std::cout << "\n" << name << "\n" << "=\n";
    for (int i = 0; i < content.length(); i++) {
        if (content[i] == ';') {
            std::cout << "\n";
        } else {
            std::cout << content[i];
        }
    }
}

int main(int argc, char* argv[], char* envp[])
{
    bool mode_is_silent = false;
    if (argc > 1) {
        mode_is_silent = mode_is_silent_for_parameter(argv[argc - 1]);
        if (argc > 2 && !mode_is_silent) {
            mode_is_silent = mode_is_silent_for_parameter(argv[1]);
        }
    }

    std::string env_str;
    const int PARAMETERS_INDEX_OFFSET = 1;
    std::vector<bool> usage_of_parameters(0);
    for (int i = PARAMETERS_INDEX_OFFSET; i < argc; i++) {
        usage_of_parameters.push_back(false);
    }


    for (; *envp; envp++) {
        env_str = *envp;
        for (int i = 1; i < argc; i++) {
            if (env_str.find(argv[i]) < std::strlen(argv[i])) {
                std::string env_name = env_str.substr(0, env_str.find("="));
                std::string env_content = env_str.substr(env_str.find("=") + 1, env_str.length());
                print_environment_variable(env_name, env_content);
                usage_of_parameters[i - PARAMETERS_INDEX_OFFSET] = true;
                break;
            }
        }
    }

    if (!mode_is_silent) {
        for (int i = 0; i < usage_of_parameters.size(); i++) {
            if (!usage_of_parameters[i]) {
                std::cout << "\n" << argv[i + PARAMETERS_INDEX_OFFSET] << " = NONE";
            }
        }
    }
}
