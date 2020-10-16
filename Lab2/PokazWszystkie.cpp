#include <iostream>

void print(char** to_print)
{
    for (char** str = to_print; *str != 0; str++)
        printf("%s\n", *str);
}

int main(int argc, char** argv, char** envp)
{
    print(argv);
    print(envp);
    return 0;
}
