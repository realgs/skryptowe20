#include <iostream>

int main(int argc, char ** argv, char **envp) {
	for (int i = 0; envp[i] != NULL; i++) {
		std::cout << envp[i] << std::endl;
	}
	for (int i = 0; argv[i] != NULL; i++) {
		std::cout << argv[i] << std::endl;
	}
}