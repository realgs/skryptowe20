#include <iostream>
#include <vector>
#include <sstream>

int main(int argc, char* argv[]) {
	std::string line;

	while (std::getline(std::cin, line)) {
		for (int i = 0; i < argc; i++) {
			size_t position = line.find(argv[i]);
			if (position != std::string::npos) {
				std::cout << line << std::endl;
			}
		}
	}

	return 0;
}
