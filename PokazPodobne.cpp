#include <iostream>
#include <sstream> 

using namespace std;

int main(int argc, char *argv[], char* env[]) {

	string env_variable;
	string env_variable_name;
	string delimiter = "=";
	char s[] = "/s";
	char S[] = "/S";
	bool silent_mode = false;
	bool env_variable_exist;

	if (strcmp(argv[argc - 1], s) == 0
		|| strcmp(argv[argc - 1], S) == 0) {
		silent_mode = true;
		argc--;
	}

	*argv++;

	while (*argv != NULL) {
		if (*(argv + 1) == NULL && silent_mode == true)
		{
			break;
		}

		cout << "enviroment variables for ";
		cout << *argv << endl;

		int env_count = 0;
		env_variable_exist = false;

		while (*(env + env_count) != NULL) {

			env_variable = *(env + env_count);
			env_variable_name = env_variable.substr(0, env_variable.find(delimiter));

			if (env_variable_name.find(*argv) != string::npos) {

				for (int j = 0; j < env_variable.size(); j++) {
					if (env_variable[j] == ';') {
						env_variable = env_variable.insert(j + 1, "\n");
					}
				}
				env_variable_exist = true;
				cout << env_variable << endl;
			}
			env_count++;
		}

		if (silent_mode == false && env_variable_exist == false) {
			cout << "parametr = NONE" << endl;
		}

		*argv++;
	}

	return 0;
}


