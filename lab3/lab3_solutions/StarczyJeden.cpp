/*#pragma once
#include<iostream>
#include<vector>
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

    std::size_t prev = 0, pos;
    vector<string> paramsReadVector;
    while ((pos = line.find_first_of("\t", prev)) != std::string::npos)
    {
        if (pos > prev)
            paramsReadVector.push_back(line.substr(prev, pos - prev));
        prev = pos + 1;
    }
    if (prev < line.length())
        paramsReadVector.push_back(line.substr(prev, std::string::npos));
    
    for (int i = 1; i < paramNumber && !isPrinted; i++)
    {
        string paramToPrint(paramsList[i]);

        for (string param : paramsReadVector) {
            if (!param.compare(paramToPrint))
            {
                cout << endl << line << endl;
                isPrinted = true;
            }
        }

    }
}
int main(int argc, char** argv)
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
}*/