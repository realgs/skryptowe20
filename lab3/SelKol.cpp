#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

vector<string> split(const string& str, char delim = '\t')
{
	vector<string> tokens;
	stringstream ss(str);
	string token;
	while (getline(ss, token, delim))
	{
		tokens.push_back(token);
	}
	return tokens;
}


int main(int argc, char* argv[])
{
	vector<int> columnParameters;
	int numberOfParameters = 0;
	for (int i = 1; i < argc; i++)
	{
		columnParameters.push_back(atoi(argv[i]));
		numberOfParameters++;
	}

	string textLine;
	string data[4];
	while (getline(cin, textLine))
	{
		vector<string> splitedLine = split(textLine);
		for (int i = 0; i < numberOfParameters; i++) {
			cout << splitedLine[columnParameters[i] - 1] << "\t";
		}
		cout << endl;
	}
}
