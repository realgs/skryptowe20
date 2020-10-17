#include <string>
#include <iostream>
#include <stdio.h>
#include <cstring>
#include <set>

using namespace std;

int findMatchingVariable(char *env[], const string &element);
void printOneEnvVariable(char *tokenNametokenName);

int main(int argc, char *argv[], char *env[])
{
    bool isSilenced = false;
    set<string> uniqueArgs;
    for (int i = 1; i < argc; i++)
    {
        string buf(argv[i]);
        if (strcmp(argv[i], "/S") && strcmp(argv[i], "/s"))
        {
            uniqueArgs.insert(buf);
        }
        else
        {
            isSilenced = true;
        }
    }

    for (const string &element : uniqueArgs)
    {
        if (findMatchingVariable(env, element) == 0 && !isSilenced)
        {
            cout << element << " = NONE\n\n";
        }
    }
    return 0;
}

int findMatchingVariable(char **env, const string &element)
{
    int bufCounter = 0;

    while (*env != NULL)
    {
        char *env_duplicate = strdup(*env);
        char *token = strtok(env_duplicate, "=");
        if (strstr(token, element.c_str()))
        {
            printOneEnvVariable(token);
            bufCounter++;
        }
        env++;
        delete env_duplicate;
    }
    return bufCounter;
}

void printOneEnvVariable(char *token)
{
    cout << token << "\n=\n";
    token = strtok(NULL, ";");
    while (token != NULL)
    {
        cout << token << "\n";
        token = strtok(NULL, ";");
    }
    cout << "\n";
}
 