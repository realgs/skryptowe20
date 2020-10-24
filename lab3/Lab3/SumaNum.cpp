#include <iostream>
#include <string>
#include <regex>
using namespace std;

bool isNumber(string test)
{
	return regex_match(test, regex(("((\\+|-)?[[:d:]]+)(\\.(([[:d:]]+){1}))?")));
	//return regex_match(test, regex(("((\\+|-)?[[:d:]]+)(\\.(([[:d:]]+)?))?"))); // wersja akceptujaca 5. jako liczbe 
}

void sumNumbers()
{
	double sum = 0;
	string lines;
	while (cin >> lines)
	{
		if(isNumber(lines)) sum += stod(lines);
	}
	cout << sum << endl;
}
int main(int argc, char* argv[])
{
	sumNumbers();
	return 0;
}
