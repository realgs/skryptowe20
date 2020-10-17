#include <iostream>



int main(int argc, const char * argv[])
{
	if (argc == 1)
	{
		std::cout << 11;
		return 11;
	}
	
	
	bool isSilence = false;
	std::string silence_text = argv[1];
	if (argc > 1 && (silence_text == "/s" || silence_text == "/S"))
	{
		isSilence = true;
	}


	if (argc == 2)
	{
		if (argv[1][1] == NULL && argv[1][0] >= 48 && argv[1][0] <= 57) //ASCII: '0'=48, '9'=57
		{
			std::cout << argv[1];
			return argv[1][0] - 48;
		}
		else
		{
			if (!isSilence)
			{
				std::cout << 12;
				return 12;
			}

			return 11;
		}
			
	}
	
	if (argc == 3 && isSilence)
	{
		if (argv[2][1] == NULL && argv[2][0] >= 48 && argv[2][0] <= 57)
		{
			return argv[2][0] - 48;
		}
		else
			return 12;
	}

	if(!isSilence)
		std::cout << 13;

	return 13;

	
}

