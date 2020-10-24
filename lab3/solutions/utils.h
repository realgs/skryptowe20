#include <vector>
#include <iostream>
#include <string>

std::vector<int> charToIntVector(int argc, char const *argv[]);

std::vector<std::string> split(std::string s, std::string splitter);

bool contains(std::string source, std::string sub);

double convertToDouble(std::string s);

std::vector<double> convertToDoubleVector(std::vector<std::string>);
