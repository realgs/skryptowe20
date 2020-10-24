#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{

    double sumOfNumbers = 0.0;

    string line;

    while (cin >> line)
    {
        try
        {
            double parameter = stod(line);
            sumOfNumbers += parameter;
        }
        catch (exception &err)
        {
        }
    }

    cout << sumOfNumbers;

    return 0;
}
