#include <iostream>

using namespace std;

int main(int argc, char* argv[], char** envp)
{
	// Environmental variables
	int index = 0;
	while (envp[index] != 0)
	{
		cout << envp[index] << endl;
		index++;
	}

	// Program params
	for (int i = 0; i < argc; i++)
	{
		cout << argv[i] << endl;
	}

	return 0;
}