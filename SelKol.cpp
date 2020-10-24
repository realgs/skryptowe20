#include <iostream>
#include <vector>
#include <string>
#include <sstream>

std::vector<std::string> splitData(const std::string& data, char delimiter) {
    std::vector<std::string> splitData;
    std::string token;
    std::istringstream stream(data);
    while (getline(stream, token, delimiter))
    {
        splitData.push_back(token);
    }
    return splitData;
}

bool parameterIsNumber(char* parameter) {
    bool isNumber = true;
    for (int i = 0; i < std::strlen(parameter) && isNumber; i++) {
        if (parameter[i] < '0' || parameter[i] > '9') {
            isNumber = false;
        }
    }

    return isNumber;
}

int main(int argc, char* argv[])
{
    std::string input;
    while (getline(std::cin, input)) {
        std::vector<int> columnsNumbers;
        std::vector<std::string> data = splitData(input, '\t');
        int columnsAmount = data.size();

        bool correctParameters = true;
        for (int i = 1; i < argc && correctParameters; i++) {
            if (correctParameters = parameterIsNumber(argv[i])) {
                int columnNumber = (int)argv[i][0] - '0';
                if (correctParameters = (columnNumber <= columnsAmount)) {
                    columnsNumbers.push_back(columnNumber);
                }
            }
        }

        if (correctParameters) {
            std::vector<std::string> selectedColumns;
            for (int i = 0; i < columnsNumbers.size(); i++) {
                int columnIndex = columnsNumbers[i] - 1;
                std::cout << data[columnIndex] << "\n";
            }
        }
        else {
            std::cout << "Incorrect parameters.";
        }
    }
}
