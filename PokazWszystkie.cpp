#include <iostream>

int main(int argc, char* argv[], char* env[])
{

	for (int i = 0; i < argc; i++)
	{
		std::cout <<(argv[i]) << "\n";
	}

	while (*env != NULL)
	{
		std::cout << *env++ << "\n";
	}
	return 0;
}