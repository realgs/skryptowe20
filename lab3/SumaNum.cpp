#include <iostream>
#include <cctype>
#include <string>

double getSumFromOneLine(std::string line) {
	double sum = 0;
	std::string num = "";
	bool isDouble = false;
	for (int i = 0; i < line.length(); i++) {
		if (std::isdigit(line[i])) {
			num += line[i];
		} else if (line[i] == '-') {
			if (num.length() == 0) {
				num += '-';
			} else {
				sum += std::stod(num);
				num = "-";
				isDouble = false;
			}
		} else if (line[i] == '.') {
			if (isDouble) {
				sum += std::stod(num);
				num = "0.";
			} else {
				num += '.';
				isDouble = true;
			}
		} else if (num.length() > 0) {
			sum += std::stod(num);
			num = "";
			isDouble = false;
		}
	}
	if (num.length() > 0) {
		sum += std::stod(num);
	}
	return sum;
}

double getSumFromInput() {
	std::string line;
	double sum = 0;
	while (std::getline(std::cin, line)) {
		sum += getSumFromOneLine(line);
	}
	return sum;
}


int main() {
	std::cout << getSumFromInput() << "\n";
}
