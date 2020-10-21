#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
int main(int argc, char *argv[], char *env[])
{
    string line;
    vector<int> selected_columns;

    for (int k = 1; k < argc; k++)
        selected_columns.push_back(atoi(argv[k]));

    while(getline(cin, line))
    {
        vector<string> tokens;
        istringstream iss(line);
        string token;
        while(getline(iss, token, '\t'))
            tokens.push_back(token);

        for (int i : selected_columns)
            cout << tokens[i-1] << '\t';
        cout << endl;
    }
    return 0;
}
