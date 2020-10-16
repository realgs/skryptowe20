#include <iostream>
#include <stdlib.h>
#include <string>

using namespace std;

bool isSilent(char* param)
{
    if (param[0] == '\\' && (param[1] == 's' || param[1] == 'S') && param[2] == NULL) {
        return true;
    }
    else {
        return false;
    }
}

int main(int argc, char* argv[])
{
    bool isSilentP = false;
    int kodPowrotu;
    for (int i = 0; i < argc; i++) {
        if (isSilent(argv[i])) {
            isSilentP = true;
        }
        else {
            try {
                kodPowrotu = stoi(argv[i]);

                if (kodPowrotu > 9 || kodPowrotu < 1) {
                    kodPowrotu = 12;
                }
            }
            catch (exception e) {
                kodPowrotu = 12;
            }
        }
    }
    if ((argc == 2 && isSilentP) || (argc == 1))
    {
        kodPowrotu = 11;
    }
    else if ((argc > 2 && !isSilentP) || (argc > 3 && isSilentP)) {
        kodPowrotu = 13;
    }

    if (!isSilentP) {
        cout << kodPowrotu << endl;
    }
    return kodPowrotu;
}
