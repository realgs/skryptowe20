
#include <iostream>
using namespace std;
bool isSilent(char* tab[])
{
	string argument;
	while (*tab != NULL)
	{
		argument = *tab++;
		if (argument == "/S" || argument == "/s")
		{
			return true;
		}
	}
	return false;
}

bool tabContains(char* ctab[], char* substring)
{
    while (*ctab != NULL)
    {
        if (strstr(*ctab, substring))
        {
            return true;
        }
        (*ctab++);
    }
    return false;
}

int main(int argc, char* argv[], char* env[])
{
    puts("Environment variables");
    if (!isSilent(argv))
    {
        for (int i = 1; i < argc; i++)
        {
            if (!tabContains(env, argv[i]))
            {
                string message = string(argv[i]) + "=NONE";
                puts(message.c_str());
            }
        }
    }

    while (*env != NULL)
    {
        bool written = false;
        for (int i = 1; i < argc; i++)
        {
            if (strstr(*env, argv[i]) && !written)
            {
                written = true;
                char* token;
                char* rest = *env;

                while ((token = strtok_s(rest, ";", &rest)))
                {
                    puts(token);
                }
            }
        }
        (*env++);
    }

    return 0;
}

