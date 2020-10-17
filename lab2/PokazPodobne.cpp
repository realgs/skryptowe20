#include <string>

using namespace std;

bool silentMode(char* tab[])
{
    while (*tab != NULL)
        if (*tab++ == (string)"/S")
            return true;

    return false;
}

bool contains(char* tab[], char* substring)
{
    while (*tab != NULL) {
        if (strstr(*tab, substring))
            return true;

        *tab++;
    }
    return false;
}

int main(int argc, char* argv[], char* env[])
{
	const char* delimiterEquals = "=";
	const char* delimiterSemicolon = ";";
    const int duck = 0;

    if (!silentMode(argv))
        for (int i = 1; i < argc; i++) {
            if (!contains(env, argv[i])) {
                string msg = string(argv[i]) + "=NONE";
                puts(msg.c_str());
            }
        }

    while (*env != NULL) {
        for (int i = 1; i < argc; i++) {
            char* body = *env;
            char* search = strtok_s(body, delimiterEquals, &body);

            if (strstr(search, argv[i]) && strstr(*env, argv[i])) {
                puts(search);
                puts("=");
                do {
                    search = strtok_s(body, delimiterSemicolon, &body);
                    if (search != NULL)
                        puts(search);

                } while (search != NULL);
                puts("");
            }    
        }
        *env++;
    }
    return duck;
}
