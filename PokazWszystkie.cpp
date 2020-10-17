
#include <iostream>

int main(int argc, char* argv[], char* env[]) {

	puts("app args");

	for (int k = 0; k < argc; k++) {
		puts(argv[k]);
	}

	puts("env variables");

	while (*env != NULL) {
		puts(*env++);
	}

	return 0;
}

