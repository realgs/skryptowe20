#include <iostream>
#include <vector>
#include <sstream>

int main(int argc, char* argv[]) {
	double sum = 0.0;
	int num_of_dots = 0;
	std::string line;
	std::string number_str = "";

	while (std::getline(std::cin, line)) {
		for (int i = 0; i < line.length(); i++) {
			if (isdigit(line[i]) || (line[i] == '.' && number_str.length() > 0)) {
				if (line[i] == '.') {
					num_of_dots++;
				}
				number_str += line[i];

			}
			else {
				if (num_of_dots <= 1) {
					sum += std::atof(number_str.c_str());
				}
				number_str = "";
				num_of_dots = 0;
			}
		}

		if (number_str.length() > 0) {
			if (num_of_dots <= 1) {
				sum += std::atof(number_str.c_str());
			}
			number_str = "";
			num_of_dots = 0;
		}
	}
	std::cout << sum;

	return 0;
}
