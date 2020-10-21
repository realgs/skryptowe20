#include <iostream>
#include <fstream>
#include <sstream>
using namespace::std;

int main(int argc, char* argv[]) {
	
	fstream MyFile("Zakup.txt");
	
	for (std::string line; getline(MyFile, line); )
	{
		string a, b;
		double c, d;
		
		std::istringstream iss(line);
		if (iss >> a >> b >> c >> d) {
			for (int i = 1; i < argc; i++) {

				if (atoi(argv[i]) == 1) {
					cout << a << '\t';
				}
				else if (atoi(argv[i]) == 2) {
					cout << b << '\t';
				}
				else if (atoi(argv[i]) == 3) {
					cout << c << '\t';
				}
				else if (atoi(argv[i]) == 4) {
					cout << d << '\t';
				}
				
			}
			cout << '\n';
		}
	}

	MyFile.close();

}