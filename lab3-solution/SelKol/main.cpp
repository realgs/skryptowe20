#include <iostream>
#include <string>
#include <vector>

#define NO_ARGUMENTS 1
#define INVALID_ARGUMENTS 2
#define MISSING_COLUMN 3
#define DELIMITER "\t"

// Constraint - counting rows starts from 1 not 0

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

int main(int argc, char *argv[]) {
    if (argc < 2)
        return NO_ARGUMENTS;

    std::vector<std::vector<std::string>> rows;
    std::vector<int> column_numbers;

    for (int i = 1; i < argc; ++i) {
        try {
            int num = std::stoi(argv[i]) - 1;
            if (num < 0)
                return INVALID_ARGUMENTS;
            column_numbers.push_back(num);
        }
        catch (std::exception const &err) {
            return INVALID_ARGUMENTS;
        }
    }

    for (std::string line; getline(std::cin, line);)
        rows.push_back(splitString(line, DELIMITER));

    for (auto &row : rows) {
        for (size_t i = 0; i < column_numbers.size(); ++i) {
            if (column_numbers[i] >= row.size())
                return MISSING_COLUMN;
            std::cout << row[column_numbers[i]];
            if (i != column_numbers.size() + 1)
                std::cout << DELIMITER;
        }
        std::cout << std::endl;
    }
    
    return 0;
}
