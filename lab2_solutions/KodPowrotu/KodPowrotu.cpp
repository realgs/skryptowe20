#include <iostream>
#include <vector>
#include <string>

using namespace std;

#define NO_PARAMETER 11;
#define NOT_DIGIT 12;
#define MORE_THAN_ONE_PARAMETER 13;
#define SILENT_MODE_LOWER_CASE "/s"
#define SILENT_MODE_UPPER_CASE "/S"

bool silentModeSwitch(char* arg) {
	return (strcmp(arg, SILENT_MODE_LOWER_CASE) == 0 || strcmp(arg, SILENT_MODE_UPPER_CASE) == 0);
}

bool isDigit(char* arg) {
	return(isdigit(*arg) != 0 && strlen(arg) == 1);
}

int returnCodeWithSilentMode(bool isSilentMode, int code) {
	if (!isSilentMode) cout << code << endl;
	return code;
}

int main(int argc, char* argv[])
{
	int numberOfParameters;
	bool isSilentMode = false;
	bool isNumber = false;
	int returnCode;
	vector<char*> parameters;

	for (int i = 1; i < argc; i++) {
		if (silentModeSwitch(argv[i])) {
			isSilentMode = true;
		}
		else {
			parameters.push_back(argv[i]);
		}
	}

	numberOfParameters = parameters.size();

	if (numberOfParameters == 0) { returnCode = NO_PARAMETER; }
	else if (numberOfParameters > 1) { returnCode = MORE_THAN_ONE_PARAMETER; }
	else {
		if (isDigit(parameters[0])) { returnCode = atoi(parameters[0]); }
		else { returnCode = NOT_DIGIT; }
	}

	return returnCodeWithSilentMode(isSilentMode, returnCode);
}
