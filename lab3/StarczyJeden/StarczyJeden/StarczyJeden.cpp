#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

#define FILE_DELIMETER "."
#define PROPER_FILE_FORMAT "txt"
#define NOT_ENOUGH_PARAMETERS 11
#define NO_FILE_PRESENT 12
#define NOT_PROPER_FILE_FORMAT 13
#define COULD_NOT_OPEN_FILE 14

bool isFilePresent(char* argv[], int argc) {
	std::string fileName(argv[argc - 1]);
	size_t fileDelimIndex = fileName.find(FILE_DELIMETER);
	if (fileDelimIndex != std::string::npos) {
		std::string fileExtension = fileName.substr(fileDelimIndex, fileName.size());
		if (fileExtension.find(PROPER_FILE_FORMAT) != std::string::npos) {
			return true;
		}
		else {
			return NOT_PROPER_FILE_FORMAT;
		}
		
	}
	return false;
}

size_t findCaseInsensitive(std::string dataToSearchIn, std::string dataToFind) {
	std::transform(dataToSearchIn.begin(), dataToSearchIn.end(), dataToSearchIn.begin(), ::tolower);
	std::transform(dataToFind.begin(), dataToFind.end(), dataToFind.begin(), ::tolower);
	return dataToSearchIn.find(dataToFind);
}

int main(int argc, char* argv[], char* env[])
{
	if (argc < 2) { return NOT_ENOUGH_PARAMETERS; }
	if (!isFilePresent(argv, argc)) { return NO_FILE_PRESENT; }
	else {
		std::string argumentToFind;
		std::string line;
		std::string fileName(argv[argc - 1]);
		std::ifstream file(fileName);
		if (file) {
			while (std::getline(file, line)) {
				for (int i = 1; i < argc - 1; i++) {
					argumentToFind = argv[i];
					if (findCaseInsensitive(line, argumentToFind) != std::string::npos) {
						std::cout << line << std::endl;
						break;
					}
				}
			}
			file.close();
		}
		else {
			return COULD_NOT_OPEN_FILE;
		}
	}
}
