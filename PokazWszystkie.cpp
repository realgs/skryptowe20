#include <iostream>

using namespace std;

int main(int argc, char *argv[], char* env[])
{
    int exitCode = 11;
    
    while (*env != NULL)
        cout << *env++ << endl;

    for(int i = 0; i < argc; i++)
    {
        cout << argv[i] << endl;
    }

    return 0;
}
 