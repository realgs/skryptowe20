#include <iostream>
#include <cstring>
#include <string.h>
#include <algorithm>

using namespace std;

bool is_silent_flag(char* arg)
{
    return (string) arg == "/s" || (string) arg == "/S";
}

bool isSilent(int argc, char *argv[])
{  
    for (int i = 0; i < argc; i++)
    {
        if (is_silent_flag(argv[i]))
        {
            return true;
        }
    }
    return false;
}

void print_variable_values(char* variable_values)
{

}

void print_environmental_variables(char* param, char* env[], bool is_in_silent_mode)
{
    bool param_found = false;
    int i = 0;
    while(env[i] != nullptr)
    {
        string env_str (env[i]);
        int string_start = 0;
        int string_end = env_str.find('=');
        string variable_name = env_str.substr(string_start, string_end);
        string value;
        if (variable_name.find(param) != string::npos)
        {
            param_found = true;
            cout << variable_name << endl; 
            cout << "= " << endl;

            while (string_start != string_end && string_end != -1)
            {
                string_start = string_end + 1;
                string_end = env_str.find(';', string_start);
                value = env_str.substr(string_start, string_end - string_start);
                cout << value << endl;
            }

        }
        
        i++;
    }

    if (!param_found && !is_in_silent_mode)
    {
        cout << param << " = NONE" << endl;
    }
}

int main(int argc, char* argv[], char* env[])
{
    bool is_in_silent_mode = isSilent(argc, argv);
    for (int i = 1; i < argc; i++)
    {
        if (!is_silent_flag(argv[i]))
        {
            print_environmental_variables(argv[i], env, is_in_silent_mode);
        }
    }

}