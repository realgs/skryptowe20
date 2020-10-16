#include <iostream>

using std::cout, std::endl, std::string;

int obtain_result(const char *argument)
{
	if(argument[1] == '\0')
	{
		if(argument[0] >= '0' && argument[0] <= '9') return argument[0] - '0';
		else return 12;
	}
	else return 12;
}

int main(int argc, const char * argv[])
{
	if(argc == 1)
	{
		cout << 11 << endl;
		return 11;
	}

	bool silent_mode = (argv[1][0] == '/' && argv[1][2] == '\0' && (argv[1][1] == 'S' || argv[1][1] == 's'));
	
	int return_value = 0;
	
	if(argc == 2) return_value = obtain_result(argv[1]);
	if(argc == 3) return_value = silent_mode ? obtain_result(argv[2]) : 13;
	if(argc > 3) return_value = 13;
	
	if(!silent_mode) cout << return_value << endl;

	return return_value;
}
