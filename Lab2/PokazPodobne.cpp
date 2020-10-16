#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

namespace
{
    const std::string no_var_value = "NONE";
}

bool is_silent(std::string token)
{
    const std::string lowercase_silent_switch = "/s";
    const std::string upperrcase_silent_switch = "/S";

    return token.compare(lowercase_silent_switch) == 0 || token.compare(upperrcase_silent_switch) == 0;
}

bool silencer(std::vector<std::string>& tokens)
{
    auto it = std::find_if(tokens.begin(), tokens.end(), is_silent);

    if (it != tokens.end())
    {
        tokens.erase(it);
        return true;
    }
    return false;
}

std::vector<std::string> extract_arguments(int argc, char* argv[])
{
    std::vector<std::string> args;

    for (int i = 1; i < argc; i++)
    {
        std::string token(argv[i]);
        args.push_back(token);
    }

    return args;
}

std::vector<std::pair<std::string, std::string>> extract_env_vars(char** envp)
{
    std::vector<std::pair<std::string, std::string>> env;

    for (char** str = envp; *str != 0; str++)
    {
        std::string variable(*str);
        auto split_point = variable.find_first_of("=");
        std::string name = variable.substr(0, split_point);
        std::string value = variable.substr(split_point + 1, std::string::npos);
        env.push_back(std::make_pair(name, value));
    }

    return env;
}

std::vector<std::pair <std::string, std::string> > find_matches(std::vector<std::string>& args, std::vector<std::pair<std::string, std::string> >& env, bool is_silent)
{
    std::vector<std::pair<std::string, std::string> > matches;

    for (auto& arg : args)
    {
        bool found_match = false;
        for (auto& var : env)
        {
            if (var.first.find(arg) != std::string::npos)
            {
                found_match = true;
                matches.push_back(var);
            }
        }
        if (!found_match && !is_silent)
        {
            matches.push_back(std::make_pair(arg, no_var_value));
        }
    }
    return matches;
}

std::string parse_match_value(std::string match_value)
{
    std::string value(match_value);

    std::replace(value.begin(), value.end(), ';', '\n');

    return value;
}

void print_matches(std::vector<std::pair<std::string, std::string>>& matches)
{
    for (auto& match : matches)
    {
        std::cout << match.first << "\n=\n" << parse_match_value(match.second) << "\n\n";
    }
}

int main(int argc, char** argv, char** envp)
{
    bool is_silent = false;

    std::vector<std::pair <std::string, std::string> > env = extract_env_vars(envp);
    std::vector<std::string> args = extract_arguments(argc, argv);

    is_silent = silencer(args);

    std::vector<std::pair <std::string, std::string> > matches = find_matches(args, env, is_silent);

    print_matches(matches);
}
