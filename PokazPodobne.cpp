#include <iostream>
#include <cstring>
#include <vector>
#include <sstream>

using namespace std;

bool isSilenceArgument(char argument[]);
vector<string> splitStringBySign(string envVariable, char sign);
bool isAnyArgumentPartOfEnvVariableName(vector<string> passedArguments, string envVariableName);
void displayFoundEnvVariable(string envVariableName, vector<string> splittedEnvContent);

int main(int argc, char *argv[], char *env[])
{
    bool isSilent = false;
    bool isMatchingVariableFound = false;
    int firstArgumentIndex = 1;

    if (argc > 1)
    {
        if (isSilenceArgument(argv[1]))
        {
            isSilent = true;
            firstArgumentIndex++;
        }
    }

    if (firstArgumentIndex < argc)
    {
        vector<string> passedArguments;
        for (int i = firstArgumentIndex; i < argc; i++)
        {
            passedArguments.push_back(string(argv[i]));
        }

        for (int envVariableIndex = 0; env[envVariableIndex] != NULL; envVariableIndex++)
        {
            string envVariable(env[envVariableIndex]);
            vector<string> splittedEnvVariable = splitStringBySign(envVariable, '=');

            string envVariableName = splittedEnvVariable.front();

            if (isAnyArgumentPartOfEnvVariableName(passedArguments, envVariableName))
            {
                isMatchingVariableFound = true;
                vector<string> splittedEnvContent = splitStringBySign(splittedEnvVariable.back(), ';');

                displayFoundEnvVariable(envVariableName, splittedEnvContent);
            }
        }
    }

    if (!isSilent && !isMatchingVariableFound)
    {
        cout << "parametr=NONE" << endl;
    }
}

bool isSilenceArgument(char argument[])
{
    if (strcmp(argument, "/s") == 0 || strcmp(argument, "/S") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool isAnyArgumentPartOfEnvVariableName(vector<string> passedArguments, string envVariableName)
{
    for (string argument : passedArguments)
    {
        if (envVariableName.find(argument) != string::npos)
        {
            return true;
        }
    }

    return false;
}

vector<string> splitStringBySign(string stringToSplit, char sign)
{
    vector<string> splittedStringVector;

    stringstream ss(stringToSplit);
    string tmpValueHolder;

    while (getline(ss, tmpValueHolder, sign))
    {
        splittedStringVector.push_back(tmpValueHolder);
    }

    return splittedStringVector;
}

void displayFoundEnvVariable(string envVariableName, vector<string> splittedEnvContent)
{
    cout << envVariableName << endl;
    cout << "=" << endl;

    for (string envContent : splittedEnvContent)
    {
        cout << envContent << endl;
    }

    cout << endl;
}

