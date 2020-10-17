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

void print_variable_values(string env_str, int start_of_string, int end_of_string)
{
    string variable_value;
    while (start_of_string != end_of_string && end_of_string != -1)
    {
        start_of_string = end_of_string + 1;
        end_of_string = env_str.find(';', start_of_string);
        variable_value = env_str.substr(start_of_string, end_of_string - start_of_string);
        cout << variable_value << endl;
    }
}

void print_environmental_variables(char* param, char* env[], bool is_in_silent_mode)
{
    bool param_found = false;
    int i = 0;
    while(env[i] != nullptr)
    {
        string env_str (env[i]);
        int start_of_string = 0;
        int end_of_string = env_str.find('=');
        string variable_name = env_str.substr(start_of_string, end_of_string);
        if (variable_name.find(param) != string::npos)
        {
            param_found = true;
            cout << variable_name << endl; 
            cout << "= " << endl;
            print_variable_values(env_str, start_of_string, end_of_string);
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