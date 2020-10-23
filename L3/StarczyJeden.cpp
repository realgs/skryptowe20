
#include "pch.h"
#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
void contains(int argc, char *argv[], char *env[]) {
	string line;
	bool shown;

	while (getline(cin, line))
	{
		shown = false;
		for (int i = 1; i < argc; i++)
		{
			if (line.find(argv[i]) != std::string::npos) {
				shown = true;
				break;
			}
		}
		if (shown)
			cout << line << endl;
	}
}
int main(int argc, char *argv[], char *env[])
{
	contains(argc, argv, env);
	return 0;
}