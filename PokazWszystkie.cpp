#include <xlocinfo>
#include <stdio.h>

int main(int argc, char* argv[], char* env[]) {

	puts("Argumenty:");
	for (int i = 1; i < argc; i++)
		puts(argv[i]);

	puts("");

	puts("Zmienne srodowiskowe: ");
	while (*env != NULL)
		puts(*env++);
	
}