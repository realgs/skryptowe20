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

int main(int argc, char** argv, char** envp) {

    return 0;
}