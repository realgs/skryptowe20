#include "zad1.h"

#include <iostream>
using namespace std;

int main(int argc, char* argv[]) {
    int ret;
    bool silent = false;
    if (argc == 1) 
    {
        ret = 11;
    }
    else {
        if (string(argv[1]) == "/s" || string(argv[1]) == "/S") silent = true;
        if (silent && argc == 2) ret = 11;
        else {
            if ((argc > 2 && !silent) || (argc > 3 && silent)) ret = 13;
            else {
                if (string(argv[argc - 1]).length()==1 && "0"<=string(argv[argc - 1]) 
                                                    && string(argv[argc - 1]) <= "9") ret = atoi(argv[argc - 1]);
                else ret = 12;
            }
        }
    }
    if (!silent) cout << ret;
    return ret;
}
