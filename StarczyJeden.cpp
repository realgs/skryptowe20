#include <iostream>
#include <string>

using namespace std;
int main(int argc, char* argv[])
{
	string line;
	bool include = false;

	while (getline(cin, line))
	{
		for (int i = 1; i < argc; i++)
		{
			if (line.find(argv[i]) != string::npos)	include = true;
		}
		
		if (include)
		{
			cout << line << endl;
			include = false;
		}
	}

	return 0;
}
