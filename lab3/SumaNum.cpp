#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;



int main(int argc, char* argv[]) {

	fstream inputFile("Zakup.txt");
	string date, name, line = "";
	double quantity, prize, sum = 0;

	while (getline(inputFile, line)) {
		istringstream iss(line);

		if (iss >> date >> name >> quantity >> prize)
			sum += (quantity + prize);
	}
	cout << sum;
	inputFile.close();
}
