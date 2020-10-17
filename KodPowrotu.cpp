#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

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

bool is_digit(std::string s)
{
    if (s.length() > 1)
        return false;
    for (int i = 0; i < s.length(); i++)
        if (isdigit(s[i]) == false)
            return false;

    return true;
}

int main(int argc, char* argv[], char* env[]) {
    bool silent_mode = is_silent(argv, argc);
    int return_code;

    std::vector<std::string> all_args(argv, argv + argc);
    all_args.erase(std::remove(all_args.begin(), all_args.end(), SILENT_MODE_LOWER), all_args.end());
    all_args.erase(std::remove(all_args.begin(), all_args.end(), SILENT_MODE_UPPER), all_args.end());
    int size = all_args.size();

    if (size == 1)
        return_code = NO_PARAMETERS_RC;

    else if (size > 2)
        return_code = MORE_THAN_ONE_PARAM;

    else if (!is_digit(all_args[1]))
        return_code = NOT_A_DIGIT_RC;

    else
        return_code = stoi(all_args[1]);

    if (!silent_mode)
        std::cout<<return_code;

    return return_code;
}