#include <iostream>
#include <string>
#include <algorithm>
#include "PokazPodobne.h"

/**
*	W tym programie zakładam, że tryb cichy będzie podany na końcu argumentów, nie w środku, ani nie na początku.
*/

bool isSilent(char* argv[], int argc) {
	for (int i = 1; i < argc; i++) {
		std::string arg = argv[i];
		if (arg == "/s" || arg == "/S") {
			return true;
		}
	}
	return false;
}

void printInfo(std::string name, std::string varInfo) {
	std::cout << "i. " << name << std::endl;
	std::cout << "ii. " << VARIABLE_DEFINITION_SEPARATOR << std::endl;
	std::cout << "iii. ";

	while (varInfo.find(VARIABLE_COMPLEX_SEPARATOR) != std::string::npos) {
		std::cout << varInfo.substr(0, varInfo.find(VARIABLE_COMPLEX_SEPARATOR)) << std::endl;
		varInfo = varInfo.substr(varInfo.find(VARIABLE_COMPLEX_SEPARATOR) + 1, varInfo.size());
	}
	std::cout << varInfo << std::endl;
}

int main(int argc, char* argv[], char* env[])
{
	bool silentMode = isSilent(argv, argc);
	bool found;

	for (int i = 1; i < argc; i++) {

		std::string argument = argv[i];
		found = false;
		int j = 0;
		while (env[j] != nullptr) {
			std::string envVariable(env[j++]);
			size_t split_index = envVariable.find(VARIABLE_DEFINITION_SEPARATOR);
			std::string varName = envVariable.substr(0, split_index);
			std::transform(varName.begin(), varName.end(), varName.begin(), ::toupper);
			std::transform(argument.begin(), argument.end(), argument.begin(), ::toupper);
			if (varName.find(argument) != std::string::npos) {
				std::cout << "Parametr: " << argument << std::endl;
				found = true;
				printInfo(envVariable.substr(0, split_index), envVariable.substr(split_index + 1, envVariable.size()));
			}
		}
		if (!found && !silentMode) {
			std::cout << "Parametr: " << argument << " = NONE" << std::endl;
		}
	}
}
