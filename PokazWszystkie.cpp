#include <iostream>

int main(int argc, char* argv[], char* env[])
{
    printf("Arugemtny programu:\n\n");
    for (int i = 0; i < argc; i++) {
        printf("%s\n", argv[i]);
    }
    printf("\n\nZmienne srodowiskowe:\n\n");
    while (*env != NULL)
    {
        printf("%s\n", *env++);
    }
    return 0;
}
