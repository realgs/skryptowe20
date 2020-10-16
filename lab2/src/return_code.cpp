#include <iostream>
#include <string>
#include <cstdlib>
#include <tuple>
#include <unordered_map>

// return codes
constexpr int NO_PARAMETERS = 11;
constexpr int NOT_A_DIGIT = 12;
constexpr int TWO_OR_MORE_PARAMETERS = 13;

const char *const RETURN_MESSAGE = "Return code: %d\n";
const char SWITCH_INDICATOR = '/';

const uint8_t SILENT_MODE = 0x01 << 0;

// used to get bitfiels from switches
const std::unordered_map<char, uint8_t> switches{
    {'s', SILENT_MODE},
};

uint8_t get_bitfield_option(const char option)
{
    auto bit_value = switches.find(option);
    return bit_value == switches.end() ? 0 : bit_value->second;
}

// get bitfield from flags
// return also first index that is a parameter and not a switch
std::tuple<uint8_t, size_t> bitfield_options(const int argc, const char *const *const argv)
{
    uint8_t bitfield = 0;
    // start with 1 - ignore the app name
    size_t count = 1;
    // iterate as long as parameters start with / - rest are parameters
    if (argc > 1)
    {
        while (count < argc && argv[count][0] == SWITCH_INDICATOR)
        {
            size_t flags_length = strlen(argv[count]);
            for (size_t i = 1; i < flags_length; i++)
                bitfield |= get_bitfield_option(std::tolower(argv[count][i]));

            count++;
        }
    }
    return std::tuple(bitfield, count);
}

int main(const int argc, const char *const *const argv)
{
    const auto [bitfield, args_index] = bitfield_options(argc, argv);

    size_t arguments = static_cast<size_t>(argc) - args_index;

    if (!arguments)
    {
        if (!(bitfield & SILENT_MODE))
            std::printf(RETURN_MESSAGE, NO_PARAMETERS);
        return NO_PARAMETERS;
    }

    if (arguments > 1)
    {
        if (!(bitfield & SILENT_MODE))
            std::printf(RETURN_MESSAGE, TWO_OR_MORE_PARAMETERS);
        return TWO_OR_MORE_PARAMETERS;
    }

    // there is only one argument and it's index is argc - 1
    if (std::strlen(argv[argc - 1]) == 1 && std::isdigit(argv[argc - 1][0]))
    {
        const int exit_code = argv[argc - 1][0] - '0';
        if (!(bitfield & SILENT_MODE))
            std::printf(RETURN_MESSAGE, exit_code);
        return  exit_code;
    }

    // it was not a digit
    if (!(bitfield & SILENT_MODE))
        printf(RETURN_MESSAGE, NOT_A_DIGIT);
    return NOT_A_DIGIT;
}