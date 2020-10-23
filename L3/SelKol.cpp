#include <iostream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;

void selectedColumns(int argc, char* argv[]) 
{
    string line;
    vector<int> columns;

    for (int i = 1; i < argc; i++) {
        columns.push_back(atoi(argv[i]));
    }

    while (getline(cin, line))
    {
        vector<string> parts;
        istringstream isstream(line);
        string part;
        while (getline(isstream, part, '\t')) parts.push_back(part);

        for (int i = 0; i < columns.size(); i++) {
            if (columns[i] - 1 < parts.size())
                cout << parts[columns[i] - 1] << '\t';
        }
        cout << endl;
    }
}
int main(int argc, char* argv[], char* env[])
{
    selectedColumns(argc, argv);
    return 0;
}
