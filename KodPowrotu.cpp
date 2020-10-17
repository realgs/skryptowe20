
#include <iostream>

int main(int argc, char* argv[], char* env[]) {

	const char* exit_code;
	char s[] = "/s";
	char S[] = "/S";
	bool silent_mode = false;

	if (strcmp(argv[argc - 1], s) == 0
		|| strcmp(argv[argc - 1], S) == 0) {
		silent_mode = true;
		argc--;
	}

	if (argc == 1) {
		exit_code = "11";
	}
	else if (argc > 2) {
		exit_code = "13";
	}
	else if (!isdigit(*argv[1])) {
		exit_code = "12";
	}
	else {
		exit_code = argv[1];
	}

	if (!silent_mode) {
		puts(exit_code);
	}

	return atoi(exit_code);
}