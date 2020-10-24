#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;



int main(int argc, char* argv[]) {

	fstream inputFile("Zakup.txt");
	string date, name, line = "";
	double quantity, prize;

	while (getline(inputFile, line)) {
		istringstream iss(line);

		if (iss >> date >> name >> quantity >> prize) {
			for (int i = 1; i < argc; i++) {
				int argument = atoi(argv[i]);
				switch (argument) {
				case 1:
					cout << date << '\t';
					break;
				case 2:
					cout << name << '\t';
					break;
				case 3:
					cout << quantity << '\t';
					break;
				case 4:
					cout << prize << '\t';
					break;

				}
			}
			cout << endl;
		}



	}
	inputFile.close();
}
