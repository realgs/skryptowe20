#pragma once
#include<iostream>
using namespace std;

#define MAX_TEXT_LENGTH 500

int readStdInToCharArray(char** text)
{
    int textSize = 0;

    while (!cin.eof()) {
        cin >> noskipws >> (*text)[textSize];
        textSize++;
    }
    return textSize;
}

void printLine(int paramNumber, char** paramsList, string line)
{
    bool isPrinted = false;

    for (int i = 1; i < paramNumber && !isPrinted; i++)
    {
        string paramToPrint(paramsList[i]);

        int pos = 0;
        string param;
        string line_copy(line);
        string delimiter = "\t";
        
        while ((pos = line_copy.find(delimiter)) >= 0)
        {
            param = line_copy.substr(0, pos);
            if (!param.compare(paramToPrint))
            {
                cout << endl << line << endl;
                isPrinted = true;
            }
            line_copy.erase(0, pos + delimiter.length());
        }
    }
}
int main(int argc, char** argv, char** env)
{
    char* text = new char[MAX_TEXT_LENGTH];
    int text_size = readStdInToCharArray(&text);
    
    string text_s(text);

    int pos = 0;
    string line;
    string delimiter = "\n";
    while ((pos = text_s.find(delimiter)) != string::npos)
    {
        line = text_s.substr(0, pos);
        printLine(argc, argv, string(line));
        text_s.erase(0, pos+delimiter.length());
    }
}