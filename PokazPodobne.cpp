#include <regex>
#include <string>
#include<iostream>
using namespace std;
int main(int argc, char* argv[], char* env[])
{

    regex findingVariables;
    vector<string> variables;
    bool silentMode = false;
    for (int i = 1; i < argc; i++) {
        int counter = 0;
        findingVariables = argv[i];
        while (env[counter] != NULL) {
            if (env[counter] == "/s" || env[counter] == "/S")
                silentMode = true;
            if (regex_search(env[counter], findingVariables)) {
                variables.push_back(env[counter]);
            }
            counter++;
        }
    }
    if (variables.size() == 0 && silentMode == false) {
        for (int i = 1; i < argc; i++) {
            cout << argv[i] << " = " << "NONE \n";
        }

        return 0;
    }
    for (int i = 0; i < variables.size(); i++) {
        string temp(variables[i]);
        temp.append(";");
        int sign_pos = temp.find('=');
        cout << temp.substr(0, sign_pos) << endl << '=' << endl;
        do
        {
            int semicolnPos = temp.find(';');
            cout << temp.substr(0, semicolnPos) << endl;
            temp = temp.substr(semicolnPos + 1);

        } while (temp.find(';') != -1);
    }
}