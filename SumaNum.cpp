#include <iostream>
#include <string>

int main(int argc, char ** argv) {
	double sum = 0.0;
	std::string input;
	while (std::cin >> input) {
		try {
			double number = stod(input);
			sum += number;
		} 
		catch(std::exception &err) {
		}
	}
	std::cout << sum;
	return 0;
}
