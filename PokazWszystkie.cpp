#include <iostream>

using std::cout;
using std::endl;
int main(int argc, char* argv[], char **envp) {
    cout << "Argumenty programu: " << endl;
    for (int i = 1; i < argc; i++) {
        cout << argv[i] << endl;
    }

    cout << "Zmienne środowiskowe: " << endl;
    while (*envp) {
        cout << *envp++ << endl;
    }

    return 0;
}