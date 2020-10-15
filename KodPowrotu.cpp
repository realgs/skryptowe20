#include <iostream>
#include <string>
using namespace std;

bool isSilent(char* ctab[])
{
	while (*ctab != NULL)
		if (*ctab++ == (string)"/S")
			return true;

	return false;
}

int main(int argc, char* argv[]){

	bool is_silent = isSilent(argv);

	int i = 1;
	if (is_silent){
		argc--;
		i++;
	}
	int return_code = 11;

	if (argc == 2 && isdigit(*argv[i]) && strlen(argv[i]) == 1){
		return_code = atoi(argv[i]);
	}
	else if (argc > 2){
		return_code = 13;
	}
	else if (argc == 2){
		return_code = 12;
	}
	if (!is_silent){
		puts(std::to_string(return_code).c_str());
	}
	return return_code;
}
