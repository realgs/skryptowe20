#include <iostream>

const char varSeparator = '=';
const char delimiter = ':';

bool checkIfSilent(char *args[], int length) {
    std::string str;
    for (int i = 0; i < length; i++) {
        str = args[i];
        if (str == "-s" || str == "-S") {
            return true;
        }
    }
    return false;
}

void printVariable(std::string &variableName, std::string &variableData) {
    std::cout << "i. " + variableName << std::endl;
    std::cout << "ii. =" << std::endl;
    if (variableData.find(delimiter) != std::string::npos) {
        size_t index;
        while ((index = variableData.find(delimiter)) != std::string::npos) {
            std::cout << "iii. " + variableData.substr(0, index) << std::endl;
            variableData.erase(0, index + 1);
        }
    }
    std::cout << "iii. " + variableData << std::endl;
}

int main(int argc, char **argv, char **envp) {
    int pos = 1;
    bool isSilent = checkIfSilent(argv, argc);
    bool isFound;

    if (isSilent) {
        pos++;
    }

    for (int i = pos; i < argc; i++) {
        isFound = false;
        std::string arg(argv[i]);
        char **envp_copy = envp;
        while (*envp_copy) {
            std::string val(*envp_copy++);
            size_t index = val.find(varSeparator);
            std::string varName = val.substr(0, index);
            val.erase(0, index + 1);
            if (varName.find(arg) != std::string::npos) {
                printVariable(varName, val);
                isFound = true;
            }
        }

        if (!isFound && !isSilent) {
            std::cout << "parametr = NONE" << std::endl;
        }
    }
    return 0;
}