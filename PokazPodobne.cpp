#include <iostream>
#include <vector>

void  showMatched(std::string var, std::string con) {
    std::cout << "\n" << var << "\n" << "=\n";
    for (int i = 0; i < con.length(); i++)
    {
        if (con[i] == ';') {
            printf("\n");
        }
        else printf("%c", con[i]);
    }
    printf("\n\n");
}

int main(int argc, char* argv[], char* env[]){
    int argOffset = 1;
    bool isSilent = false;
    if (argc >= 2) {
        for (int i = 1; i < argc; i++) {
            std::string silentString = argv[i];
            if (((argv[i][0] == '/' && argv[i][1] == 'S') || (argv[i][0] == '/' && argv[i][1] == 's')) && silentString.length() == 2) {
                isSilent = true;
            }
        }
    }

    bool* zeroMatches = new bool[argc];
    for (int i = 1; i < argc; i++) 
        zeroMatches[i] = false;
    
    while (*env != NULL)
    {
        std::string envText = std::string(*env);
        for (int i = 1; i < argc; i++) {
            std::string argText = std::string(argv[i]);
            if (!envText.find(argText)) {
                zeroMatches[i - argOffset] = true;
                std::string text_content = envText.substr(envText.find("=") + 1, envText.length());
                showMatched(argText, text_content);
            }
        }
        *env++;
    }

    if(!isSilent){
        for (int i = 1; i < argc; i++){
            if (!zeroMatches[i]) {
                std::cout << argv[i + argOffset] << " = NONE" << std::endl;
            }
        }
    }
    delete zeroMatches;
}
