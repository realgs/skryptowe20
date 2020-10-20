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

void printSelectedColumns(int columnsNumber, char** columnsIDs, char* line)
{
    int current_column_id = 0;

    for (int i = 1; i < columnsNumber; i++)
    {
        for (int j = 0; j < strlen(line); j++)
        {
            if (line[j] == '\t')
                current_column_id++;
            else if (current_column_id == atoi(columnsIDs[i]))
                cout << line[j];
        }
        current_column_id = 0;
        cout << '\t';
    }
    cout << endl;
    
}
int main(int argc, char** argv, char** env)
{
    char* text = new char[MAX_TEXT_LENGTH];
    int text_size = readStdInToCharArray(&text);
    char* line = strtok(text, "\n");
    while (line != NULL)
    {
        printSelectedColumns(argc, argv, line);
        line = strtok(NULL, "\n");
    }
    
    delete[] text;
}
