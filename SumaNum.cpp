#include <iostream>
#include <fstream>

int main(int argc, char *argv[]) {
    std::ifstream infile(
            "/Users/piotrrasinski/OneDrive - Politechnika Wroclawska/Semestr5/Skryptowe_L/skryptowe20/zakupy.txt");

    int counter = 0;
    double sum = 0.0;
    std::string word;
    while (infile >> word) {
        if (counter == 2) {
            sum += std::stod(word);
            counter++;
        } else if (counter == 3) {
            sum += std::stod(word);
            counter = 0;
        } else {
            counter++;
        }
    }
    std::cout << sum << std::endl;
    return 0;
}