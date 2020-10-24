
#include <iostream>
#include <string>
using namespace std;

int main()
{
	double sum = 0;
	string arg;
	getline(cin, arg);
	while (arg != "")
	{
		bool isNumber = true, isNegative = false;
		int tempInt = 0, i = 0;
		if (arg[0] == '-')
		{
			isNegative = true;
			i++;
		}
		for (; isNumber && arg[i] != NULL && arg[i] != '.'; i++)
		{
			if (arg[i] >= '0' && arg[i] <= '9')
			{
				tempInt *= 10;
				tempInt += arg[i] - '0';
			}
			else
				isNumber = false;
		}
		if (arg[i] == '.')
		{
			i++;
			double tempFrac = 0;
			double tempDiv = 1;
			for (; isNumber &&  arg[i] != NULL; i++)
			{
				if (arg[i] >= '0' && arg[i] <= '9')
				{
					tempFrac *= 10;
					int temp = arg[i] - '0';
					tempFrac += temp;
					tempDiv *= 10;
				}
				else
					isNumber = false;
			}
			if (isNumber)
			{
				if(isNegative)
					sum -= tempFrac / tempDiv;
				else
					sum += tempFrac / tempDiv;
			}
		}
		if (isNumber)
		{
			if(isNegative)
				sum -= tempInt;
			else
				sum += tempInt;
		}
		if (!cin.eof())
			getline(cin, arg);
		else
			arg = "";
		
	}
	cout << sum;
}
