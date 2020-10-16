#include <iostream>
using namespace std;
bool silentMode = false;

const int NO_PARAMETERS = 11;
const int NOT_NUMBER_PARAMETER = 12;
const int MORE_THAN_ONE_PARAMETERS = 13;

bool isSilentModeOn(char arg[])
{
	if ((string)arg == "/s" || (string)arg == "/S") return true;
	else return false;
}

bool isDigit(char* argv[], int number)
{
	if (strlen(argv[number]) == 1)
	{
		if (!isdigit(*argv[number]))
		{
			return false;
		}
		return true;
	}
	return false;
}


int main(int argc, char* argv[])
{
	for (int i = 1; i < argc; i++)
	{
		if (isSilentModeOn(argv[i]))
		{
			silentMode = true;
			break;
		}
	}
	if (argc == 1)
	{
		cout << NO_PARAMETERS;
		return NO_PARAMETERS;
	}
	if (argc == 2)
	{
		if (silentMode)
		{
			return NO_PARAMETERS;
		}
		if (isDigit(argv, 1))
		{
			cout << argv[1];
			return (int)argv[1];
		}
		cout << NOT_NUMBER_PARAMETER;
		return NOT_NUMBER_PARAMETER;
	}
	if (argc == 3)
	{
		if (silentMode && isDigit(argv, 1))
		{
			return (int)argv[1];
		}
		if (silentMode && isDigit(argv, 2))
		{
			return (int)argv[2];
		}
		if (silentMode)
		{
			return NOT_NUMBER_PARAMETER;
		}
		cout << MORE_THAN_ONE_PARAMETERS;
		return MORE_THAN_ONE_PARAMETERS;
	}
	else
	{
		if (!silentMode) cout << MORE_THAN_ONE_PARAMETERS;
		return MORE_THAN_ONE_PARAMETERS;
	}
}