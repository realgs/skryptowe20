#include <iostream>
#include <string>

using namespace std;

const int NO_PARAMETER = 11;
const int NOT_A_DIGIT = 12;
const int MORE_THAN_TWO_ARGS = 13;

bool isDigit(char c) {
    int num = (int) c;
    if (num > 47 && num < 58) return true;
    return false;
}

int main(int argc, char *argv[]) {
    bool silent_mode = false;
    for (int i = 0; i < argc; i++) {
        string str = argv[i];
        if (str.compare("/s") == 0 || str.compare("/S") == 0) {
            silent_mode = true;
            argc--;
        } 
    }
    if (argc == 1) {
        if (!silent_mode) cout << NO_PARAMETER;
        return NO_PARAMETER;
    }
    if (argc > 2) {
        if (!silent_mode) cout << MORE_THAN_TWO_ARGS;
        return MORE_THAN_TWO_ARGS;
    }
    int i = 0;
    if (!isDigit(argv[1][0]) || (isDigit(argv[1][0]) && argv[1][1] != NULL)) {
        if (!silent_mode) cout << NOT_A_DIGIT;
        return NOT_A_DIGIT;
    }
    while (argv[1][i] != NULL) {
        if (!isDigit(argv[1][i])) {
            if (!silent_mode) cout << NOT_A_DIGIT;
            return NOT_A_DIGIT;
        }
        i++;
    }
    char ret = *argv[1];
    if (!silent_mode) cout << ret;
    return ret;
}