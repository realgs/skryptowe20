#include <iostream>
#include <string.h>

const int NO_PARAMETER = 11;
const int PARAMETER_NOT_A_DIGIT = 12;
const int TOO_MANY_PARAMETERS = 13;

bool isSilentTrigger(char* triggerToCheck);
bool isDigit(char* toCheck);

int main(int argc, char** argv) {
	bool isSilent = false;
	int returnCode = 0;
	if (argc == 1)
		returnCode = NO_PARAMETER;
	else {
		isSilent = isSilentTrigger(argv[1]);
		if (argc > 3)
			returnCode = TOO_MANY_PARAMETERS;
		else if (isSilent) {
			if (argc == 2)
				returnCode = NO_PARAMETER;
			else if (isDigit(argv[2]))
				returnCode = argv[2][0] - 48;
			else
				returnCode = PARAMETER_NOT_A_DIGIT;
		}
		else {
			if (argc == 3)
				returnCode = TOO_MANY_PARAMETERS;
			else if(isDigit(argv[1]))
				returnCode = argv[1][0] - 48;
			else 
				returnCode = PARAMETER_NOT_A_DIGIT;
		}	
	}
	if (!isSilent)
		std::cout << returnCode << std::endl;
	return returnCode;
}

bool isSilentTrigger(char* triggerToCheck) {
	if (strlen(triggerToCheck) != 2)
		return false;
	return triggerToCheck[0] == '/' && (triggerToCheck[1] == 's' || triggerToCheck[1] == 'S');
}

bool isDigit(char* toCheck) {
	if (strlen(toCheck) != 1)
		return false;
	return  47 < toCheck[0] && toCheck[0] < 58;
}