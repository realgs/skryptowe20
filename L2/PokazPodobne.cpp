#include <iostream>
#include <string>

int main(int argc, char* argv[], char* env[])
{
	if (argc == 1)
	{
		return 0;
	}


	bool isSilence = false;
	std::string silence_text = argv[1];
	if (argc > 1 && (silence_text == "/s" || silence_text == "/S"))
	{
		isSilence = true;
	}

	bool* isSubstr = new bool[argc-2];
	for (int i = 0; i < argc - 2; i++)
	{
		isSubstr[i] = false;
	}

	while (*env != NULL)
	{
		std::string env_str = *env;
		std::string var_name = env_str.substr(0, env_str.find("="));
		std::string var_content = env_str.substr(env_str.find("=")+1);
		while (var_content.find(";") != std::string::npos)
		{
			var_content.replace(var_content.find(";"), 1, "\n");
		}

		bool isWritten = false;
		if (!isSilence)
		{
			std::string argv_str = argv[1];
			if (var_name.find(argv_str) != std::string::npos)
			{
				isWritten = true;
				std::cout << var_name << "=" << var_content << "\n";
			}
		}
		for (int i=2; i < argc; i++)
		{
			std::string argv_str = argv[i];
			if (var_name.find(argv_str) != std::string::npos)
			{
				if (!isWritten)
				{
					isWritten = true;
					std::cout << var_name << "=" << var_content << "\n";
				}
				isSubstr[i-2] = true;
			}
		}
		*env++;
	}

	std::cout << "\n";
	
	if (!isSilence)
	{
		for (int i=2; i < argc; i++)
		{
			if (!isSubstr[i - 2])
			{
				std::cout << argv[i] << " = NONE\n";
			}
		}
	}
}

