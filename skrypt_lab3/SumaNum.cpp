#include <iostream>
#include <fstream>
#include <sstream>
using namespace::std;

int main(int argc, char* argv[]) {

	fstream MyFile("Zakup.txt");

	double sum = 0.0;

	for (std::string line; getline(MyFile, line); )
	{
		string a, b;
		double c, d;

		std::istringstream iss(line);
		if (iss >> a >> b >> c >> d)
			sum += c + d;
	}

	cout << sum; 
	MyFile.close();

}