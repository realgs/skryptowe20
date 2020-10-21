#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
int main(int argc, char *argv[], char *env[])
{
    double sum = 0;
    string token;
    while(cin >> token)
    {
        try{
            sum += stod(token);
        } catch (std::exception& e){}
    }
    cout << sum << endl;
    return 0;
}
