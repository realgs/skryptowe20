#include <iostream>
#include <string>

const int NO_OCCURANCES = -1;

int indexOf(int* arr, int arrSize, int toFind) {
	for (int i = 0; i < arrSize; i++) {
		if (arr[i] == toFind)
			return i;
	}
	return -1;
}

void printString(std::string toPrint, int firstIndex, int lastIndex, char endChar) {
	for (int i = firstIndex; i <= lastIndex; i++) {
		std::cout << toPrint[i];
	}
	std::cout << endChar;
}

void processIndexes(int* beginIndexes, int* endIndexes, int arrSize, std::string line) {
	for (int i = 0; i < arrSize; i++) {
		if (beginIndexes[i] != 0 || endIndexes[i] != 0) {
			printString(line, beginIndexes[i], endIndexes[i], '\t');
		}
	}
}

void processLine(std::string line, int* columnIndexes, int columnIndexesSize) {
	int* beginIndexes = new int[columnIndexesSize];
	int* endIndexes = new int[columnIndexesSize];
	bool wasLastColumnConsidered = false;

	int columnIndex = 0, columnStart = 0, columnEnd = -1;
	int tabIndex = line.find('\t', 0);
	while (!wasLastColumnConsidered) {
		columnStart = columnEnd + 1;
		columnEnd = (tabIndex != NO_OCCURANCES) ? tabIndex : line.length() - 1;
		int columnOrder = indexOf(columnIndexes, columnIndexesSize, columnIndex);
		if (columnOrder != NO_OCCURANCES) {
			beginIndexes[columnOrder] = columnStart;
			endIndexes[columnOrder] = columnEnd;
		}
		columnIndex++;

		if (tabIndex != NO_OCCURANCES)
			tabIndex = line.find('\t', columnEnd + 1);
		else
			wasLastColumnConsidered = true;
	}
	processIndexes(beginIndexes, endIndexes, columnIndexesSize, line);
	delete beginIndexes;
	delete endIndexes;
}

int main(int argc, char** argv) {
	int* columnsIndexes = new int[argc - 1];
	for (int i = 1; i < argc; i++) {
		columnsIndexes[i - 1] = std::stoi(argv[i]);
	}
	std::string line;
	int previousIndex = -1;
	while (getline(std::cin, line)) {
		processLine(line, columnsIndexes, argc - 1);
		std::cout << std::endl;
	}
	delete columnsIndexes;
}