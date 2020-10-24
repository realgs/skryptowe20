#include <iostream>
#include <string>
#include <vector>
#include <sstream>

const int TOO_MANY_ARGS = 1;
const int INVALID_ARGS = 2;

int main(int argc, char* argv[]) {

    if (argc > 5) {
        return TOO_MANY_ARGS;
    }

    for (int i = 0; i < argc; i++)
        if (atoi(argv[i]) > 4)
            return INVALID_ARGS;

    std::string line;

    while (std::getline(std::cin, line)) {

        std::vector<std::string> line_content;
        std::istringstream iss(line);
        std::string part;

        while(std::getline(iss, part, '\t'))
            line_content.push_back(part);

        for (int i = 1; i < argc; i++)
            std::cout<<line_content[atoi(argv[i]) - 1]<<'\t';

        std::cout<<'\n';
    }

    return 0;
}
