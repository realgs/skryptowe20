#include <iostream>
#include <string>
#include <vector>
#define NO_PARAMETERS_GIVEN 11;

bool isNumber(std::string number)
{
	int i = 0;
	int dotCount = 0;
	if (number[0] == '-') {
		i = 1;
	}
	for (; number[i] != '\0'; i++)
	{
		if (number[i] == '.') {
			dotCount++;
			continue;
		}
		if (!isdigit(number[i]) || dotCount > 1)
			return false;
	}
	return true;
}



int main(int argc, char* argv[], char* env[])
{
	double sum = 0.0;
	std::string number;
	std::vector <std::string> numbersToSum;
	for (int i = 1; i < argc; i++)
	{	
		numbersToSum.clear();
		std::string argument(argv[i]);
		if (argument.find(" ") != std::string::npos && argument.find('\t') != std::string::npos) {
			while (argument != "") {
				if (argument.find(" ") != std::string::npos) {
					number = argument.substr(0, argument.find(" "));
					argument = argument.substr(argument.find(" ") + 1, argument.size());
				}
				else if (argument.find('\t') != std::string::npos) {
					number = argument.substr(0, argument.find('\t'));
					argument = argument.substr(argument.find('\t') + 1, argument.size());
				}
				else {
					number = argument;
				}
				numbersToSum.push_back(number);
				/*if (isNumber(number)) {
					sum += std::stod(argument.c_str());
				}*/
			}
		}
		else {
			numbersToSum.push_back(argument);
		}
		for (int i = 0; i < numbersToSum.size(); i++) {
			if (isNumber(numbersToSum.at(i))) {
				sum += std::stod(numbersToSum.at(i).c_str());
			}
		}
	}
	std::cout << "The sum is: " << sum;
}
