#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
int main(int argc, char *argv[], char *env[])
{
    string line;
    bool display;

    while(getline(cin, line))
    {
        display = false;
        for (int k = 1; k < argc; k++)
        {
            if (line.find(argv[k]) != std::string::npos) {
                display = true;
                break;
            }
        }
        if (display)
            cout << line << endl;
    }
    return 0;
}
