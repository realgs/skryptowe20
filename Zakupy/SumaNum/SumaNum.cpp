#include <iostream>
#include <string>

using namespace std;

bool TryParseDouble(const char* val, double& out)
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
    argv++; // Skip filename
    double sum = 0.;

    while (*argv != NULL)
    {
        double currentNumber;
        if (TryParseDouble(*argv++, currentNumber))
        {
            sum += currentNumber;
        }
    }

    cout << "Total sum: " << sum << endl;
}