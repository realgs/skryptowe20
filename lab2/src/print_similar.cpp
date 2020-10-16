#include <string>
#include <iostream>

void split_and_print(const int argc, const char *const *const argv, char *env_var)
{
    for (int i = 1; i < argc; i++)
    {
        if (std::strstr(env_var, argv[i]))
        {
            char *token = std::strtok(env_var, "=");
            std::cout << token << "\n";
            std::cout << "=\n";
            token = std::strtok(nullptr, ";");
            while (token)
            {
                std::cout << token << '\n';
                token = std::strtok(nullptr, ";");
            }
            return;
        }
    }
}

int main(const int argc, const char *const *const argv, char **env)
{
    while (*env != nullptr)
        split_and_print(argc, argv, *env++);
}