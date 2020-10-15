#include <string>
using namespace std;

bool isSilent(char* ctab[])
{
    while (*ctab != NULL)
        if (*ctab++ == (string)"/S")
            return true;

    return false;
}

bool isInTab(char* ctab[], char* substring)
{
    while (*ctab != NULL){
        if (strstr(*ctab, substring))
            return true;

        (*ctab++);
    }
    return false;
}

int main(int argc, char* argv[], char* env[])
{
    if (!isSilent(argv))
        for (int i = 1; i < argc; i++) {
            if (!isInTab(env, argv[i])) {
                string message = string(argv[i]) + "=NONE";
                puts(message.c_str());
            }
        }

    while (*env != NULL) {
        for (int i = 1; i < argc; i++) {
            if (strstr(*env, argv[i])) {
                char* token;
                char* rest = *env;

                token = strtok_s(rest, "=", &rest);
                if (strstr(token, argv[i])) {
                    puts(token);
                    puts("=");
                    while ((token = strtok_s(rest, ";", &rest)))
                        puts(token);
                    puts("");
                }
            }
        }
        (*env++);
    }

    return 0;
}