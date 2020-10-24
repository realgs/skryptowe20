#include <iostream>
#include <string>
#include <vector>

#define DELIMITER " "

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

int main() {
    double sum = 0.0;
    std::vector<std::string> values;

    for (std::string line; getline(std::cin, line);) {
        values = splitString(line, DELIMITER);
        for (auto &value : values) {
            try {
                double num = std::stod(value);
                sum += num;
            }
            catch (std::exception const &err) {}
        }
    }

    std::cout << sum << std::endl;
    return 0;
}
