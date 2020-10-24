#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

int main(int argc, char* argv[]) {

    std::string line;
    int columnMaxAmount = 4;
    
    while (getline(std::cin, line)) {
        std::vector<std::string> tokens;
        std::stringstream stringStream(line);
        std::string token;
        int i = 0;
        
        while (getline(stringStream, token, '\t')) {
            tokens.push_back(token);
        }
        
        for (int i = 1; i < argc; i++) {
            int column = atoi(argv[i]);
            if (column > 0 && column <= columnMaxAmount) {
                std::cout << tokens.at(column - 1) << "\t";
            }
        }
        
        std::cout << std::endl;
    }
}
