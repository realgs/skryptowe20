#include <iostream>

int main(int argc, char* argv[], char* env[])
{
	
	std::cout << "Zmienne srodowiska:";
	while (*env != NULL) 
		std::cout << "\n" << *env++;

	std::cout << "\n\nArgumenty programu:";
	for (int k = 0; k < argc; k++)
		std::cout << "\n" << argv[k];
}

