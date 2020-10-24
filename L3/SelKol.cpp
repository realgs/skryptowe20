
#include <iostream>
#include "string"
#include <vector>
using namespace std;

#define ARG_NOT_NUMBER 1;
#define COLUMN_NOT_FIND "null";


int main(int argc, char* argv[])
{
	int* ColNums = new int[argc - 1];
	for (int i = 1; i < argc; i++)
	{
		int tempNum = 0;
		for (int j = 0; argv[i][j] != NULL; j++)
		{
			if (argv[i][j] >= '0' && argv[i][j] <= '9')
			{
				tempNum *= 10;
				tempNum += argv[i][j] - '0';
			}
			else
				return ARG_NOT_NUMBER;
		}
		ColNums[i-1] = tempNum;
	}

	string output_text = "";

	string text;
	
	getline(cin, text);
	while (text!="")
	{
		if(output_text!="")
			output_text += "\n";

		int start = 0;
		int finish;
		vector<string> cols;
		while (text.find("\t", start) != string::npos)
		{
			finish = text.find("\t", start);
			cols.push_back(text.substr(start, finish - start));
			start = finish + 1;
		}

		cols.push_back(text.substr(start));


		for (int i = 0; i < argc - 1; i++)
		{
			if (i > 0)
			{
				output_text += "\t";
			}
			if (ColNums[i] < cols.size())
			{
				output_text += cols[ColNums[i]];
			}
			else
			{
				output_text += COLUMN_NOT_FIND;
			}
		}

		if (!cin.eof())
			getline(cin, text);
		else
			text = "";
	}
		

	cout << output_text;

	delete ColNums;
	return 0;
}


