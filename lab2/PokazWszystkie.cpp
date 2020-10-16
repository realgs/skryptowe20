#include <iostream>

int main(int argc, char* argv[], char* env[]) {
	for(; *argv; argv++) {
		std::cout << *argv << "\n";
	}
	for (; *env; env++) {
		std::cout << *env<<"\n";
	}
}
