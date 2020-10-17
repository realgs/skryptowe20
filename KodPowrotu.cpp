

#include <iostream>
#include <cstdlib>
#include <vector>
#include <regex>
#include <string>
using namespace std;
int main(int argc, char* argv[], char* env[])
{

    bool isDigit = false;
    int returnCode;
    bool silentMode = false;
    vector<string> parameters;

    for (int i = 1; i < argc; i++) {
        if ((string)argv[i] == "\s" || (string)argv[i] == "/S") 
            silentMode = true;
        else
            parameters.push_back(argv[i]);
    }


    if (parameters.size() == 1) {
        string temp(parameters[0]);
        if ((int)temp[0] >= 48 && (int)temp[0] <= 57 && temp.length() == 1)
        {
            isDigit = true;
            returnCode = temp[0] - 48;

        }

    }

    if (parameters.size() == 0)
        returnCode = 11;
    else if (parameters.size() >= 2)
        returnCode = 13;
    else if (!isDigit)
        returnCode = 12;


    if (!silentMode)
        cout << returnCode << endl;
    return returnCode;

}
