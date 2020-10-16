#include <iostream>

int main(int argc, char* argv[], char* envp[]) {
	for(; *argv; argv++) {
		std::cout << *argv << "\n";
	}
	for (; *envp; envp++) {
		std::cout << *envp<<"\n";
	}
}
