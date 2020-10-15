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

int check(int argc, char* argv[])
{
	if (!isSilentMode(argv))
	{
		puts("Argumenty programu: ");
		if (argc == 2 && isdigit(*argv[1]))
		{
			for (int i = 0; i < argc; i++)
			{
				puts(argv[1]);
				return int(argv[i]);
			}
		}
		else if (argc == 1)
		{
			puts("11");
			return 11;
		}
		else if (argc == 2 && !isdigit(*argv[1]))
		{
			puts("12");
			return 12;
		}
		else if (argc > 2)
		{
			puts("13");
			return 13;
		}
	}
	else {

		if (argc == 2 && isdigit(*argv[2]))
		{
			for (int i = 0; i < argc; i++)
				return int(argv[i]);
			
		}
		else if (argc == 2)  return 11;
		else if (argc == 3 && !isdigit(*argv[2])) return 12;
		else if (argc > 3)  return 13;
		
	}
}

int main(int argc, char* argv[])
{
	return check(argc, argv);
}

