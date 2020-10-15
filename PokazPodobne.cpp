#include <iostream>
#include <string>
#include <vector>

bool silent(int count, char** args) {
	for (int i = 1; i < count; i++) {
		if (strcmp(args[i], "/S") == 0) return true;
	}
	return false;
}

int main(int argc, char* argv[], char* env[])
{
	std::string envVar;
	char delimiterEquals = '=';
	char delimiterSemicolon = ';';
	std::vector<char*> envCopy;
	bool isSilent = silent(argc, argv);

	while (*env != NULL) {
		envCopy.push_back(*env++);
	}

	for (int k = 1; k < argc; k++) {
		bool foundOne = false;
		for(int j = 0; j < envCopy.size(); j++){
			envVar = envCopy[j];
			int pos = 0;
			std::size_t found = envVar.find(argv[k]);
			if (found != std::string::npos) {
				foundOne = true;
				for (int i = 0; i < envVar.size(); i++) {
					if (envVar[i] == delimiterEquals) {
						std::cout << envVar.substr(pos, i++) << "\n" << "=" << "\n";
						pos = i;
					}
					else if (envVar[i] == delimiterSemicolon) {
						std::cout << envVar.substr(pos, i - pos) << "\n";
						pos = ++i;
					}
				}
				std::cout << envVar.substr(pos) << "\n";
			}
		}
		if (!foundOne && !isSilent) std::cout << argv[k] << "=NONE";
	}
}
