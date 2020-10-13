#include <iostream>

bool checkIfSilent(char *args[], int length) {
    std::string str;
    for (int i = 0; i < length; i++) {
        str = args[i];
        if (str == "/s" || str == "/S") {
            return true;
        }
    }
    return false;
}

bool isDigit(char* value) {
    try {
        int val = std::stoi(value);
        return (val >= 0 && val <= 9);
    } catch (...) {
        return false;
    }
}

int main(int argc, char** argv) {
    int pos = 1;
    int returnCode;
    bool isSilent = checkIfSilent(argv, argc);

    if (isSilent) {
        argc--;
        pos++;
    }

    if (argc == 1) {
        returnCode = 11;
    } else if (argc == 2) {
        if (isDigit(argv[pos])) {
            returnCode = atoi(argv[pos]);
        } else {
            returnCode = 12;
        }
    } else {
        returnCode = 13;
    }
    
    if (!isSilent) {
        std::cout << returnCode << std::endl;
    }

    return returnCode;
}