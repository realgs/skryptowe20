
#include <string>
using namespace std;

bool silentMode(char* tab[])
{
	while (*tab != NULL)
		if (*tab++ == (string)"/S")
			return true;

	return false;
}
int main(int argc, char* argv[]){

	bool is_silent = silentMode(argv);
	int code = 11;
	int i = 1;
	if (is_silent){
		argc--;
		i++;
	}

	if (argc == 2 && isdigit(*argv[i]) && strlen(argv[i]) == 1){
		code = atoi(argv[i]);
	}
	else if (argc == 2) {
		code = 12;
	}
	else if (argc > 2){
		code = 13;
	}	
	if (!is_silent){
		puts(std::to_string(code).c_str());
	}
	return code;
}


