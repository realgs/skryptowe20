#include <iostream>

using namespace std;

int main(int argc, char** argv, char** envp) {
    cout << "argv:" << endl;
    for( int i = 0; i < argc; i++) {
        cout << i << ": " << argv[i] << endl;
    }
    cout << "\nenvp:" << endl;
    for( int i = 0; envp[i] != nullptr; ++i ) {
        cout << i << ": " << envp[i] << endl;
    }
}