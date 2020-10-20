/*#define _CRT_SECURE_NO_WARNINGS
#include<iostream>
using namespace std;
#define MAX_INPUT_LENGTH 500

int readStdInToCharArray(char** text)
{
    int textSize = 0;

    while (!cin.eof()) {
        cin >> noskipws >> (*text)[textSize];
        textSize++;
    }
    return textSize;
}

int main(int argc, char** argv)
{
	char* text = new char[MAX_INPUT_LENGTH];
    int text_size = readStdInToCharArray(&text);
    char* input_string = strtok(text, " \n\t");
    double sum = 0;
    while (input_string != NULL)
    {
        cout << input_string <<endl;
        double number = atof(input_string);
        if (number != 0)
            sum += number;
        input_string = strtok(NULL, " \n\t");
    }
    cout << "\nSum: " << sum;
}*/
