#include <iostream>

bool mode_is_silent_for_parameter(char* parameter) {
    return  parameter[0] == '/' && (parameter[1] == 's' || parameter[1] == 'S') && std::strlen(parameter) == 2;
}

int get_code_for_digit_parameter(char* digit_parameter) {
    int code = 12; // parameter is not a digit
    int parameter_length = std::strlen(digit_parameter);
    if (parameter_length == 1) {
        bool parameter_is_digit = digit_parameter[0] >= '0' && digit_parameter[0] <= '9';
        if (parameter_is_digit) {
            code = digit_parameter[0] - '0';
        }
    }
    
    return code;
}

int main(int argc, char* argv[])
{
    int code = 13; // too much parameters
    int digit_parameter_index = 1;
    bool mode_is_silent = false;
    if (argc > 1) {
        mode_is_silent = mode_is_silent_for_parameter(argv[argc - 1]);
        digit_parameter_index = argc == 2 ? 1 : 2;
        if (argc > 2 && !mode_is_silent) {
            mode_is_silent = mode_is_silent_for_parameter(argv[1]);
        }
    }

    if (argc <= 3) {
        if (argc == 1) {
            code = 11;
        } else if (argc == 2) {
            if (mode_is_silent) {
                code = 11;
            } else {
                code = get_code_for_digit_parameter(argv[digit_parameter_index]);
            }
        } else {
            if (mode_is_silent) {
                code = get_code_for_digit_parameter(argv[digit_parameter_index]);
            }
        }
    }

    if (!mode_is_silent) {
        std::cout << code;
    }

    return code;
}
