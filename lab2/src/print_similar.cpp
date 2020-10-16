#include <iostream>
#include "input_switches.hpp"

constexpr int NOT_FOUND = -1;

size_t count_env_variables(char **env)
{
    size_t count = 0;
    while (*env++ != nullptr)
        count++;
    return count;
}

bool split_and_print(const char *const arg, char **env, bool *if_env_printed)
{
    bool if_found = false;
	size_t i = 0;
	while (*env != nullptr)
	{
		// check if arg is a substring
		if (std::strstr(*env, arg))
		{
			// check if this env var was printed
			if_found = true;
			if (!(if_env_printed[i]))
			{
				char* token = std::strtok(*env, "=");
				std::cout << token << "\n";
				std::cout << "=\n";
				token = std::strtok(nullptr, ";");
				while (token)
				{
					std::cout << token << '\n';
					token = std::strtok(nullptr, ";");
				}
                if_env_printed[i] = true;
            }
        }
        i++;
        env++;
    }
    return if_found;
}

int main(const int argc, const char *const *const argv, char **env)
{
    const auto [bitfield, args_index] = bitfield_options(argc, argv);
    const int arguments = argc - args_index;
    const size_t env_variavbles = count_env_variables(env);

    if (arguments && env_variavbles)
    {
        bool *if_printed_env = new bool[env_variavbles];
        memset(if_printed_env, 0, env_variavbles);
        bool *if_printed_arg = new bool[arguments];

        for (int i = 0; i < arguments; i++)
            if_printed_arg[i] = split_and_print(argv[i + args_index], env, if_printed_env);

        if (!(bitfield & SILENT_MODE))
            for (int i = 0; i < arguments; i++)
                if (!if_printed_arg[i])
                    std::cout << argv[args_index + i] << "=NONE\n";

        delete[] if_printed_env;
        delete[] if_printed_arg;
    }
}
