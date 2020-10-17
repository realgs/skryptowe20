#include <iostream>
#include <string>
#include <vector>

constexpr int NO_PARAM = 11;
constexpr int NOT_DIGIT = 12;
constexpr int TOO_MANY_PARAM = 13;


bool isNum(std::string str)
{
	for (auto character : str)
	{
		if (!isdigit(character))
			return false;
		return true;
	}
}

void getErrorCode(int index, char* argv[], int &return_code)
{
	if (argv[index])
	{
		std::string str = argv[index];
		if (isNum(str))
			return_code = stoi(str);
		else
			return_code = NOT_DIGIT;
	}
	else
	{
		return_code = NO_PARAM;
	}
}


int main(int argc, char* argv[])
{
	int return_code = 0;
	bool silent_mode = false;
	if (argc > 1)
		if (std::string(argv[1]) == "/s" || std::string(argv[1]) == "/S")
			silent_mode = true;
	if ((argc > 2 && !silent_mode) || argc > 3)
	{
		return_code = TOO_MANY_PARAM;
		if (!silent_mode) 
			std::cout << "return code = " << return_code << std::endl;
	}
		
	else if (!silent_mode)
	{
		getErrorCode(1, argv, return_code);
		std::cout << "return code = " << return_code << std::endl;
	}
	else
		getErrorCode(2, argv, return_code);
	return return_code;
}
