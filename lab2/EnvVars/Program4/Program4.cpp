#include <iostream>
#include <string>
#include <direct.h> // _getcwd
using namespace std;

void PrintReturnCodeMessage(int code, const char* param)
{
    switch (code)
    {
        case 11:
            cout << "ii. Brak parametrow" << endl;
            break;
        case 12:
            cout << "iii. Parametr " << param << " nie jest cyfra" << endl;
            break;
        // Podpunkt zdefiniowany tak ze wypisac mamy 1 z parametrow, chociaz kod 13 oznacza ze liczba parametrow przekracza 1...
        case 13:
            cout << "iv. Niewlasciwa wartosc parametru " << param << endl;
            break;
        default:
            cout << "Przekazano: " << param << endl;
            break;
    }
}

void TransformParamsToString(char** argv, string& out)
{
    argv++; // Skip filename
    while (*argv != NULL)
    {
        out += string(*argv++) + " ";
    }
}

int main(int argc, char** argv)
{
    char buffer[129] = { 0 };
    _getcwd(buffer, 128);

    string current_path(buffer);
    string custom_path;
    int return_code;
    string params = " ";

    TransformParamsToString(argv, params);

    cout << "Specify \"KodPowrotu.exe\" path (Press ENTER for default): ";
    getline(cin, custom_path);

    if (custom_path.length() == 0)
    {
        string exec_path = current_path + "\\..\\Debug\\KodPowrotu.exe";
        return_code = system((exec_path + params).c_str());
    }
    else
    {
        return_code = system((current_path + params).c_str());
    }

    PrintReturnCodeMessage(return_code, *++argv);
    return 0;
}