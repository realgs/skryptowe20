#include <iostream>

using namespace std;

int main(int argc, char *argv[], char *env[]) {
    cout << "Argumenty:" << endl;
    for (int i = 1; i < argc; i++) {
        cout << i << ".) " << argv[i] << endl;
    }
    cout << "Zmienne srodowisko:" << endl;
    int envCounter = 1;
    for (char **currentEnv = env; *currentEnv != 0; currentEnv++) {
        cout << envCounter << ".) " << *currentEnv << endl;
        envCounter++;
    }
}


