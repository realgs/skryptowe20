#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;

bool isNumber(string number)
{
	int counter = 0;
	int dot_counter = 0;
	if (number[0] == '-') {
		counter = 1;
	}
	while (number[counter] != NULL)
	{
		if (number[counter] == '.') dot_counter++;
		else if (!isdigit(number[counter])) return false;
		counter++;
	}
	if(dot_counter > 1 || !isdigit(number[counter - 1])) return false;
	return true;	
}

int main(int argc, char* argv[])
{
	double sum = 0.0;
	string data;
	for (int i = 1; i < argc; i++)
	{
		if (isNumber(argv[i]))
		{
			sum += stod(argv[i]);
		}		
	}

	while (cin >> data)
	{
		if (isNumber(data))
		{
			sum += stod(data);
		}
	}
	cout << sum << endl;
}
