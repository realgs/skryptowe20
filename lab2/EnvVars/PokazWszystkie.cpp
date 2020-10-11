
#include <iostream>
using namespace std;

int main(int argc, char** argv, char** env)
{
    cout << "Zmienne srodowiska: " << endl;
	while (*env != NULL)
	{
		cout << *env++ << endl;
	}

	cout << "Parametry programu: " << endl;
	while (*argv != NULL)
	{
		cout << *argv++ << endl;
	}
}