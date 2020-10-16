#include <iostream>
#include <cctype>

std::pair<bool, int> isSilence(int argc, char* argv[]) {
	bool isSilence = false;
	int silenceIndex = 0;

	for (int i = 1; i < argc; i++) {
		if (strcmp(argv[i], "/s") == 0 || strcmp(argv[i], "/S") == 0) {
			isSilence = true;
			silenceIndex = i;
		}
	}

	return std::make_pair(isSilence, silenceIndex);
}

void getCodeFromParam(char* argv[], int silenceIndex, int& returnCode) {
	char* argValue;

	if (isSilence && silenceIndex == 1) {
		argValue = argv[2];
	} else {
		argValue = argv[1];
	}

	if (strlen(argValue) == 1 && std::isdigit(argValue[0])) {
		returnCode = argValue[0] - '0';
	} else {
		returnCode = 12;
	}
}

int calculateReturnCode(int argc, char* argv[], bool isSilence, int silenceIndex) {
	int returnCode;
	if (argc < 2 || (argc == 2 && isSilence)) {
		returnCode = 11;
	} else if (argc == 2 || (argc == 3 && isSilence)) {
		getCodeFromParam(argv, silenceIndex, returnCode);
	} else {
		returnCode = 13;
	}

	return returnCode;
}

int main(int argc, char* argv[]) {
	auto silenceParams = isSilence(argc, argv);
	int returnCode = calculateReturnCode(argc, argv, silenceParams.first, silenceParams.second);

	if (!silenceParams.first) {
		std::cout << returnCode << "\n";
	}

	return returnCode;
}
