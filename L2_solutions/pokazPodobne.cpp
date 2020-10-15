#include <iostream>
#include <cstring>
#include <string.h>
#include <algorithm>

#define SILENT_MODE_SWITCH_UPPER "/S"
#define SILENT_MODE_SWITCH_LOWER "/s"
#define NAME_AND_VALUE_SEPARATOR '='
#define VALUES_SEPARATOR ';'


bool isSilentModeSwitch(char* param)
{
	return strcmp(param, SILENT_MODE_SWITCH_UPPER) == 0 || strcmp(param, SILENT_MODE_SWITCH_LOWER) == 0;
}

int main(int argc, char* argv[], char* env[]) {
	bool is_in_silent_mode = false;
	int silent_mode_switch_position;
	for (int i = 1; i < argc; i++) {
		if (isSilentModeSwitch(argv[i])) {
			is_in_silent_mode = true;
			silent_mode_switch_position = i;
			break;
		}
	}

	for (int i = 1; i < argc; i++) {
		if (i != silent_mode_switch_position){
			bool param_found = false;
			int j = 0;
			while (env[j] != nullptr) {
				std::string env_str(env[j]);
				std::string env_name = env_str.substr(0, env_str.find(NAME_AND_VALUE_SEPARATOR));

				std::string argv_str(argv[i]);
				if (env_name.find(argv_str) != std::string::npos) {
					param_found = true;
					std::replace(env_str.begin(), env_str.end(), VALUES_SEPARATOR, '\n');
					std::cout << env_str << std::endl;
				}
				j++;
			}

			if (!param_found && !is_in_silent_mode) {
				std::cout << argv[i] << "=NONE" << std::endl;
			}
		}
	}

	return 0;
}
