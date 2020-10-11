#include <iostream>
#include <string>
#include <vector>
using namespace std;

void Split(const string& input, const char delimiter, vector<string>& result)
{
    size_t last_offset = 0;
    size_t new_offset = input.find(delimiter, last_offset);

    while (new_offset != string::npos)
    {
        string sub = input.substr(last_offset, new_offset);
        result.push_back(sub);
        last_offset = new_offset + 1;

        new_offset = input.find(delimiter, last_offset);
    }
    result.push_back(input.substr(last_offset, result.size() - 1 - last_offset));
}

void PrintVar(const string& var)
{
    const char content_entries_delimiter = ';';
    const char name_content_delimiter = '=';

    vector<string> name_content_vector;
    Split(string(var), name_content_delimiter, name_content_vector);

    string var_name = name_content_vector[0];
    string content = name_content_vector[1];

    vector<string> all_content_entries;
    Split(content, content_entries_delimiter, all_content_entries);

    cout << "i. " << var_name << endl;
    cout << "ii. =" << endl;

    for (const string& entry : all_content_entries)
    {
        cout << "iii. " << entry << endl;
    }

    cout << endl;
}

int main(int argc, char** argv, char** env)
{
    bool is_silent = strcmp(argv[1], "/S") == 0 || strcmp(argv[1], "/s") == 0;

    argv++; // Skip filename;

    if (is_silent)
    {
        argv++;
    }

    while (*argv != NULL)
    {
        char** env_copy = env;
        bool found_one = false;
        const char* arg = *argv;

        while (*env_copy != NULL)
        {
            string var(*env_copy++);

            if (var.find(arg) != string::npos)
            {
                found_one = true;
                PrintVar(var);
            }
        }

        if (!found_one && !is_silent)
        {
            cout << arg << " = NONE" << endl;
        }

        argv++;
    }
}