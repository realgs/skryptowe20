#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[], char* env[]) {
	string value;
	double result = 0;

	while (cin >> value) {
		try {
			double parsed = stod(value);
			result += parsed;
		}
		catch (invalid_argument e) {
			continue;
		}
	}
	cout << result;
}
