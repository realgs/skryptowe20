#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

int main(int argc, char* argv[])
{
	string data;
	while (getline(cin, data))
	{		
		for (int i = 1; i < argc; i++)
		{
			if (data.find(argv[i]) != string::npos)
			{
				cout << data << endl;
				i = argc;
			}
		}		
	}
}
