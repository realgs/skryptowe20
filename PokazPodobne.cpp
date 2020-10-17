#include<iostream>
using namespace std;
bool silentMode = false;

const string SILENT_MODE_SMALL_CASE = "/s";
const string SILENT_MODE_UPPER_CASE = "/S";
const char* VAL_SEPARATOR = ";";
const char* NAME_VAL_SEPARATPR = "=";

bool isSilentModeOn(char arg[])
{
	if ((string)arg == SILENT_MODE_SMALL_CASE || (string)arg == SILENT_MODE_UPPER_CASE) return true;
	else return false;
}

void printEnvNameAndValues(char* var_name, char* var_values)
{
	cout << var_name << endl;
	cout << "=" << endl;

	char* value = strtok(var_values, VAL_SEPARATOR);
	while (value != NULL)
	{
		puts(value);
		value = strtok(NULL, VAL_SEPARATOR);
	}
	cout << endl;
}

void checkEnvSimilarity(char* envp[], char* substring)
{
	bool similarity_found = false;
	for (int i = 0; envp[i] != NULL; i++)
	{
		char* name = strtok(envp[i], NAME_VAL_SEPARATPR);
		char* values = strtok(NULL, NAME_VAL_SEPARATPR);
		if (strstr(name, substring) != NULL)
		{
			similarity_found = true;
			printEnvNameAndValues(name, values);
		}
	}
	if (!similarity_found && !silentMode) cout << substring << " = NONE";
}

int main(int argc, char* argv[], char* envp[])
{
	for (int i = 1; i < argc; i++)
	{
		if (isSilentModeOn(argv[i]))
		{
			silentMode = true;
			break;
		}
	}

	for (int i = 1; i < argc; i++)
	{
		checkEnvSimilarity(envp, argv[i]);
	}
}
