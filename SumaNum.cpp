// Skryptowe_lab3.cpp : Ten plik zawiera funkcję „main”. W nim rozpoczyna się i kończy wykonywanie programu.
//

#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <vector>
using namespace std;
int main(int argc, char* argv[])
{
    double amount = 0;
    string number;
    while (cin >> number)
    {
        amount += stod(number);
    }
    cout << amount << endl;
    return 0;
    
}

