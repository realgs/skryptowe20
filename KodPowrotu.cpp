#include <iostream>
#include <string>

const int NO_PARAMETERS_RC = 11;
const int NOT_A_DIGIT_RC = 12;
const int MORE_THAN_ONE_PARAM = 13;
const std::string SILENT_MODE_LOWER = "/s";
const std::string SILENT_MODE_UPPER = "/S";

bool is_silent(char *param_array[], int length) {
    for (int i = 0; i < length; i++)
        if (param_array[i] == SILENT_MODE_LOWER || param_array[i] == SILENT_MODE_UPPER)
            return true;
    return false;
}

int main(int argc, char* argv[], char* env[]) {
    bool silent_mode = is_silent(argv, argc);
    int return_code;

    if (argc == 1)
        return_code = NO_PARAMETERS_RC;

    else if (argc > 2)
        return_code = MORE_THAN_ONE_PARAM;

    else if (!isdigit(*argv[1]))
        return_code = NOT_A_DIGIT_RC;

    else
        return_code = atoi(argv[1]);

    if (!silent_mode)
        std::cout<<return_code;

    return return_code;
}