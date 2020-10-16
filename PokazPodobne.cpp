#include <iostream>
#include <vector>

void  print_environment_variable(std::string name, std::string content) {
    std::cout << "\n" << name << "\n" << "=\n";
    for (int i = 0; i < content.length(); i++)
    {
        if (content[i] == ';') {
            printf("\n");
            if (content[i + 1] == ';') i++;
        }
        else printf("%c", content[i]);
    }
    printf("\n\n");
}

int main(int argc, char* argv[], char* env[])
{
    bool isSilent = false;
    if (argc >= 2)
    {
        for (int i = 1; i < argc; i++) {
            std::string arg = argv[i];
            if (((argv[i][0] == '/' && argv[i][1] == 'S') || 
                (argv[i][0] == '/' && argv[i][1] == 's')) && arg.length() == 2) isSilent = true;
        }
    }

    std::vector<bool> isThereAnyVariable(0);
    const int INDEX_OFFSET = 1;
    for (int i = 1; i < argc; i++) isThereAnyVariable.push_back(false);

    while (*env != NULL)
    {
        std::string text = std::string(*env);
        for (int i = 1; i < argc; i++) {
            std::string arg = std::string(argv[i]);
            if (!text.find(arg)) {
                isThereAnyVariable[i - INDEX_OFFSET] = true;
                std::string text_content = text.substr(text.find("=") + 1, text.length());
                print_environment_variable(arg, text_content);
            }
        }
        *env++;
    }

    if(!isSilent){
        for (int i = 0; i < isThereAnyVariable.size(); i++)
        {
            if (!isThereAnyVariable[i]) {
                std::cout << argv[i + INDEX_OFFSET] << " = NONE" << std::endl;
            }
        }
    }

    return 0;
}
