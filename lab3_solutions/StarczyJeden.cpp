#include <iostream>
#include <string>
#include <algorithm>

using namespace std;

void readAndPrintMatchingLines(int argc, char* argv[]) {
	string input;
	string inputToLower;
	string paramToLower;

	bool found = false;

	while (getline(cin, input)) {
		for (int i = 1; i < argc; i++) {
			inputToLower = input;
			transform(inputToLower.begin(), inputToLower.end(), inputToLower.begin(), ::tolower);

			paramToLower = argv[i];
			transform(paramToLower.begin(), paramToLower.end(), paramToLower.begin(), ::tolower);

			if (inputToLower.find(paramToLower) != string::npos) {
				found = true;
			}
		}
		if (found) cout << input << endl;
		found = false;
	}
}

int main(int argc, char* argv[])
{
	readAndPrintMatchingLines(argc, argv);
}
