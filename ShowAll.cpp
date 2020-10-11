#include <iostream>

int main(int argc, char* argv[], char* env[])
{
	puts("Arguments:");

	for (int k = 0; k < argc; k++)
	{
		puts(argv[k]);
	}
	puts("Environment variables:");

	while (*env != NULL)
	{
		puts(*env++);
	}
	return 0;
}
