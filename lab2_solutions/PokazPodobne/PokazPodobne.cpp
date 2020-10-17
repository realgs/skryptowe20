#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>

using namespace std;

#define SILENT_MODE_LOWER_CASE "/s"
#define SILENT_MODE_UPPER_CASE "/S"
#define ENV_EQUAL_SIGN "="
#define ENV_ADDRESS_SEPARATOR ";"

bool silentModeSwitch(char* arg) {
	return (strcmp(arg, SILENT_MODE_LOWER_CASE) == 0 || strcmp(arg, SILENT_MODE_UPPER_CASE) == 0);
}

void transformParameters(int argc, char* argv[], vector<string>& parameters, bool* silentMode) {
	*silentMode = false;
	for (int i = 1; i < argc; i++) {
		if (silentModeSwitch(argv[i])) *silentMode = true;
		else {
			string parameter = argv[i];
			transform(parameter.begin(), parameter.end(), parameter.begin(), ::toupper);
			parameters.push_back(parameter);
		}
	}
}

void printEnvironmentVar(string envName, string envAddress) {
	vector <string> separatedAddresses;
	stringstream addressStream(envAddress);
	string singleAddress;

	while (getline(addressStream, singleAddress, ';')) {
		separatedAddresses.push_back(singleAddress);
	}

	for (unsigned int i = 0; i < separatedAddresses.size(); i++) {
		cout << envName << " = " << separatedAddresses[i] << endl;
	}
}


void findEnvironmentVar(string environmentVar, vector<string> parameters, bool silentMode) {
	int equalSignIndex = environmentVar.find(ENV_EQUAL_SIGN);

	string envName = environmentVar.substr(0, equalSignIndex);
	string envNameToUpper = envName;
	transform(envNameToUpper.begin(), envNameToUpper.end(), envNameToUpper.begin(), ::toupper);
	string envAddress = environmentVar.substr(equalSignIndex + 1);

	int parametersNumber = parameters.size();
	bool found = false;

	for (int i = 0; i < parametersNumber; i++) {
		if (envNameToUpper.find(parameters[i]) != string::npos) {
			printEnvironmentVar(envName, envAddress);
			found = true;
		}
	}
	if ((!found || parametersNumber == 0) && !silentMode) {
		cout << envName << " = NONE" << endl;
	}
}

int main(int argc, char* argv[], char* env[])
{
	bool* silentMode = new bool(false);
	vector <string> parameters;
	transformParameters(argc, argv, parameters, silentMode);
	int parametersNumber = parameters.size();

	while (*env != NULL) {
		string environmetVar(*env++);
		findEnvironmentVar(environmetVar, parameters, *silentMode);
	}

	delete silentMode;
	return 0;
}
