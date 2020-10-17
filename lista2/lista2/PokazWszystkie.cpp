#include <iostream>
using namespace std;

int main(int argc, char* argv[], char* env[])
{
	puts("Zmienne srodowiskowe:");
	for (int i = 0; *env[i] != NULL; i++) puts(env[i]);
	puts("Parametry programu:");
	for (int k = 0; k < argc; k++) puts(argv[k]);
	return 0;
}
