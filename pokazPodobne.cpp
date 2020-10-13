#include <iostream>

bool checkIfSilent(char* args[], int length) {
    std::string str;
    for (int i = 0; i < length; i++) {
        str = args[i];
        if (str == "-s" || str == "-S") {
            return true;
        }
    }
    return false;
}

void printVariable(std::string &variableName, std::string &variableData, char del = ':') {

}

int main(int argc, char **argv, char **envp) {
    int pos = 1;
    char delimiter = '=';
    bool isSilent = checkIfSilent(argv, argc);
    bool isFound;

    if (isSilent) {
        pos++;
    }

    for (int i = pos; i < argc; i++) {
        isFound = false;
        std::string arg(argv[i]);
        while (*envp) {
            std::string val(*envp++);
            size_t index = val.find(delimiter);
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