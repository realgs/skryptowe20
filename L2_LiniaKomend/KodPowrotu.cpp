#include <iostream>
#define EXIT_NO_PARAM 11
#define EXIT_NON_DIGIT 12
#define EXIT_MULTIPLE_PARAMS 13

using namespace std;


int main(int argc, char** argv) {
    int i_param = 1;
    int i_exit_code;
    bool b_is_silent = false;

    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "/s") == 0 || strcmp(argv[i], "/S") == 0) {
            b_is_silent = true;
            argc--;
            if (i == 1) {
                i_param = 2;
            }
        }
    }

    if (argc == 1) {
        i_exit_code = EXIT_NO_PARAM;
    } else if (argc > 2) {
        i_exit_code = EXIT_MULTIPLE_PARAMS;
    } else {
        if (isdigit(argv[i_param][0]) && argv[i_param][1] == '\0') {
            i_exit_code = argv[i_param][0] - '0';
        } else {
            i_exit_code = EXIT_NON_DIGIT;
        }
    }

    if (!b_is_silent) {
        cout << i_exit_code << endl;
    }

    return i_exit_code;
}
