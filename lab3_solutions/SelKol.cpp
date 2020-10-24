#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

#define COLUMNS_SEPARATOR '\t'

void readColumns(vector<vector<string>>* separatedColumns, int* numberOfLines) {
	string input;
	string singleColumn;

	while (getline(cin, input)) {
		stringstream columns(input);
		vector<string> line;

		while (getline(columns, singleColumn, COLUMNS_SEPARATOR)) {
			line.push_back(singleColumn);
		}
		separatedColumns->push_back(line);
		(*numberOfLines)++;
	}
}

void printSelectedColumns(vector<vector<string>>* separatedColumns, int numbersOfLines, char* argv[], int argc) {
	int index;
	for (int i = 0; i < numbersOfLines; i++) {
		for (int j = 1; j < argc; j++) {
			index = atoi(argv[j]);
			if (index < (*separatedColumns)[i].size()) cout << (*separatedColumns)[i][index] << COLUMNS_SEPARATOR;
		}
		cout << endl;
	}
}

int main(int argc, char* argv[])
{
	vector<vector<string>> separatedColumns;
	int numbersOfLines = 0;
	readColumns(&separatedColumns, &numbersOfLines);
	printSelectedColumns(&separatedColumns, numbersOfLines, argv, argc);
}
