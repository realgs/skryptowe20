#include <iostream>
#include <vector>
#include <string>

std::vector<std::string> extract_arguments(int argc, char* argv[])
{
	std::vector<std::string> args;

	for (int i = 1; i < argc; i++)
	{
		args.push_back(argv[i]);
	}
	return args;
}

float convert_arg_to_number(std::string arg)
{
	float out_value = 0;

	try
	{
		out_value = std::stof(arg, nullptr);
	}
	catch (const std::invalid_argument& ia)
	{
		out_value = 0;
	}

	return out_value;
}

std::vector<float> convert_args_to_floats(std::vector<std::string> args)
{
	std::vector<float> output;

	for (const auto& arg : args)
	{
		float converted = convert_arg_to_number(arg);
		if (converted != 0)
		{
			output.push_back(converted);
		}
	}

	return output;
}

float sum_of_vector(std::vector<float> args)
{
	float sum = 0;

	for (const auto& arg : args)
	{
		sum += arg;
		std::cout << "sum: " << sum << "\n";
	}

	return sum;
}

int main(int argc, char* argv[])
{
	std::vector<std::string> args = extract_arguments(argc, argv);
	std::vector<float> parsed_args = convert_args_to_floats(args);

	std::cout << sum_of_vector(parsed_args);

	return 0;
}