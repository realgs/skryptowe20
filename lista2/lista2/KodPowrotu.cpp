#include <iostream>
using namespace std;

#define NO_ARGUMENTS 11
#define NOT_A_DIGIT 12
#define TOO_MANY_ARGUMENTS 13

bool bIsSilent = false;

bool isDigit(char* number[], int index)
{
	if (strlen(number[index]) == 1) {
		if (isdigit(*number[index])) return true;
		else  return false;
	}
	else return false;
}

void returnCodeCout(char* code[], int index)
{
	if (!bIsSilent) cout << code[index];
}

void returnCodeCout(int code) {
	if (!bIsSilent) cout << code;

}

bool isSilent(int argc, char* arg[])
{
	for (int i = 1; i < argc; i++)
	{
		if ((string)arg[i] == "/s" || (string)arg[i] == "/S") return true;
	}
	return false;
}


int main(int argc, char* argv[])
{
	bIsSilent = isSilent(argc, argv);
	if (argc == 1)
	{
		returnCodeCout(NO_ARGUMENTS);
		return NO_ARGUMENTS;
	}
	if (argc == 2)
	{
		if (bIsSilent)
		{
			return NO_ARGUMENTS;
		}
		if (isDigit(argv, 1))
		{
			returnCodeCout(argv, 1);
			return (int)argv[1];
		}
		else
		{
			returnCodeCout(NOT_A_DIGIT);
			return(NOT_A_DIGIT);
		}
	}
	if (argc == 3)
	{
		if (isDigit(argv, 1) && bIsSilent)
		{
			return (int)argv[1];
		}
		if (isDigit(argv, 2) && bIsSilent)
		{
			return (int)argv[2];
		}
		if (bIsSilent)
		{
			returnCodeCout(NOT_A_DIGIT);
			return NOT_A_DIGIT;
		}
		returnCodeCout(TOO_MANY_ARGUMENTS);
		return TOO_MANY_ARGUMENTS;
	}
	else
	{
		if (!bIsSilent) returnCodeCout(TOO_MANY_ARGUMENTS);
		return TOO_MANY_ARGUMENTS;
	}
}
