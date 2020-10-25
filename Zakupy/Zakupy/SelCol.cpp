#include <iostream>
#include <string>
#include <fstream>
#include <vector>

using namespace std;

const string FILE_NAME = "Zakupy.txt";
const int COLUMNS_NUMBER = 4;

void Split(const string& input, const char delimiter, vector<string>& out)
{
    size_t last_offset = 0;
    size_t new_offset = input.find(delimiter, last_offset);

    if (!out.empty())
    {
        out.clear();
    }

    while (new_offset != string::npos)
    {
        string sub = input.substr(last_offset, new_offset - last_offset);

        out.push_back(sub);
        last_offset = new_offset + 1;

        new_offset = input.find(delimiter, last_offset);
    }
    out.push_back(input.substr(last_offset, out.size() - 1 - last_offset));
}

bool TryParseInt(const char* val, int& out)
{
    try
    {
        out = stoi(val);
        return true;
    }
    catch (const invalid_argument&)
    {
        return false;
    }
}

int* GetColumns(int argc, char** argv)
{
    if (argc == 0) return NULL;

    int* columns = new int[argc];
    int i = 0;

    while (*argv != NULL)
    {
        if (!TryParseInt(*argv++, columns[i]) || columns[i] > COLUMNS_NUMBER)
        {
            columns[i] = -1;
        }

        ++i;
    }

    return columns;
}

int main(int argc, char** argv)
{
	argv++;
    argc--; // Skip filename

    const int* columns = GetColumns(argc, argv);

	ifstream stream;
    string currentLine;

	stream.open(FILE_NAME);

    if (stream.is_open())
    {
        while (getline(stream, currentLine))
        {
            vector<string> products;
            vector<string> productData;

            Split(currentLine, '\n', products);

            for (const string& product : products)
            {
                Split(product, '\t', productData);

                for (int i = 0; i < argc; i++)
                {
                    if (columns[i] != -1)
                    {
                        cout << productData[columns[i] - 1] << '\t';
                    }
                }

                cout << endl;
            }
        }
        stream.close();
    }

    delete[] columns;
}