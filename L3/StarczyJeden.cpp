
#include <iostream>
#include "string"
using namespace std;

int main(int argc, char* argv[])
{
	string text;

	getline(cin, text);
	while (text != "")
	{
		for (int i = 1; i < argc; i++)
		{
			if (text.find(argv[i]) != string::npos)
			{
				cout << text << "\n";
				i = argc;
			}
		}

		if (!cin.eof())
			getline(cin, text);
		else
			text = "";
	}

	return 0;
}
