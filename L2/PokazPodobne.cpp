
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
                string msgnot = string(argv[i]) + "=NONE";
                puts(msgnot.c_str());
            }
        }


        while (*env != NULL)
        {
            bool put = false;
            for (int i = 1; i < argc; i++)
            {
                if (!put && strstr(*env, argv[i]))
                {
                    put = true;
                    char* text;
                    char* part = *env;

                    while ((text = strtok_s(part, ";", &part))) puts(text);
                }
            }
            (*env++);
        }
    }

    return 10;
}

