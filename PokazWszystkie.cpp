#include <iostream>

int main(int argc, char* argv[], char* env)
{
	puts("Zmienne środowiskowe:");
	while (*env != NULL) puts(*env++);
	puts("Parametry programu:");
	for (int k = 0; k < argc; k++) puts(argv[k]);
	return 10;
}
