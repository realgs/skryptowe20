#include <iostream>

const int NO_OCCURANCES = -1;


bool shouldPrintLine(std::string line, std::string * parameters, int parametersSize) {
	int columnStart = 0, columnEnd = -1;

	bool wasLastColumnConsidered = false;
	int tabIndex = line.find('\t', 0);
	while (!wasLastColumnConsidered) {
		columnStart = columnEnd + 1;
		columnEnd = (tabIndex != NO_OCCURANCES) ? tabIndex : line.length();
		for (int i = 0; i < parametersSize; i++) {
			int comparisonResult = line.compare(columnStart, (columnEnd - columnStart), parameters[i]);
			if (comparisonResult == 0)
				return true;
		}

		if (tabIndex != NO_OCCURANCES)
			tabIndex = line.find('\t', columnEnd + 1);
		else
			wasLastColumnConsidered = true;
	}
	return false;
}

void processLine(std::string line, std::string * parameters, int parametersSize) {
	if (shouldPrintLine(line, parameters, parametersSize)) {
		std::cout<<line<<std::endl;
	}
}

int main(int argc, char ** argv) {
	std::string * parameters = new std::string[argc - 1];
	for (int i = 1; i < argc; i++) {
		parameters[i - 1] = argv[i];
	}
	
	std::string line;
	while (getline(std::cin, line)) {
		processLine(line, parameters, argc - 1);
	}
	delete parameters;
}