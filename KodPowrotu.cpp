#include <iostream>
#include <string>

const int NO_PARAMETERS = 11;
const int PARAMETER_NOT_NUMBER = 12;
const int MORE_PARAMETERS = 13;

bool silent(int* count, char** args) {
	for(int i = 1; i < *count; i++){
		if (strcmp(args[i], "/s") == 0 || strcmp(args[i], "/S") == 0) {
			(*count)--;
			return true;
		}
	}
	return false;
}

bool isNumber(std::string number) {
	for(int i = 0; i < number.size(); i++)
		if (!isdigit(number[i])) return false;
	return true;
}

int main(int argc, char** argv)
{

	bool isSilent = silent(&argc, argv);
	int returnParameter;
	if (argc < 2) returnParameter = NO_PARAMETERS;
	else if (isNumber(argv[1])) returnParameter = atoi(argv[1]);
	else returnParameter = PARAMETER_NOT_NUMBER;

	if (argc > 2) returnParameter = MORE_PARAMETERS;
	if(!isSilent) std::cout << returnParameter;
	return returnParameter;
}
