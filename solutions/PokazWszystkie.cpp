#include <iostream>
using namespace std;

int main(int argc, char* argv[], char* env[])
{
    cout << "Environmental variables: " << endl;
    while (*env != NULL)
    {
        cout << *env++ << endl;
    }
    cout << "Program parameters: " << endl;
    for (int i=0; i < argc; i++)
    {
        cout << argv[i] << endl;
    }
}