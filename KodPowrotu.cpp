#include <iostream>
#include <stdlib.h>
#include <string>

using namespace std;

int main(int argc, char* argv[])
{
    bool isSilent = false;
    if (argc >= 2)
    {
        for (int i = 1; i < argc; i++) {
            if ((argv[i][0] == '/' && argv[i][1] == 's') ||
                (argv[i][0] == '/' && argv[i][1] == 'S')) {
                isSilent = true;
            }
        }
    }
    int x;
    if (argc == 1) {
        if (!isSilent)
        {
            printf("Kod powrotu: %d\n", 11);
        }
        return 11;
    }
    else if (argc > 2) {
        if (!isSilent)
        {
            printf("Kod powrotu: %d\n", 13);
        }
        return 13;
    }
    try {
        x = stoi(argv[1]);
        if (argv[1][1] != NULL) {
            x = 12;
        }
    }
    catch (exception e) {
        x = 12;
    }
    if (!isSilent) {
        printf("Kod powrotu: %d\n", x);
    }
    return x;
}