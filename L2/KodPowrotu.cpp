#include <iostream>
using namespace std;
bool isSilent(char* tab[])
{
	string argument;
	while (*tab != NULL)
	{
		argument = *tab++;
		if (argument == "/S" || argument == "/s") return true;
	}
	return false;
}
int chceckNumber(int argc, char* argv[]) {
	if (!isSilent(argv))
	{
		puts("Argumenty programu");
		if (argc == 2 && isdigit(*argv[1])) {

				puts(argv[1]);

				return int(argv[1]);
				
		}
		else if (argc == 2 && !isdigit(*argv[1])) {
			puts("12");
			return 12;
		}
		else if (argc == 1) {
			puts("11");
			return 11;
		}
		else if (argc > 2) {
			puts("13");
			return 13;
		}

	}
	else 
	{
		if (argc == 3 && isdigit(*argv[2])) {
			for (int k = 0; k < argc; k++)
				return int(argv[k]);
		}
		else if (argc == 3 && !isdigit(*argv[2])) {
			
			return 12;
		}
		else if (argc == 2) {
			
			return 11;
		}
		else if (argc > 3) {
			
			return 13;
		}
	}
	
}
int main(int argc, char* argv[])
{
	return chceckNumber(argc, argv);
}
