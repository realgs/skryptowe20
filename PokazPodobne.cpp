#include <iostream>
#include <string>


const char SEPARATOR = '=';
const char DELIMITER = ';';

using namespace std;

void printResult(string &name, string &desc) {
    cout << "i. " << name << endl;
    cout << "ii. =" << endl;
    if (desc.find(DELIMITER) != string::npos) {
        size_t index;
        while (desc.find(DELIMITER) != string::npos) {
            index = desc.find(DELIMITER);
            cout << "iii. " << desc.substr(0, index) << endl;
            desc.erase(0, index+1);
        }
    }
    cout << "iii. " << desc << endl;
}

int main(int argc, char* argv[], char **envp) {
    bool silent_mode = false;
    for (int i = 0; i < argc; i++) {
        string str = argv[i];
        if (str.compare("/s") == 0 || str.compare("/S") == 0) {
            silent_mode = true;
        } 
    }
    bool found;

    for (int i = 1; i < argc; i++) {
        found = false;
        string delim = argv[i];
        if (delim == "/S" || delim == "/s") continue;
        char **envVariables = envp;
        while (*envVariables) {
            string envVar(*envVariables++);
            size_t splitInd = envVar.find(SEPARATOR);
            string name = envVar.substr(0, splitInd);
            envVar.erase(0, splitInd + 1);
            if (name.find(delim) != string::npos) {
                found = true;
                printResult(name, envVar);
            }
        }
        if (!found && !silent_mode) {
            cout << "parametr = NONE" << endl;
        }
    }
    return 0;
}