#include <iostream>
#include <string>

using namespace std;

double calculateSum() {
	string number;
	double sum = 0.0;

	while (!cin.eof()) {
		number = "";
		cin >> number;

		try {
			sum += stod(number);
		}
		catch (invalid_argument exc) {};
	}
	return sum;
}

int main()
{
	cout << calculateSum();
}
