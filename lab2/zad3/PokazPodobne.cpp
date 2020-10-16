#include <iostream>
#include <string>
#include <vector>
#include <functional>
#include <iostream>

using namespace std;

const string ENV_VALUE_SEPARATOR = ";";
const string NONE_VALUE_MESSAGE = "NONE";
const string SILENT_SIGN_LOWER = "/s";
const string SILENT_SIGN_UPPER = "/S";
const string WRONG_ARGUMENT_MESSAGE = "Please specify search argument !";


void printAllVariableValues(string variableValue, string searchValue) {
    int semicolonSignIndex = variableValue.find(ENV_VALUE_SEPARATOR);
    if (semicolonSignIndex != -1) {
        string firstValue = variableValue.substr(0, semicolonSignIndex);
        string otherValues = variableValue.substr(semicolonSignIndex + 1, variableValue.length());
        if (firstValue.find(searchValue) != -1) {
            cout << firstValue << endl;
        }
        printAllVariableValues(otherValues, searchValue);
    } else {
        if (variableValue.find(searchValue) != -1) {
            cout << variableValue << endl;
        }
    }
}

void printVariable(string variable, string searchValue, bool isSilentModeEnabled) {
    int equalSignIndex = variable.find("=");
    string variableName = variable.substr(0, equalSignIndex);
    string variableValue = variable.substr(equalSignIndex + 1, variable.length() - 1);
    if (variableValue.find(searchValue) != -1) {
        cout << variableName << endl << "=" << endl;
        if (variableValue.find(ENV_VALUE_SEPARATOR) == -1) {
            cout << variableValue << endl;
        } else {
            printAllVariableValues(variableValue, searchValue);
        }
    } else if (!isSilentModeEnabled) {
        cout << variableName << " = " << NONE_VALUE_MESSAGE << endl;
    }
}

bool checkIfIsSilentModeEnabled(int argc, char *argv[]) {
    if (argc > 2) {
        string secondArgument = argv[2];
        if (secondArgument == SILENT_SIGN_UPPER || secondArgument == SILENT_SIGN_LOWER) {
            return true;
        }
    }
    return false;
}

int main(int argc, char *argv[], char *env[]) {
    if (argc > 1) {
        string searchValue = argv[1];
        bool isSilentModeEnabled = checkIfIsSilentModeEnabled(argc, argv);
        for (char **currentEnv = env; *currentEnv != 0; currentEnv++) {
            string env = *currentEnv;
            printVariable(env, searchValue, isSilentModeEnabled);
        }
    } else {
        cout << WRONG_ARGUMENT_MESSAGE << endl;
        return 11;
    }
}


