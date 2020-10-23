#include <iostream>
#include <string>
#include <vector>
#include <sstream>

using namespace std;
void sumNumbers() 
{
    double addsum = 0;
    string lines;
    while (cin >> lines)
    {
        try
        {
            addsum += stod(lines);
        }
        catch (exception& e) {}
    }
    cout << addsum << endl;
}
int main(int argc, char* argv[], char* env[])
{
    sumNumbers();
    return 0;
}
