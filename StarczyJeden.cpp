#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<string> getParameters(int argc, char *argv[]);
bool isParameterPartOfLine(vector<string> parameters, string line);

int main(int argc, char *argv[])
{
    if (argc == 1)
    {
        return 0;
    }

    vector<string> parameters = getParameters(argc, argv);

    if (parameters.size() > 0)
    {
        string line;
        while (getline(cin, line))
        {
            if (isParameterPartOfLine(parameters, line))
            {
                cout << line << endl;
            }
        }
    }

    return 0;
}

vector<string> getParameters(int argc, char *argv[])
{
    vector<string> parameters;

    for (int i = 1; i < argc; i++)
    {
        parameters.push_back(argv[i]);
    }

    return parameters;
}

bool isParameterPartOfLine(vector<string> parameters, string line)
{
    for (string parameter : parameters)
    {
        if (line.find(parameter) != string::npos)
        {
            return true;
        }
    }

    return false;
}
