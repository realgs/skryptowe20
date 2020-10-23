#include <iostream>
#include <fstream>
#include <vector>

std::vector<std::string> read_file()
{
	const std::string file_path = "Zakup.txt";

	std::ifstream input(file_path);
	std::vector<std::string> output;
	std::string date, name, weight, price;

	while (input >> date >> name >> weight >> price)
	{
		output.push_back(date + "\t" + name + "\t" + weight + "\t" + price);
	}

	return output;
}

std::vector<std::string> extract_arguments(int argc, char* argv[])
{
	std::vector<std::string> args;

	for (int i = 1; i < argc; i++)
	{
		args.push_back(argv[i]);
	}

	return args;
}

void print(std::vector<std::string>& lines, std::vector<std::string>& args)
{
	for (const auto& line : lines)
	{
		for (const auto& arg : args)
		{
			if (line.find(arg) != std::string::npos)
			{
				std::cout << line << "\n";
				break;
			}
		}
	}
}

int main(int argc, char* argv[])
{
	std::vector<std::string> lines = read_file();
	std::vector<std::string> args = extract_arguments(argc, argv);

	print(lines, args);

	return 0;
}

