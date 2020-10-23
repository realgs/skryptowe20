#include <string>
#include <regex>
#include <vector>
using namespace std;
int main(int argc, char* argv[])
{
    fstream file;
    string word;
    int numberOfColumns = 4;

    vector<regex> phrase;
    string line;
    for (int i = 1; i < argc; i++) {
        phrase.push_back(regex(argv[i]));
    }
    while (getline(cin, line)) {
        for (int i = 0; i < phrase.size(); i++) {
            if (regex_search(line, phrase[i])) {
                cout << line << endl;
                break;
            }

        }

    }
}
