
#include <iostream>
#include <string>
#include <vector>

std::vector<std::string> divideIntoColumns(std::string line) {
	std::vector<std::string> columns;
	std::size_t nextColumnIndex = line.find('\t');
	while (nextColumnIndex != std::string::npos) {
		columns.push_back(line.substr(0, nextColumnIndex));
		line = line.substr(nextColumnIndex + 1);
		nextColumnIndex = line.find('\t');
	}
	columns.push_back(line);
	return columns;
}

void printSelectedColumns(std::vector<int> indexesOfColumns, std::vector<std::string> columns) {

	for (int columnIndex : indexesOfColumns) {
		if (columnIndex < columns.size()) {
			std::cout << columns[columnIndex] << '\t';
		}
	}
	std::cout << "\n";
}

int main(int argc, char* argv[], char* env[]) {
	std::string line;
	std::vector<int> indexesOfColumns;
	for (int i = 1; i < argc; i++) {
		indexesOfColumns.push_back(atoi(argv[i])-1);
	}
	while(std::getline(std::cin, line)) {
		std::vector<std::string> columns = divideIntoColumns(line);
		printSelectedColumns(indexesOfColumns, columns);
	}
}
