#include "pch.h"
#include <iostream>
using namespace std;

bool isSilentMode(char* argv[])
{
	string arg1;
	while (*argv != NULL)
	{
		arg1 = *argv++;
		if (arg1 == "/s" || arg1 == "/S")
		{
			return true;
		}
	}
	return false;
}

bool Contains(char* ctab[], char* substring)
{
	while (*ctab != NULL)
	{
		if (strstr(*ctab, substring))
		{
			return true;
		}
		(*ctab++);
	}
	return false;
}

void write(int argc, char* argv[], char* env[]) 
{
	while (*env != NULL)
	{
		bool isDone = false;
		for (int i = 1; i < argc; i++)
		{
			if (strstr(*env, argv[i]) && !isDone)
			{
				isDone = true;
				char* token;
				char* rest = *env;

				while ((token = strtok_s(rest, ";", &rest)))
				{
					puts(token);
				}
			}
		}
		(*env++);
	}
}

int main(int argc, char* argv[], char* env[])
{
	puts("Zmienne srodowiska: ");
	if (!isSilentMode(argv))
	{
		for (int i = 1; i < argc; i++)
		{
			if (!Contains(env, argv[i]))
			{
				string msg = string(argv[i]) + " = NONE";
				puts(msg.c_str());
			}
		}
	}
	write(argc, argv, env);
	return 0;
}

