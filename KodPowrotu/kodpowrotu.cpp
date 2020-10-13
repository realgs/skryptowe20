#include <iostream>
#include <cstring>
#include <string>

#define NOT_DIGIT 12
#define NO_ARGUMENTS 11
#define TOO_MANY_ARGUMENTS 13
#define SILENT_MODE_ARG_UPPER "/S"
#define SILENT_MODE_ARG_LOWER "/s"

int main(int argc, char *argv[]) {
    bool is_silent_mode = false;
    int silent_mode_arg_pos;
    int arg_count = 0;
    int main_arg;

    // lok for silent-mode switch argument
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], SILENT_MODE_ARG_LOWER) == 0 || strcmp(argv[i], SILENT_MODE_ARG_UPPER) == 0) {
            is_silent_mode = true;
            silent_mode_arg_pos = i;
            break;
        }
    }

    for (int i = 1; i < argc; ++i) {
        if (i == silent_mode_arg_pos)
            continue;

        if (++arg_count > 1) {
            if (!is_silent_mode)
                std::cout << TOO_MANY_ARGUMENTS << std::endl;
            return TOO_MANY_ARGUMENTS;
        }

        try {
            main_arg = std::stoi(argv[i]);
            std::string number_str = std::to_string(main_arg);
            if (main_arg > 9 || main_arg < 0 || number_str.length() < strlen(argv[i]))
                throw std::exception(); // also not digit
        }
        catch (std::exception const &err) {
            if (!is_silent_mode)
                std::cout << NOT_DIGIT << std::endl;
            return NOT_DIGIT;
        }
    }

    if (arg_count == 0)
        main_arg = NO_ARGUMENTS;

    if (!is_silent_mode)
        std::cout << main_arg << std::endl;
    return main_arg;
}
