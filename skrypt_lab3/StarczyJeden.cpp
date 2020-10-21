#include <iostream>
#include <fstream>
#include <sstream>
using namespace::std;

int main(int argc, char* argv[]) {

	fstream MyFile("Zakup.txt");

	for (std::string line; getline(MyFile, line); ) {
		string a, b;
		double c, d;

		std::istringstream iss(line);
		if (iss >> a >> b >> c >> d) {
			for (int i = 1; i < argc; i++) {
				if (argv[i] == a || argv[i] == b || atof(argv[i]) == c || atof(argv[i]) == d) {
					cout << line;
					cout << '\n';
				}
			}
		}
	}

	MyFile.close();

}