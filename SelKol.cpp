// Skryptowe_lab3.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
int main(int argc, char* argv[], char* env[])
{

    string word;
    string line;
    int numberOfColumns = 4;
    string row[4];
    int* parameters = new int[argc];
    for (int i = 1; i < argc; i++) {
        parameters[i] = argv[i][0] - 48;
    }

    while (getline(cin, line)) {
        istringstream iss(line);
        for (int i = 0; i < numberOfColumns; i++) {
            iss >> word;
            row[i] = word;
        }

        for (int i = 1; i < argc; i++) {
            cout << row[parameters[i] - 1] << "\t";
        }
        cout << endl;
    }

}
