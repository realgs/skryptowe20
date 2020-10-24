#include <iostream>
#include <string>
#include <sstream>

using namespace std;
int main(int argc, char* argv[])
{
    string foo;
    double sum = 0.0;
    double value;
    while (cin >> foo)
    {
        try
        {
            value = stod(foo);
            sum += value;

        }
        catch (const exception& e)
        {

        }
    }
    
    cout << "Sum:" << sum << endl;
    return 0;
}
