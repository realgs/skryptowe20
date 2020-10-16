#include <iostream>

bool isSilent(char* argv[]) {
	while(*argv != nullptr) {
		std::string arg = *argv++;
		if (arg == "/s" || arg == "/S")
			return true;
	}
	return false;
}

int checkArguments(int argc, char* argv[]) {
	int returnCode;
	bool isCalledSilent = isSilent(argv);
	int argumentsExpected = 2;

	if (isCalledSilent) {
		argumentsExpected++;
	}

	if (argc <= argumentsExpected - 1) {
		returnCode = 11;
	} else if (argc > argumentsExpected) {
		returnCode = 13;
	} else 	if (argc == argumentsExpected) {
		for (int i = 0; i < argumentsExpected; i++) {
			if (isdigit(*argv[i]) && argv[i] != "/s" && argv[i] != "/S") {
				returnCode = int(*argv[i]) - 48;
			} else if (!isdigit(*argv[i]) && argv[i] != "/s" && argv[i] != "/S") {
				returnCode = 12;
			}
		}
	}

	if (!isCalledSilent) {
		printf("Code: %i\n", returnCode);
	}
	return returnCode;
}

int main( int argc, char* argv[] ) {
	return checkArguments(argc, argv);
}
