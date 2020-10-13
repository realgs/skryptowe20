#include <iostream>
#include <string>
#include <cstring>
#include <vector>

#define DELIMITER_WIN ";"
#define DELIMITER_UNIX ":"
#define SILENT_MODE_ARG_UPPER "/S"
#define SILENT_MODE_ARG_LOWER "/s"

std::vector<std::string> splitString(const std::string &text, const std::string &delimiter) {
    std::vector<std::string> result;
    size_t next = 0;
    size_t last = 0;
    std::string token;
    while (next < text.length()) {
        next = text.find(delimiter, last);
        if (next == std::string::npos)
            next = text.length();
        token = text.substr(last, next - last);
        result.push_back(token);
        last = next + 1;
    }
    return result;
}

int main(int argc, char *argv[], char *env[]) {
    std::string arg_str;
    std::string env_str;
    char **env_start = env;
    bool found;
    bool is_silent_mode = false;
    int silent_mode_arg_pos = -1;

    // lok for silent-mode switch argument
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], SILENT_MODE_ARG_LOWER) == 0 || strcmp(argv[i], SILENT_MODE_ARG_UPPER) == 0) {
            is_silent_mode = true;
            silent_mode_arg_pos = i;
            break;
        }
    }

    // print found env variables
    for (int i = 1; i < argc; ++i) {
        if (i == silent_mode_arg_pos)
            continue;
        arg_str = argv[i];
        found = false;
        while (*env != nullptr) {
            env_str = *env;
            size_t pos = env_str.find('=') + 1;
            std::string env_name = env_str.substr(0, pos - 1);
            std::string val = env_str.substr(pos, env_str.length() - pos);
            if (env_name.find(arg_str) != std::string::npos) {
                found = true;
                std::vector<std::string> values = splitString(val, DELIMITER_UNIX);
                std::cout << env_name << "=";
                if (values.size() > 1) {
                    std::cout << std::endl;
                    for (auto &value : values)
                        std::cout << value << std::endl;
                } else if (values.size() == 1)
                    std::cout << values[0] << std::endl;
                else
                    std::cout << std::endl;
            }
            ++env;
        }
        if (!found && !is_silent_mode)
            std::cout << arg_str << "=NONE" << std::endl;
        env = env_start;
    }
    return 0;
}
