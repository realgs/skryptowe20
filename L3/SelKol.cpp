
#include "pch.h"
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;
void chooseColumns(int argc, char *argv[], char *env[])
{
	string line;
	vector<int> chosen_Columns;

	for (int i = 1; i < argc; i++)
		chosen_Columns.push_back(atoi(argv[i]));

	while (getline(cin, line))
	{
		vector<string> tokens;
		istringstream iss(line);
		string one_token;
		while (getline(iss, one_token, '\t'))
			tokens.push_back(one_token);

		for (int i = 0; i < chosen_Columns.size(); i++)
			cout << tokens[chosen_Columns[i] - 1] << '\t';
		cout << endl;
	}
}

int main(int argc, char *argv[], char *env[])
{
	chooseColumns(argc, argv, env);
	return 0;
}

