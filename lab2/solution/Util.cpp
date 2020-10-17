#include "Util.h"

void parse_args(char** args, const int count, std::vector<std::string>& params, std::set<std::string>& switches) {
    for(int i = 1; i < count; ++i) {
        if(args[i][0] == '/')
            switches.insert(args[i]);
        else
            params.push_back(args[i]);
    }
}
