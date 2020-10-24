#include <iostream>
#include <vector>
#include <sstream>

using namespace std;

vector<string> split(const string& str, char delim = '\t')
{
    vector<string> tokens;
    stringstream ss(str);
    string token;
    while (getline(ss, token, delim))
    {
        tokens.push_back(token);
    }
    return tokens;
}

int main()
{
    string textLine;
    double sum = 0.0;
    double value;
    while (cin >> textLine)
    {
        vector<string> splitedLine = split(textLine);
        for (int i = 0; i < splitedLine.size(); i++)
        {
            try
            {
                value = stod(splitedLine[i]);
                sum += value;
            }
            catch (exception e)
            {
            }
        }
    }
    cout << sum;
    return 0;
}
