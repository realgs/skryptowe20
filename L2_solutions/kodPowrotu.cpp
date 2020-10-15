#include <iostream>
#include <string>
#include <cstring>

#define SILENT_MODE_SWITCH "/S"
#define NO_PARAM_RETURN_CODE 11
#define PARAM_NOT_A_DIGIT_RETURN_CODE 12
#define MORE_THAN_ONE_PARAM_RETURN_CODE 13
#define DEFAULT_DESIRED_ARGC_VAL 2

std::string getUppercase(char sequence[]) {
	std::string uppercase_sequence = "";

	for (int i = 0; i < strlen(sequence); i++)
		uppercase_sequence += toupper(sequence[i]);

	return uppercase_sequence;
}

bool isSilentModeSwitch(char param[]) 
{
	return strcmp(getUppercase(param).c_str(), SILENT_MODE_SWITCH) == 0;
}

int getDigitReturnCode(char* param) {
	if (isdigit(*param) && strlen(param) == 1) {
		return atoi(param);
	}
	else {
		return PARAM_NOT_A_DIGIT_RETURN_CODE;
	}
}


int main(int argc, char* argv[])
{
	if (argc == 1) {
		std::cout << NO_PARAM_RETURN_CODE << std::endl;
		return NO_PARAM_RETURN_CODE;
	}

	bool is_in_silent_mode = false;
	int desired_argc_val = DEFAULT_DESIRED_ARGC_VAL;
	int return_code = NO_PARAM_RETURN_CODE;

	int param_index = argc - 1;
	for (int i = 1; i < argc; i++) {
		if (isSilentModeSwitch(argv[i])) {
			is_in_silent_mode = true;
			desired_argc_val += 1;
			break;
		}
		else {
			param_index = i;
		}
	}

	if (argc > desired_argc_val) {
		return_code = MORE_THAN_ONE_PARAM_RETURN_CODE;
	}
	else if (argc < desired_argc_val) {
		return_code = NO_PARAM_RETURN_CODE;
	}
	else {
		return_code = getDigitReturnCode(argv[param_index]);
	}

	if (!is_in_silent_mode) {
		std::cout << return_code << std::endl;
	}

	return return_code;
}
