#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
void findInLine(int argc, char* argv[]) 
{
    string lines;
    bool found;

    while (getline(cin, lines))
    {
        found = false;
        for (int i = 1; i < argc; i++)
        {
            if (lines.find(argv[i]) != string::npos)
            {
                found = true;
                break;
            }
        }
        if (found) cout << lines << endl;
    }
}
int main(int argc, char* argv[], char* env[])
{
    findInLine(argc, argv);
    return 0;
}
