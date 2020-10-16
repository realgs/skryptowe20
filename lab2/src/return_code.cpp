#include <iostream>
#include "input_switches.hpp"

// return codes
constexpr int NO_PARAMETERS = 11;
constexpr int NOT_A_DIGIT = 12;
constexpr int TWO_OR_MORE_PARAMETERS = 13;

const char *const RETURN_MESSAGE = "Return code: %d\n";

int main(const int argc, const char *const *const argv)
{
    const auto [bitfield, args_index] = bitfield_options(argc, argv);

    int arguments = argc - args_index;

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
