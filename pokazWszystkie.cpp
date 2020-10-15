#include <iostream>

int main(int argc, char* argv[], char* envp[])
{
	std::cout<<"Arguments (including name of the file):\n";

	for (int i = 0; i < argc; i++)
	{
		std::cout<<(argv[i])<<std::endl;
	}
	std::cout<<"\nEnvironment variables:\n";

	while (*envp != nullptr)
	{
		std::cout<<(*envp++)<<std::endl;
	}
	return 0;
}
