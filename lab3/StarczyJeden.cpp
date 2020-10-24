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

		if (iss >> date >> name >> quantity >> prize) {

			for (int i = 1; i < argc;i++) {
				if (argv[i] == date || argv[i] == name)
					cout << line << '\n';
				else if (atof(argv[i]) == quantity || atof(argv[i]) == prize)
					cout << line << '\n';

			}
		}
			
	}
	cout << sum;
	inputFile.close();
}
