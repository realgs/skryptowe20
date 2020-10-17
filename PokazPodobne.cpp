#include <iostream>
#include <string>


int main(int argc, const char * argv[], char* env[])
{
	if(argc == 1) return 1;

	bool *have_seen = new bool[argc];
	bool isSilent = false;
	std::string silence = argv[1];
	for (int i = 1; i < argc; i++) have_seen[i] = true;

	if(argc > 1 && silence == "/s" || silence == "/S"){
		isSilent = true;
	}
	while (*env != NULL)
	{
		string env_body = string(*env++);
		string envs_name = env_body.substr(0, env_body.find('='));

		for (int i = isSilent ? 2 : 1; i < argc; i++)
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

				std::cout << env_body << std::endl;
				break;
			}
		}
	}

	if(!isSilent)
		for (int i = 1; i < argc; i++)
			if(not_appeared[i]) std::cout << argv[i] << "=NONE" << std::endl;

	return 0;
}
