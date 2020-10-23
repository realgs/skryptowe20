#include <iostream>
#include <string>
using namespace std;

int main(int argc, char* argv[]) {

    string line;
    double sum = 0.0;
    while (getline(cin, line)) {sum += atof(line.c_str());}
    cout << sum;
    
}
