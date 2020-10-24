//
//  main.cpp
//  StarczyJeden
//
//  Created by Filip Jabłoński on 23/10/2020.
//

#include <iostream>
#include <vector>
using std::cin, std::cout, std::endl, std::string;

int main(int argc, const char * argv[])
{
	string input = "\t";
	
	while (input != "" && !cin.eof())
	{
		getline(cin, input);
		
		for (int i = 1; i < argc; i++)
		{
			if(input.find(argv[i]) != string::npos)
			{
				cout << input << endl;
				break;
			}
		}
	}
	
	return 0;
}
