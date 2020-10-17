#include <iostream>

int main(int argc, char* argv[], char* envp[])
{
	puts("Zmienne srodowiskowe:");
	while (*envp != NULL) puts(*envp++);
	puts("Parametry programu:");
	for (int k = 0; k < argc; k++) puts(argv[k]);
}
