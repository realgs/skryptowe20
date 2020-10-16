#include <tuple>
#include <string>
#include <unordered_map>

const char SWITCH_INDICATOR = '/';

const uint8_t SILENT_MODE = 0x01 << 0;

// used to get bitfiels from switches
inline const std::unordered_map<char, uint8_t> switches{
    {'s', SILENT_MODE},
};

uint8_t get_bitfield_option(const char option)
{
    auto bit_value = switches.find(option);
    return bit_value == switches.end() ? 0 : bit_value->second;
}

// get bitfield from flags
// return also first index that is a parameter and not a switch
std::tuple<uint8_t, int> bitfield_options(const int argc, const char *const *const argv)
{
    uint8_t bitfield = 0;
    // start with 1 - ignore the app name
    int count = 1;
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
