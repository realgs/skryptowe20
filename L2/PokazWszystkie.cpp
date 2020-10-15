
#include <iostream>

int main(int argc, char* argv[], char** env)
{
	puts("Parametry programu:");
	for (int k = 0; k < argc; k++) puts(argv[k]);
	puts("Zmienne środowiska:");
	while (*env != NULL) puts(*env++);
	return 10;
}

