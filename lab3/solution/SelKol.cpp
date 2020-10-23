#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>

constexpr int ERROR_NPOS = -1;
constexpr char FILE_DELIMITER = '\t';
constexpr char PRINT_DELIMTIER = '\t';

constexpr int ARG_ERROR_CODE = 1;
constexpr int FILE_ERROR_CODE = 2;

int parse_args(char** args, const int count, std::vector<int>& selected_columns) {
    int value;

    for(int args_i = 1; args_i < count; ++args_i) {
        std::string arg(args[args_i]);

        if(std::all_of(arg.begin(), arg.end(), isdigit) && (value = std::stoi(arg)) > 0)
            selected_columns.push_back(value - 1);
        else
            return args_i;
    }
    return ERROR_NPOS;
}

std::vector<std::string> split(const std::string& line, char delimiter) {
    std::vector<std::string> result;

    std::istringstream iss(line);
    std::string token;

    while (std::getline(iss, token, delimiter))
        result.push_back(token);

    return result;
}

int print_columns(const std::vector<int>& selected_columns) {
    if(selected_columns.empty())
        return ERROR_NPOS;

    std::string line;
    int max_column = *std::max_element(selected_columns.begin(), selected_columns.end());

    for(int i = 1; std::getline(std::cin, line); ++i) {
        std::vector<std::string> split_line = split(line, FILE_DELIMITER);

        if(max_column >= split_line.size())
            return i;

        std::string to_print;
        for(const auto& column : selected_columns) {
            to_print += split_line[column];
            to_print += '\t';
        }

        to_print.pop_back(); // remove last '\t'
        std::cout << to_print << std::endl;
    }
    return ERROR_NPOS;
}

int main(int argc, char* argv[]) {
    std::vector<int> selected_columns;
    int error_pos = parse_args(argv, argc, selected_columns);

    if(error_pos != ERROR_NPOS) {
        std::cout << "Wystapil blad w argumencie na pozycji " << error_pos << std::endl;
        return ARG_ERROR_CODE;
    }

    error_pos = print_columns(selected_columns);

    if(error_pos != ERROR_NPOS) {
        std::cout << "Zbyt mala liczba kolumn w linii " << error_pos << std::endl;
        return FILE_ERROR_CODE;
    }
    return 0;
}
