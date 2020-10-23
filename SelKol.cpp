#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
using namespace std;

int main(int argc, char* argv[]) {

    string line;
    while (getline(cin, line)) {
        vector<string> items;
        stringstream ss(line);
        string token;
        while (getline(ss, token, '\t')) {
            items.push_back(token);
        }
        for (int i = 1; i < argc; i++) {
            int index = atoi(argv[i]);
            if (index <=4  && index>0) cout << items.at(index-1)<<"\t";
        }
        cout << endl;
    }
}

