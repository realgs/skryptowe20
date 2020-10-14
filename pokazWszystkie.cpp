#include <iostream>

int main(int argc, char **argv, char **envp) {
    puts("Argumenty programu (wraz z nazwą pliku): ");
    for (int i = 0; i < argc; i++)
        puts(argv[i]);

    puts("\nZmienne środowiskowe: ");
    while (*envp)
        puts(*envp++);

    return 0;
}