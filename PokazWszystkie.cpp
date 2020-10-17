#include <iostream>

using namespace std;

int main(int argc, char *argv[], char *env[])
{
    for (int i = 0; env[i] != NULL; i++)
    {
        cout << env[i] << endl;
    }

    cout << endl;

    for (int i = 1; i < argc; i++)
    {
        cout << argv[i] << endl;
    }
}

