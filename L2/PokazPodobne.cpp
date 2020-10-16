#include <iostream>
#include <string>

using std::cout, std::endl, std::string;

int main(int argc, const char * argv[], char* env[])
{
	if(argc == 1) return 1;
	
	bool *not_appeared = new bool[argc];
	for (int i = 1; i < argc; i++) not_appeared[i] = true;
	
	bool silent_mode = (argv[1][0] == '/' && argv[1][2] == '\0' && (argv[1][1] == 'S' || argv[1][1] == 's'));
	
	while (*env != NULL)
	{
		string env_body = string(*env++);
		string envs_name = env_body.substr(0, env_body.find('='));
		
		for (int i = silent_mode ? 2 : 1; i < argc; i++)
		{
			if(envs_name.find(argv[i]) != string::npos)
			{
				not_appeared[i] = false;
				
				long position = env_body.find(';');
				while (position != string::npos)
				{
					env_body.replace(position, 1, "\n");
					position = env_body.find(';');
				}
				
				cout << env_body << endl;
				break;
			}
		}
	}
	
	if(!silent_mode)
		for (int i = 1; i < argc; i++)
			if(not_appeared[i]) cout << argv[i] << "=NONE" << endl;
	
	return 0;
}
