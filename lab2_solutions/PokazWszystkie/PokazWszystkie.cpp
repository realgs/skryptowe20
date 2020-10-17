#include <iostream>
using namespace std;

#define SILENT_MODE_LOWER_CASE "/s"
#define SILENT_MODE_UPPER_CASE "/S"

bool silentModeSwitch(char* arg) {
	return (strcmp(arg, SILENT_MODE_LOWER_CASE) == 0 || strcmp(arg, SILENT_MODE_UPPER_CASE) == 0);
}

int main(int argc, char* argv[], char* env[])
{
	cout << "Environment variables: " << endl;
	while (*env != NULL) {
		cout << (*env++) << endl;
	}

	cout << endl << "Program parameters: " << endl;
	for (int i = 1; i < argc; i++) {
		if (!silentModeSwitch(argv[i])) cout << argv[i] << endl;
	}

	return 0;
}
