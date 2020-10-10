#include <stdio.h>
#include <string.h>
#include "iostream"
#include <bits/stdc++.h>
using namespace std;

bool containsName(string env)
{
    return true;
}

int main(int argc, char *argv[], char **envp)
{
    for (char **env = envp; *env != 0; env++)
    {
    char *thisEnv = *env;
    string tenv = thisEnv;

    vector <string> tokens;
    stringstream check1(tenv);
    string intermediate;

    while(getline(check1, intermediate, '='))
    {
        tokens.push_back(intermediate);
    }

    if(containsName(tokens[0]))
    {
        cout << tokens[0] << endl;
        cout << "=" << endl;

        string oneLine = tokens[1];

        // Vector of string to save tokens
        vector <string> tokens2;

        // stringstream class check1
        stringstream check2(oneLine);

        string intermediate2;

        // Tokenizing w.r.t. space ' '
        while(getline(check2, intermediate2, ';'))
        {
            tokens2.push_back(intermediate2);
        }

        // Printing the token vector
        for(int i = 0; i < tokens2.size(); i++)
            cout << tokens2[i] << '\n';
    }
    cout << endl;
}
}

