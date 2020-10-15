#include <iostream>

const char separator = '=';
const char delimeter = ':';

bool isSilent(char* argtab[])
{
    std::string arg;
    while (*argtab != nullptr)
    {
        arg = *argtab++;
        if (arg == "-s" || arg == "-S")
        {
            return true;
        }
    }
    return false;
}

void printVar(std::string &variableName, std::string &variableData){
    std::cout << "\ni. " + variableName << std::endl;
    std::cout << "ii. =" << std::endl;
    std::cout << "iii. ";
    char * token;
    char* rest = &variableData[0];

    while ((token = strtok_r(rest, &delimeter, &rest)))
        printf("%s\n", token);
}

int main(int argc, char* argv[], char* envp[]){
    int pos = 1;
    bool silent = isSilent(argv);
    bool varFound;

    if (silent) {
        pos++;
    }

  for (int i = pos; i < argc; i++) {
          varFound = false;
          std::string argument(argv[i]);
          char **envp_cp = envp;
          while (*envp_cp) {
              std::string variable(*envp_cp++);
              size_t index = variable.find(separator);
              std::string varName = variable.substr(0, index);
              variable.erase(0, index + 1);
              if (varName.find(argument) != std::string::npos) {
                  printVar(varName, variable);
                  varFound = true;
              }
          }
          if(!silent && !varFound)
            std::cout<< argument << "= NONE"<<std::endl;

  }
  return 0;
}
