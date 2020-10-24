#include <iostream>
#include <vector>
#include <string>
#include <sstream>

using namespace std;

vector<int> getColumnNumbersFromParameters(int argc, char *argv[]);
vector<string> splitStringBySign(string stringToSplit, char sign);

int main(int argc, char *argv[])
{
    if (argc == 1)
    {
        return 0;
    }

    vector<int> columnNumbers = getColumnNumbersFromParameters(argc, argv);

    if (columnNumbers.size() > 0)
    {
        string line;

        while (getline(cin, line))
        {
            vector<string> row = splitStringBySign(line, '\t');

            for (int column : columnNumbers)
            {
                cout << row.at(column) << '\t';
            }

            cout << endl;
        }
    }

    return 0;
}

vector<int> getColumnNumbersFromParameters(int argc, char *argv[])
{
    const int NUMBER_OF_COLUMNS = 4;
    vector<int> columnNumbers;

    for (int i = 1; i < argc; i++)
    {
        try
        {
            int parameter = stoi(argv[i]);
            if (parameter >= 0 && parameter < NUMBER_OF_COLUMNS)
            {
                columnNumbers.push_back(parameter);
            }
        }
        catch (exception &err)
        {
        }
    }

    return columnNumbers;
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
