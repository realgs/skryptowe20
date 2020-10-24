#include <iostream>
#include <vector>
#include <sstream>

#define DELIMITER '\t'

int main(int argc, char* argv[]) {
	std::vector<int> columns_ids;
	std::string line;

	for (int i = 1; i < argc; i++) {
		columns_ids.push_back(atoi(argv[i]));
	}

	while (std::getline(std::cin, line)) {
		std::vector<std::string> elems;
		std::stringstream line_stream(line);
		std::string elem;

		while (std::getline(line_stream, elem, DELIMITER)) {
			elems.push_back(elem);
		}

		for (int i = 0; i < columns_ids.size(); i++) {
			if (columns_ids.at(i) < elems.size()) {
				std::cout << elems.at(columns_ids.at(i)) << DELIMITER;
			}
		}
		std::cout << std::endl;
	}

	return 0;
}
