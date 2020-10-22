#include <iostream>

int main(int argc, char* argv[], char* env[]) {
	puts("Args:");
	for (int i = 0; i < argc; i++){
		puts(argv[i]);
	}
	puts("Envs:");
	while (*env != NULL){
		puts(*env++);
	}
	return 10;
}
