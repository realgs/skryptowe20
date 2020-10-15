#include "pch.h"
#include <iostream>

int main(int argc, char* argv[], char* env[])
{
	puts("Argumenty programu: ");
	for (int i = 0; i < argc; i++)
		puts(argv[i]);
	puts("Zmienne srodowiska: ");
	while (*env != NULL)
		puts(*env++);
	return 10;
}


