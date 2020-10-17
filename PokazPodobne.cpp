#include <iostream>
#include <string.h>

bool isSilentTriggered(int argc, char ** argv);
bool doesVariableContainArgument(char * variable, char * argument);
void printVariable(char * variable);

int main(int argc, char ** argv, char ** envp) {
	bool isSilent = isSilentTriggered(argc, argv);
	int didOccurSize = (isSilent ? argc - 2 : argc - 1);
	bool didArgumentOccurInAnyVariable[didOccurSize];

	for (int i = 0; envp[i] != NULL; i++) {
		bool wasFound = false;
		for (int j = (isSilent ? 2 : 1); argv[j] != NULL; j++) {
			bool doesContain = doesVariableContainArgument(envp[i], argv[j]);
			if (doesContain) {
				int argumentIndex = (isSilent ? j - 2 : j - 1);
				if (!didArgumentOccurInAnyVariable[argumentIndex])
					didArgumentOccurInAnyVariable[argumentIndex] = true;
				if (!wasFound)
					wasFound = true;
			}
		}
		if (wasFound)
			printVariable(envp[i]);
	}
	if (!isSilent) {
		for (int i = 0; i < didOccurSize; i++) {
			if (!didArgumentOccurInAnyVariable[i])
				std::cout << argv[(i + 1)] << " = NONE" << std::endl;
		}
	}
}

bool isSilentTriggered(int argc, char ** argv) {
	if (argc == 1)
		return false;
	return strlen(argv[1]) == 2 && argv[1][0] == '/' && argv[1][1] == 'S';
}

bool doesVariableContainArgument(char * variable, char * argument) {
	std::string variableString(variable);
	std::string argumentString(argument);

	std::string variableName = variableString.substr(0, variableString.find("="));
	return variableName.find(argumentString) != -1;
}

void printVariable(char * variable) {
	std::string variableString(variable);

	int equalPosition = variableString.find("=");
	std::string stringVariableName = variableString.substr(0, equalPosition);
	std::cout << stringVariableName << std::endl << '=' << std::endl;;

	std::string variableContent = variableString.substr(equalPosition + 1);
	int semicolonPosition = variableContent.find(";");
	while (semicolonPosition != -1) {
		std::string toWrite = variableContent.substr(0, semicolonPosition);
		variableContent = variableContent.substr(semicolonPosition + 1);
		std::cout << toWrite << std::endl;

		semicolonPosition = variableContent.find(";");
	}
	if(variableContent.length() != 0)
		std::cout << variableContent << std::endl;
}