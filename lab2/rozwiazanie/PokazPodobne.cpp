#include <stdio.h>
#include <string.h>
#include "iostream"
#include <bits/stdc++.h>
#include <algorithm>
#include <cctype>
#include <string>
using namespace std;

bool silentMode = false;
char asciitolower(char in) {
    if (in <= 'Z' && in >= 'A')
        return in - ('Z' - 'z');
    return in;
}
bool containsName(string name, string substring)
{
    std::transform(name.begin(), name.end(), name.begin(), asciitolower);
    std::transform(substring.begin(), substring.end(), substring.begin(), asciitolower);
    if (name.find(substring) != string::npos)
        return true;
    return false;
    return true;
}

bool isSilentSwitch(char arg[])
{
    if((string)arg == "/s" || (string)arg == "/S")
        return true;
    return false;
}

vector <string> split(string line, char separator)
{
    vector <string> tokens;
    stringstream strstream(line);
    string intermediate;

    while(getline(strstream, intermediate, separator))
    {
        tokens.push_back(intermediate);
    }
    return tokens;
}


int main(int argc, char *argv[], char **envp)
{
    for(int i = 1; i < argc; i++)
    {
        if(isSilentSwitch(argv[i]))
        {
            silentMode = true;
            break;
        }
    }

    vector<pair<string, vector<string> > > envVariables;
    for (char **env = envp; *env != 0; env++)
    {
        vector<string> envVariable = split(*env, '=');
        envVariables.push_back(make_pair(envVariable[0], split( envVariable[1], ';')));
    }

    if(!silentMode)
    {
        for(int i = 1; i < argc; i++)
        {
            bool variableContainsParam = false;
            for(int y = 0; y < envVariables.size(); y++)
            {
                if(containsName(envVariables[y].first, (string)argv[i]))
                {
                    variableContainsParam = true;
                    break;
                }
            }
            if(!variableContainsParam)
            {
                cout<<argv[i]<<"=NONE"<<endl<<endl;
            }
        }
    }

    for(int i = 0; i < envVariables.size(); i++)
    {
        if(argc == 1)
        {
            cout<<envVariables[i].first<<endl;
            cout<<'='<<endl;
            for(int z = 0; z < envVariables[i].second.size(); z++)
                    cout<<envVariables[i].second[z]<<endl;
            cout << endl;
        }
        else
        {
            for(int y = 1; y < argc; y++)
            {
                if(containsName(envVariables[i].first, (string)argv[y]))
                {
                    cout<<envVariables[i].first<<endl;
                    cout<<'='<<endl;
                    for(int z = 0; z < envVariables[i].second.size(); z++)
                        cout<<envVariables[i].second[z]<<endl;
                    cout << endl;
                    break;
                }
            }
        }

    }

}

