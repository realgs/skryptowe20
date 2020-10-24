#include <iostream>
#include <fstream>
#include <vector>
#include <string>

std::vector<std::string> getFileData(std::string fileName) {
    std::vector<std::string> fileData;
    std::string line;
    std::ifstream fileReader(fileName);

    while (std::getline (fileReader, line)) {
        fileData.push_back(line);
    }
    fileReader.close();

    return fileData;
}

std::vector<std::string> getColumnsForNumbers(std::vector<std::string> data, std::vector<int> columnsNumbers) {
    std::vector<std::string> selectedColumns;
    for (int i = 0; i < data.size(); i++) {
        int column = 1;
        std::string rowDataForColumn;

        bool columnChanged = false;
        bool firstSelectedColumn = true;
        std::vector<std::string> columnsRowsData;
        for (int j = 0; j < data[i].length(); j++) {
            if (data[i][j] == '\t') {
                column++;
                columnChanged = true;
                columnsRowsData.push_back(rowDataForColumn);
                rowDataForColumn = "";
            } else {
                rowDataForColumn += data[i][j];
                if (j == data[i].length() - 1) {
                    columnsRowsData.push_back(rowDataForColumn);
                }
            }
        }
        std::string selectedRow = "";
        for (int j = 0; j < columnsNumbers.size(); j++) {
            selectedRow += columnsRowsData[columnsNumbers[j] - 1] + "\t";
        }
        selectedColumns.push_back(selectedRow);
    }
    return selectedColumns;
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
    std::vector<int> columnsNumbers;
    std::vector<std::string> fileData = getFileData("Zakup.txt");
    int columnsAmount;
    if (fileData.size() > 0) {
        columnsAmount = 1;
        for (int i = 0; i < fileData[0].length(); i++) {
            if (fileData[0][i] == '\t') {
                columnsAmount++;
            }
        }
    } else {
        columnsAmount = 0;
    }

    bool correctParameters = true;
    for (int i = 1; i < argc && correctParameters; i++) {
        if ( correctParameters = parameterIsNumber(argv[i]) ) {
            int columnNumber = (int)argv[i][0] - '0';
            if ( correctParameters = (columnNumber <= columnsAmount) ) {
                columnsNumbers.push_back(columnNumber);
            }
        }
    }

    if (correctParameters) {
        std::vector<std::string> selectedColumns = getColumnsForNumbers(fileData, columnsNumbers);
        for (int i = 0; i < selectedColumns.size(); i++) {
            std::cout << selectedColumns[i] << "\n";
        }
    } else {
        std::cout << "Incorrect parameters.";
    }
}
