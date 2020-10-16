#include <iostream>
#include <vector>
#include <string>

const std::string lowercase_silent_switch = "/s";
const std::string upperrcase_silent_switch = "/S";

const int error_no_args = 11;
const int error_not_a_digit = 12;
const int error_too_many_args = 13;

bool is_silent(std::string token)
{
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

bool is_digit(std::string token)
{
    if (token.size() == 1)
        return isdigit(token[0]);
    return false;
}

void tokenize(int argc, char* argv[], std::vector<std::string>& tokens)
{
    for (int i = 1; i < argc; i++)
    {
        std::string token(argv[i]);
        tokens.push_back(token);
    }
}

int convert_digit(std::string possibly_digit)
{
    if (is_digit(possibly_digit))
        return (possibly_digit[0]) - '0';
    else
        return error_not_a_digit;
}

int determine_output(std::vector<std::string>& tokens)
{
    if (tokens.size() == 0)
        return error_no_args;
    else if (tokens.size() == 1)
        return convert_digit(tokens.back());
    else
        return error_too_many_args;
}

int main(int argc, char* argv[])
{
    int output = 0;
    bool isSilent = false;
    std::vector<std::string> tokens;

    tokenize(argc, argv, tokens);
    isSilent = silencer(tokens);
    output = determine_output(tokens);

    if (!isSilent) std::cout << output;

    return output;
}
