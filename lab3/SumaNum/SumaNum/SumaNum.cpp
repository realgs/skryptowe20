#include <iostream>

#define NO_PARAMETERS_GIVEN 11;

bool isNumber(char number[])
{
    int i = 0;

    if (number[0] == '-')
        i = 1;
    for (; number[i] != '\0'; i++)
    {
        if (!isdigit(number[i]))
            return false;
    }
    return true;
}

int main(int argc, char* argv[], char* env[])
{
	int sum = 0;
	if (argc < 2) { return NO_PARAMETERS_GIVEN; }
	
	for (int i = 1; i < argc; i++)
	{
        if (isNumber(argv[i])) {
            sum += strtol(argv[i], NULL, 10);
        }
	}
	std::cout << "The sum is: " << sum;
}
