#include<iostream>

bool isSilentModeOn(int argc, char** argv)
{
	for (int i = 1; i < argc; i++)
	{
		if (strcmp(argv[i], "/s") == 0 || strcmp(argv[i], "/S") == 0)
			return true;
	}

	return false;
}
void printVarValues(char* var_values)
{
	char* value = strtok(var_values, ";");
	while (value != NULL)
	{
		std::cout << value << std::endl;
		value = strtok(NULL, ";");
	}
	std::cout << std::endl;
}
void printVar(char* var_name, char* var_values)
{
	std::cout << var_name << std::endl;
	std::cout << "=" << std::endl;
	printVarValues(var_values);
}
void getEnvVars(char** envp, char* substring, bool isSilent)
{
	bool env_found = false;
	while (*envp != NULL)
	{
		char* var_name = strtok(*envp, "=");
		char* var_values = strtok(NULL, "=");
		if (strstr(var_name, substring) != NULL)
		{
			env_found = true;
			printVar(var_name, var_values);
		}
		*envp++;
	}
	if (!env_found && !isSilent)
		std::cout << substring << " = NONE" << std::endl;
}
int main(int argc, char** argv, char** envp)
{
	bool silent = isSilentModeOn(argc, argv);
	for (int i = 1; i < argc; i++)
	{
		char* arg = argv[i];
		getEnvVars(envp, arg, silent);
	}
}