#include <vector>
#include <iostream>
#include <sstream>

using namespace std;

int main (int argc, char* argv[]) {
    vector<int> cols;

    for (int i = 1; i < argc; i++) {
        int temp = atoi(argv[i]);

        if (temp != 0) {
            cols.push_back(temp);
        }
    }

    while (!cin.eof()) {
        string line;

        getline(cin, line);
        stringstream iss(line);

        string word;
        line = "";
        int i = 0;
        int j = 0;
        while(iss >> word) {
            if (j < cols.size() && i == cols.at(j) - 1) {
                line += word;
                line += "\t";
                j++;
            }
            i++;
        }
        if (line != "") {
            cout << line << endl;
        }

    }

    return 0;
}
