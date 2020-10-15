// KodPowrotu.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//
#include "KodPowrotu.h"
#include <iostream>
#include <sstream>



bool isSilent(char* argv[], int argc) {
	for (int i = 1; i < argc; i++) {
		if (argv[i] == "/s" || argv[i] == "/S") {
			return true;
		}
	}
	return false;
}



int main(int argc, char* argv[], char* env[])
{


	if (argc == 1) {return NO_PARAMETER_GIVEN; }
	else if (argc > 3 || argc == 3 && !isSilent(argv, argc)) { return TOO_MANY_ARGUMENTS; }
	else {
		bool silentMode = isSilent(argv, argc);
		if (isdigit(*argv[1])) {
			if (!silentMode) { std::cout << atoi(argv[1]); }
			return atoi(argv[1]);
		}
		else if (isdigit(*argv[2])) {
			if (!silentMode) { std::cout << atoi(argv[2]); }
			return atoi(argv[2]);
		}
		else {
			return NOT_A_NUMBER;
		}
		
	}
}