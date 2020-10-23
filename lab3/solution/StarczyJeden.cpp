#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> parse_args(char** args, int count) {
    std::vector<std::string> parsed_args;
    for(int i = 1; i < count; ++i) {
        parsed_args.push_back(std::string(args[i]));
    }
    return parsed_args;
}

void print_lines_containing(std::vector<std::string> params) {
    std::string line;

    while(std::getline(std::cin, line)) {
        for(const auto& param : params) {
            if(line.find(param) != std::string::npos) {
                std::cout << line << std::endl;
                break;
            }
        }
    }
}

int main(int argc, char* argv[]) {
    std::vector<std::string> args = parse_args(argv, argc);
    print_lines_containing(args);
    return 0;
}
