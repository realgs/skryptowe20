#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[])
{
    string textLine;
    while (getline(cin, textLine))
    {
        for (int i = 1; i < argc; i++)
        {
            size_t found = textLine.find(argv[i]);
            if (found != string::npos)
            {
                cout << textLine << endl;
                break;
            }
        }
    }
}
