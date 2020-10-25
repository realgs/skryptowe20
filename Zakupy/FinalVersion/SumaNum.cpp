#include <iostream>
#include <string>

using namespace std;

bool TryParseDouble(const string& val, double& out)
{
    try
    {
        out = stod(val);
        return true;
    }
    catch (const invalid_argument&)
    {
        return false;
    }
}

int main(int argc, char** argv)
{
    double sum = 0.;
    string inputStr;

    while (getline(cin, inputStr))
    {
        double currentNumber;
        if (TryParseDouble(inputStr, currentNumber))
        {
            sum += currentNumber;
        }
    }

    cout << "Total sum: " << sum << endl;
}