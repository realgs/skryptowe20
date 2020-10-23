// zadanie 1
#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>

static int constexpr NOT_ENOUGHT_ARGUMENTS = 1;
static int constexpr ARGUMENT_NOT_A_NUMBER = 2;

bool if_positive_int(char const *const number)
{
    size_t len = std::strlen(number);
    for (size_t i = 0; i < len; i++)
        if (!std::isdigit(number[i]))
            return false;

    return true;
}

std::vector<std::string> split_into_words(std::string input)
{
    std::istringstream iss(input);
    return std::vector<std::string>((std::istream_iterator<std::string>(iss)), std::istream_iterator<std::string>());
}

int main(int const argc, char const *const *const argv)
{
    // at least one colum needs to be selected
    if (argc < 2)
    {
        std::cout << "Not enought arguments";
        exit(NOT_ENOUGHT_ARGUMENTS);
    }

    std::vector<int> columns;
    columns.reserve(argc - 1);

    for (int i = 1; i < argc; i++)
        if (!if_positive_int(argv[i]))
        {
            std::cout << "It's not a valid digit: " << argv[i];
            exit(ARGUMENT_NOT_A_NUMBER);
        }
        else
        {
            columns.push_back(std::atoi(argv[i]));
        }

    std::string line;
    while (std::getline(std::cin, line))
    {
        auto const words = split_into_words(line);
        for (int const column : columns)
        {
            if (static_cast<size_t>(column) < words.size())
                std::cout << words[column] << '\t';
        }
        std::cout << '\n';
    }
}
