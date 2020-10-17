#include <iostream>
using namespace std;
bool silentMode = false;

const int NO_PARAMETERS = 11;
const int NOT_NUMBER_PARAMETER = 12;
const int MORE_THAN_ONE_PARAMETERS = 13;
const string SILENT_MODE_SMALL_CASE = "/s";
const string SILENT_MODE_UPPER_CASE = "/S";

bool isSilentModeOn(char arg[])
{
	if ((string)arg == SILENT_MODE_SMALL_CASE || (string)arg == SILENT_MODE_UPPER_CASE) return true;
	return false;
}

bool isDigit(char* argv[], int number)
{
	if (strlen(argv[number]) == 1)
	{
		if (isdigit(*argv[number]))
		{
			return true;
		}
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
	else if (argc == 2)
	{
		if (silentMode)
		{
			return NO_PARAMETERS;
		}
		else if (isDigit(argv, 1))
		{
			cout << argv[1];
			return (int)argv[1];
		}
		else
		{
			cout << NOT_NUMBER_PARAMETER;
			return NOT_NUMBER_PARAMETER;
		}
	}
	else if (argc == 3)
	{
		if (silentMode && isDigit(argv, 1))
		{
			return (int)argv[1];
		}
		else if (silentMode && isDigit(argv, 2))
		{
			return (int)argv[2];
		}
		else if (silentMode)
		{
			return NOT_NUMBER_PARAMETER;
		}
		else
		{
			cout << MORE_THAN_ONE_PARAMETERS;
			return MORE_THAN_ONE_PARAMETERS;
		}
	}
	else
	{
		if (!silentMode) cout << MORE_THAN_ONE_PARAMETERS;
		return MORE_THAN_ONE_PARAMETERS;
	}
}
