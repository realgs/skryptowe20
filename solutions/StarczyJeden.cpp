#include <iostream>
#include <string>

using namespace std;

void findInLine(int argc, char* argv[]){
    string line;

    while (getline(cin, line)){
        for (int i = 1; i < argc; i++){
            if (line.find(argv[i]) != string::npos){
                cout << line << endl;
                break;
            }
        }
    }
}

int main(int argc, char* argv[]){
    findInLine(argc, argv);
    return 0;
}
