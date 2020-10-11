#include <iostream>
#include <string>


bool isSilent(char* ctab[])
{
	std::string arg;
	while (*ctab != NULL)
	{
		arg = *ctab++;
		if (arg == "/s" || arg == "/S")
		{
			return true;
		}
	}
	return false;
}

int main(int argc, char* argv[])
{
	bool silent = isSilent(argv);
	int i = 1;
	if (silent)
	{
		argc--;
		i++;
	}

	int returnCode = 11;

	if (argc == 2 && isdigit(*argv[i]) && strlen(argv[i]) == 1)
	{
		returnCode = atoi(argv[i]);
	}
	else if (argc > 2)
	{
		returnCode = 13;
	}
	else if (argc == 2)
	{
		returnCode = 12;
	}
	if (!silent)
	{
		puts(std::to_string(returnCode).c_str());
	}
	return returnCode;
}
