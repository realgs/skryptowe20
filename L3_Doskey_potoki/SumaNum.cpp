#include <vector>
#include <iostream>

using namespace std;

int main (int argc, char* argv[]) {
    float sum = 0;
    string word;

    while (cin >> word) {
        try {
            sum += stof(word);
        } catch (exception e) {}
    }
    cout << sum << endl;

    return 0;
}
