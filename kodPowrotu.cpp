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

int main(int argc, char** argv) {
    int returnCode;
    bool isSilent = checkIfSilent(argv, argc);

    if (isSilent) {
        argc--;
    }

    if (argc == 1) {
        returnCode = 11;
    } else if (argc == 2) {
        
    } else {
        returnCode = 13;
    }
    
    if (!isSilent) {
        std::cout << returnCode << std::endl;
    }

    return returnCode;
}