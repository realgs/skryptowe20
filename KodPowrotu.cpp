#include <iostream>
#include <string>


int main(int argc, char* argv[]){
    bool isSilent = false;
    int silentOffset = -1;
    if (argc >= 2){
        for (int i = 1; i < argc; i++) {
            std::string silentString = argv[i];
            if (((argv[i][0] == '/' && argv[i][1] == 'S') || (argv[i][0] == '/' && argv[i][1] == 's')) && silentString.length() == 2) {
                isSilent = true;
                silentOffset = i;
            }
        }
    }
    int returnCode;
    if (argc == 1) {
        if (!isSilent){
            printf("Kod powrotu: %d\n", 11);
        }
        return 11;
    }
    else if (argc >= 3) {
        if (!isSilent){
            printf("Kod powrotu: %d\n", 13);
            return 13;
        }
        else if (argc > 3){
            return 13;
        }
    }

    if (argc == 2 && (argv[1][0] == '/') && (argv[1][1] == 'S' || argv[1][1] == 's') && (((std::string)argv[1]).length() == 2)) {
        return 11;
    }
    try {
        if (isSilent){
            if (silentOffset == 1) {
                returnCode = std::stoi(argv[2]);
                if (argv[2][1] != NULL) {
                    returnCode = 12;
                }
            }
            else {
                returnCode = std::stoi(argv[1]);
                if (argv[1][1] != NULL) {
                    returnCode = 12;
                }
            }
        }
        else {
            returnCode = std::stoi(argv[1]);
            if (argv[1][1] != NULL) {
                returnCode = 12;
            }
        }
    }
    catch (std::exception e) {
        returnCode = 12;
    }
    if (!isSilent) {
        printf("Kod powrotu: %d\n", returnCode);
    }
    return returnCode;
}