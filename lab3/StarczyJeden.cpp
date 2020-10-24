#include <string>
#include <iostream>

bool isThereAnyOfParameters(int argc, char* argv[], std::string line) {
	for (int i = 0; i < argc; i++) {
		if (line.find(argv[i]) != std::string::npos) {
			return true;
		}
	}
	return false;
}

int main(int argc, char* argv[]) {
	std::string line;
	while (std::getline(std::cin, line)) {
		if (isThereAnyOfParameters(argc, argv, line)) {
			std::cout << line << "\n";
		}
	}
}
