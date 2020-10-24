#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
void showSelectedColumns(int argc, char* argv[]){
    string line;
    vector <int> selected_columns;
    for (int i = 1; i < argc; i++){
        selected_columns.push_back(atoi(argv[i]));
    }

    while(getline(cin,line)){
        vector <string> parts;
        istringstream isstream(line);
        string part;
        while (getline(isstream, part, '\t')){
            parts.push_back(part);
        }
        for (int i = 0; i < selected_columns.size(); i++){
            if (selected_columns[i] - 1 < parts.size()){
                cout << parts[selected_columns[i] - 1] << '\t';
            }
        }
        cout << endl;
    }
}

int main(int argc, char* argv[], char* env[]) {
    showSelectedColumns(argc, argv);
    return 0;
}
