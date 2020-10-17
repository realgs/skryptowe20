#include <iostream>
#if defined(unix) || defined(__unix__) || defined(__unix)
#define PRINT_COMMAND "env"
#else
#define PRINT_COMMAND "set"
#endif

int main(int argc, char** argv) {
    std::cout << "___PROGRAM ARGUMENTS___\n " << std::endl;
    for (auto i = 0; i < argc; i++)
        puts(argv[i]);

    std::cout << "\n___ENV VARIABLES___\n " << std::endl;
    system(PRINT_COMMAND);

    return 0;
}
