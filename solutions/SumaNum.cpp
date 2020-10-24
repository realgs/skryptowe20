#include <iostream>
#include <string>

using namespace std;
void sumNumbers(){
    double sum = 0;
    string line;
    
    while (cin >> line){
        try{
            sum += stod(line);
        }
        catch (exception& e){}
    }
    cout << sum << endl;
}

int main(int argc, char* argv[], char* env[]) {
    sumNumbers();
    return 0;
}
