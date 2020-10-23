#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main(int argc, char* argv[]) {

    string line;
    while (getline(cin, line)) {
        for (int i = 1; i < argc; i++) {
            size_t found = line.find(argv[i]);
            if (found != std::string::npos) {
                cout << line << endl;
                break;
            }
        }
    }

}
