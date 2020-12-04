#include <iostream>
#include <string>
#include <vector>

#define DELIMITER_OF_COLUMNS "\t"
#define NO_ARGUMENTS_GIVEN 11
#define WRONG_COLUMN_INDEX 12
#define NO_DELIMITER_DETECTED 13

int getNumberOfLines(std::string text) {
	int numberOfLines = 1;
	size_t separatorIndex = text.find('\n');
	while (text != "" && separatorIndex != std::string::npos) {
			numberOfLines += 1;
			text = text.substr(separatorIndex + 1, text.size());
			separatorIndex = text.find('\n');
	}
	return numberOfLines;
}

int main(int argc, char* argv[], char* env[])
{
	if (argc < 2) { return NO_ARGUMENTS_GIVEN; }
	std::string userInput;
	std::getline(std::cin, userInput, ' ');
	std::vector <std::string> userInputParsedText;
	std::vector <std::string> textToBeDisplayed;
	std::string output = "";
	int numberOfLines = 1;

	while (userInput != "" && userInput.find(DELIMITER_OF_COLUMNS) != std::string::npos) {
		if (numberOfLines == 1) { 
			numberOfLines = getNumberOfLines(userInput);
		}
		if (userInput.find('\n') != std::string::npos) {
			userInput = userInput.replace(userInput.find('\n'), 1, DELIMITER_OF_COLUMNS);
		}
		size_t separatorIndex = userInput.find(DELIMITER_OF_COLUMNS);
		userInputParsedText.push_back(userInput.substr(0, separatorIndex));
		userInput = userInput.substr(separatorIndex + 1, userInput.length());
	}
	userInputParsedText.push_back(userInput);
	for (int i = 1; i < argc; i++) {
		int index = strtol(argv[i], nullptr, 10) - 1;

		if (index < userInputParsedText.size()) {
			int j = index;
			for (int k = 0; k < numberOfLines; k++) {
				if (j % userInputParsedText.size() == index) {
					textToBeDisplayed.push_back(userInputParsedText.at(index));
				}
				j += userInputParsedText.size();
			}
		}
		else {
			return WRONG_COLUMN_INDEX;
		}
	}
	for (int i = 0; i < textToBeDisplayed.size(); i++) {
		if (textToBeDisplayed.at(i) != "") {
		output += textToBeDisplayed.at(i);
		}
		if (i != textToBeDisplayed.size() - 1) {
			output += DELIMITER_OF_COLUMNS;
		}
	}
	std::cout << output;
}