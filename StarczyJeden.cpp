#include <iostream>
#include <fstream>
#include <vector>

int main(int argc, char *argv[]){
    std::ifstream infile(
            "/Users/piotrrasinski/OneDrive - Politechnika Wroclawska/Semestr5/Skryptowe_L/skryptowe20/zakupy.txt");

    std::string input_line;
    std::vector<std::string> output_rows;
    while (std::getline(infile, input_line)) {
        for (int i = 1; i < argc; i++) {
            if (input_line.find(argv[i]) != std::string::npos)
                output_rows.push_back(input_line);
        }
    }
    if (!output_rows.empty()) {
        for (std::string& s : output_rows)
            std::cout << s << std::endl;
    }
    return 0;
}