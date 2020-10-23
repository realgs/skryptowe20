#include <iostream>
#include <fstream>
#include <sstream>
using namespace::std;

int main(int argc, char* argv[]) {

	double sum = 0.0;

	string token;
	while (cin >> token)
	{
		try {
			sum += stod(token);
		}
		catch (std::exception & e) {}
	}

	cout << sum << endl; 
}
