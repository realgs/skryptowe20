#pragma warning(disable:4996)
#include <iostream>


bool argPresent(char* buffer, int argc, char* argv[], bool silent_mode)
{
	int i;
	if (silent_mode)
		i = 2;
	else
		i = 1;
	for (i; i < argc; i++)
	{
		if (strstr(buffer, argv[i]))
			return true;
	}
	return false;
}


int main(int argc, char* argv[], char* envp[])
{
	bool silent_mode = false;
	bool found_flag = false;
	char* buffer;
	if (argc > 1)
		if (std::string(argv[1]) == "/s" || std::string(argv[1]) == "/S")
			silent_mode = true;
	while (*envp)
	{
		buffer = strtok(*envp++, "=");
		if (argPresent(buffer, argc, argv, silent_mode))
		{
			found_flag = true;
			std::cout << buffer << "\n=\n";
			buffer = strtok(NULL, ";");
			while (buffer)
			{
				std::cout << buffer << std::endl;
				buffer = strtok(NULL, ";");
			}
			std::cout << std::endl;
		}
	}
	if (!found_flag && !silent_mode)
	{
		for (auto i = 1; i < argc; i++)
		{
			std::cout << argv[i] << " ";
		}
		std::cout << "= NONE\n";
	}
}
