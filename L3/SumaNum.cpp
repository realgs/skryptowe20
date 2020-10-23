
#include "pch.h"
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
using namespace std;
void add_numbers()
{
	double add_numbers = 0.0;
	string one_token;
	while (cin >> one_token)
	{
		try 
		{
			add_numbers += stod(one_token);
		}
		catch (std::exception& e) {}
	}
	cout << add_numbers << endl;
}

int main(int argc, char *argv[], char *env[])
{
	add_numbers();
	return 0;
}