#include <iostream>
#include <vector>
#include <set>

const std::string SILENT_SWITCH_LOWER = "/s";
const std::string SILENT_SWITCH_UPPER = "/S";
constexpr int NOT_ENOUGH_ARGUMENTS = 11;
constexpr int NOT_A_DIGIT = 12;
constexpr int TOO_MANY_ARGUMENTS = 13;
constexpr int MAX_SIZE = 1;


// Z tego co rozumiem z tresci zadania, to przelaczniki nie wliczaja sie do liczby
// parametrow, wiec wywolanie KodPowrotu.exe 1 /s /f powinno wciaz zwrocic 1.

void parse_args(char** args, const int count, std::vector<std::string>& params, std::set<std::string>& switches) {
    for(int i = 1; i < count; ++i) {
        if(args[i][0] == '/')
            switches.insert(args[i]);
        else
            params.push_back(args[i]);
    }
}

int get_digit(const std::string& param) {
    return param.length() == 1 && param[0] >= '0' && param[0] <= '9' ? std::stoi(param) : NOT_A_DIGIT;
}

int main(int argc, char* argv[]) {
    std::vector<std::string> params;
    std::set<std::string> switches;
    parse_args(argv, argc, params, switches);

    bool silent = switches.count(SILENT_SWITCH_LOWER) || switches.count(SILENT_SWITCH_UPPER);
    int return_code;

    if(params.empty())
        return_code = NOT_ENOUGH_ARGUMENTS;
    else if(params.size() > MAX_SIZE)
        return_code = TOO_MANY_ARGUMENTS;
    else
        return_code = get_digit(params[0]);

    if(!silent)
        std::cout << return_code << std::endl;
    return return_code;
}
