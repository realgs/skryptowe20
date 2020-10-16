#include <iostream>

using namespace std;

const string SILENT_SIGN_LOWER = "/s";
const string SILENT_SIGN_UPPER = "/S";


bool isArgumentSilentSwitch(const string &flag) {
    return flag == SILENT_SIGN_LOWER || flag == SILENT_SIGN_UPPER;
}

int extractReturnCode(const string &data) {
    try {
        return std::stoi(data);
    } catch (std::exception const &e) {
        return 12;
    }
}

int printAndReturn(int code) {
    std::cout << code << std::endl;
    return code;
}

int main(int argc, char *argv[]) {
    if (argc == 1) {
        return printAndReturn(11);
    } else if (argc == 2) {
        return printAndReturn(extractReturnCode(argv[1]));
    } else if (argc == 3) {
        int returnCode = extractReturnCode(argv[1]);
        if (isArgumentSilentSwitch(argv[2])) {
            return returnCode;
        }
        return printAndReturn(returnCode);
    } else {
        return printAndReturn(13);
    }
}


