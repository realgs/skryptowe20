#include <iostream>
#include <string>
#include <fstream>
#include <vector>

using namespace std;

const string FILE_NAME = "Zakupy.txt";

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

int main(int argc, char** argv)
{
    argv++; // Skip filename

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
                char** argvCopy = argv;

                while (*argvCopy)
                {
                    if (product.find(*argvCopy++) != string::npos)
                    {
                        cout << product << endl;
                    }
                }                
            }
        }
        stream.close();
    }
}