#include <iostream>
using std::cout, std::endl;

int main(int argc, const char * argv[], char* env[])
{
	cout << "argumenty programu:\n";
	for (int i = 0; i < argc; i++) cout << argv[i] << endl;
	
	cout << "zmienne srodowiska:\n";
	while (*env != NULL) cout << *env++ << endl;
	
	return 10;
}
