#ifndef UTIL_H
#define UTIL_H

#include <vector>
#include <set>
#include <string>

// Basic parser that splits arguments into options and parameters (no support for options with parameters).
void parse_args(char** args, int count, std::vector<std::string>& params, std::set<std::string>& switches);

#endif
