#include <iostream>
#include <string>
#include <vector>

#define DELIMITER_OF_COLUMNS "\t"
#define NO_ARGUMENTS_GIVEN 11
#define WRONG_COLUMN_INDEX 12
#define NO_DELIMITER_DETECTED 13

int main(int argc, char* argv[], char* env[])
{   
    std::cout << "Podaj tekst to slekecji kolumn (wyrazy oddzielone oddzielone tabluacją:" << std::endl;
    std::string userInput;
    std::getline(std::cin, userInput);
    std::vector <std::string> textToBeDisplayed;

    while (userInput != "" && userInput.find(DELIMITER_OF_COLUMNS) != std::string::npos) {
        size_t separatorIndex = userInput.find(DELIMITER_OF_COLUMNS);
        textToBeDisplayed.push_back(userInput.substr(0, separatorIndex));
        userInput = userInput.substr(separatorIndex + 1, userInput.length());
    }
    textToBeDisplayed.push_back(userInput);
    if (argc < 2) { return NO_ARGUMENTS_GIVEN; }
    for (int i = 1; i < argc; i++) {
        int index = strtol(argv[i], nullptr , 10) - 1;
        if (index < textToBeDisplayed.size()) {
            std::cout << textToBeDisplayed.at(index) << DELIMITER_OF_COLUMNS;
        } 
        else {
            return WRONG_COLUMN_INDEX;
        }
    }
}