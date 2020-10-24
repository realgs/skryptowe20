#include <iostream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;

vector<int> getSelectedColumn(int argc, char* argv[])
{
    vector<int> columns;
    int col = 0;
    for (int i = 1; i < argc; i++){
        col = atoi(argv[i]);
        if(col>0)columns.push_back(col);
    }
    return columns;
}

void showSelectedColumns(int argc, char* argv[])
{
    string line;
    vector<int> columns = getSelectedColumn(argc, argv);
    vector<string> elements;
    string elem;

    while (getline(cin, line))
    {
        elements.clear();
        istringstream isstream(line);
        while (getline(isstream, elem, '\t')) elements.push_back(elem);
        for (int i = 0; i < columns.size(); i++) {
            if (columns[i] - 1 < elements.size())
                cout << elements[columns[i] - 1] << '\t';
        }
        cout << endl;
    }
}

int main(int argc, char* argv[])
{
    showSelectedColumns(argc, argv);
    return 0;
}
