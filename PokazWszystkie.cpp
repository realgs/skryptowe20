#include <iostream>
using namespace std;
int main(int argc, char* argv[], char* env[])
{

    cout << "ZMIENNE ŚRODOWISKOWE : \n";
    system("set");
    cout << "PARAMETRY PROGRAMU : \n";
    for (int i = 0; i < argc; i++) {
        cout << argv[i] << endl;
    }
}