#include <iostream>
#include <fstream>
#include <sstream>
using namespace::std;

int main(int argc, char* argv[]) {

	for (string line; getline(cin, line); ) {
		string date, product;
		double weight, price;

		std::istringstream iss(line);
		if (iss >> date >> product >> weight >> price) {
			for (int i = 1; i < argc; i++) {
				if (argv[i] == date || argv[i] == product || atof(argv[i]) == weight || atof(argv[i]) == price) 
					cout << line << endl;	
			}
		}
	}

}
