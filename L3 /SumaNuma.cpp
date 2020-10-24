//
//  main.cpp
//  SumaNuma
//
//  Created by Filip Jabłoński on 23/10/2020.
//

#include <iostream>
#include <vector>
using std::cin, std::cout, std::endl, std::string, std::stod;

int main(int argc, const char * argv[])
{
	double sum = 0;
	string input;
	
	while (getline(cin, input) && input != ""  && !cin.eof())
	{
		try { sum += stod(input); }
		catch (std::invalid_argument error){}
	}
	
	cout << sum << endl;
	
	return 0;
}
