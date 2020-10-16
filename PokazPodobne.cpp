#include <iostream>
#include <cstring>

bool isSilent(char* argv[]) {
	while(*argv != nullptr) {
		std::string arg = *argv++;
		if (arg == "/s" || arg == "/S")
			return true;
	}
	return false;
}

bool contains(char* tab[], char* substr) {
  while (*tab != nullptr) {
    if (strstr(*tab, substr)) {
        return true;
    }
    *(tab++);
  }
  return false;
}

int main(int argc, char* argv[], char* env[]) {
  std::cout << "Environment variables\n";

  for (int i = 1; i < argc; i++) {
    if (!contains(env, argv[i]) && !isSilent(argv)) {
      std::string msgNone = std::string(argv[i]) + "=NONE\n";
      std::cout << msgNone.c_str();
    }
  }

  while (*env != nullptr) {
    bool printed = false;
    for (int i = 1; i < argc; i++) {
      if (!printed && std::strstr(*env, argv[i])) {
        printed = true;
        char* part = *env;
        char* text = std::strtok(part, ";");

        while (text) {
          std::cout << text << "\n";
          text = std::strtok(nullptr, ";");
        }
      }
    }
    (*env++);
  }

  return 10;
}
