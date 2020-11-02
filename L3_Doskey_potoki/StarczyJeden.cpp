#include <vector>
#include <iostream>

using namespace std;

int main (int argc, char* argv[]) {
    vector<string> w;

    for (int i = 1; i < argc; i++) {
        w.push_back(argv[i]);
    }

    while (!cin.eof()) {
        bool found = false;
        string line;

        getline(cin, line);
        for (auto & i : w) {
            if (!found && line.find(i) != std::string::npos) {
                cout << line << endl;
                found = true;
            }
        }
    }

    return 0;
}
