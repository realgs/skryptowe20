#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;
int main(int argc, char* argv[])
{

    if (argc > 5) return 11;
    for (int i = 1; i < argc; i++)
    {
        if (atoi(argv[i]) > 4) return 12;
    }

    vector<int> selCol;
    for (int i = 1; i < argc; i++)
    {
        selCol.push_back(atoi(argv[i]));
    }

    ifstream source;
    source.open("Zakup.txt");
    vector<string> lines;
    string line;
    while (getline(source, line))
    {
        stringstream ss(line);
        string token;
        vector<string> tokens;
        while (getline(ss, token, '\t')) {
            tokens.push_back(token);
        }
        for (int i = 0; i < static_cast<int>(selCol.size()); i++)
        {
            int k = selCol[i];
            cout << tokens[k-1] << "\t";
        }
        cout << endl;
    }

    return 0;
}

