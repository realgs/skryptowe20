#include <iostream>
#include <fstream>
#include <sstream>
using namespace::std;

int main(int argc, char* argv[]) {
	
	for (std::string line; getline(cin, line); )
	{
		string date, product;
		double weight, price;
		
		std::istringstream iss(line);
		if (iss >> date >> product >> weight >> price) {
			for (int i = 1; i < argc; i++) {

				if (atoi(argv[i]) == 1) {
					cout << date << '\t';
				}
				else if (atoi(argv[i]) == 2) {
					cout << product << '\t';
				}
				else if (atoi(argv[i]) == 3) {
					cout << weight << '\t';
				}
				else if (atoi(argv[i]) == 4) {
					cout << price << '\t';
				}
			}
			cout << endl;
		}
	}
}
