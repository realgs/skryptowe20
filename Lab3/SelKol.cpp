#include <iostream>
#include <fstream>
#include <vector>

namespace
{
	constexpr int max_column_index = 3;
	constexpr int min_column_index = 0;
};

struct Product
{
	Product(std::string date, std::string name, std::string weight, std::string price)
	{
		values_.push_back(date);
		values_.push_back(name);
		values_.push_back(weight);
		values_.push_back(price);
	}
	std::vector<std::string> values_;
};

std::vector<Product> read_file()
{
	const std::string file_path = "Zakup.txt";

	std::ifstream input(file_path);
	std::vector<Product> output;
	std::string date, name, weight, price;

	while (input >> date >> name >> weight >> price)
	{
		output.push_back(Product(date, name, weight, price));
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

int convert_arg_to_int(std::string arg)
{
	return ((arg[0] - '0') - 1);
}

bool is_arg_valid(std::string arg)
{
	return arg.size() == 1 and convert_arg_to_int(arg) >= min_column_index
		   and convert_arg_to_int(arg) <= max_column_index;
}

std::vector<int> convert_args_to_int(std::vector<std::string> args)
{
	std::vector<int> output;

	for (const auto& arg : args)
	{
		if (is_arg_valid(arg))
		{
			output.push_back(convert_arg_to_int(arg));
		}
	}

	return output;
}

void print(std::vector<int> indexes, std::vector<Product> products)
{
	for (const auto& index : indexes)
	{
		for (const auto& product : products)
		{
			std::cout << product.values_[index] << "\t";
		}
		std::cout << "\n";
	}
}

int main(int argc, char* argv[])
{
	std::vector<Product> products = read_file();
	std::vector<std::string> args = extract_arguments(argc, argv);
	std::vector<int> parsed_args = convert_args_to_int(args);

	print(parsed_args, products);

	return 0;
}