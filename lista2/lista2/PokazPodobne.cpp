#include<iostream>
#include<string>
using namespace std;

bool isSilent(int argc, char** argv)
{
	for (int i = 1; i < argc; i++)
	{
		if ((string)argv[i] == "/s" || (string)argv[i] == "/S") return true;
	}
	return false;
}

void printVarValues(char* var_values)
{
	char* value = strtok(var_values, ";");
	while (value != NULL)
	{
		cout << value << endl;
		value = strtok(NULL, ";");
	}
	cout << endl;
}

void printVar(char* var_name, char* var_values)
{
	cout << var_name << endl;
	cout << "=" << endl;
	printVarValues(var_values);
}

void getEnvVars(char* arg, char** envp, bool bSilent)
{
	bool bEnv_found = false;
	while (*envp != NULL)
	{
		char* var_name = strtok(*envp, "=");
		char* var_values = strtok(NULL, "=");
		if (strstr(var_name, arg) != NULL)
		{
			bEnv_found = true;
			printVar(var_name, var_values);
		}
		*envp++;
	}
	if (!bEnv_found && !bSilent) cout << arg << " = NONE" << endl;
}

int main(int argc, char** argv, char** envp)
{
	bool bIsSilent = isSilent(argc, argv);
	for (int i = 1; i < argc; i++)
	{
		getEnvVars(argv[i], envp, bIsSilent);
	}
}
