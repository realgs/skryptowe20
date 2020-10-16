#include <utility>
#include <cstring>
#include <vector>
#include <string>
#include <iostream>

std::pair<bool, int> isSilence(int argc, char* argv[]) {
	bool isSilence = false;
	int silenceIndex = 0;

	for (int i = 1; i < argc; i++) {
		if (strcmp(argv[i], "/s") == 0 || strcmp(argv[i], "/S") == 0) {
			isSilence = true;
			silenceIndex = i;
		}
	}

	return std::make_pair(isSilence, silenceIndex);
}

std::pair<std::vector<std::string>, std::vector<std::string>> splitEnv(char* env[]) {
	std::vector<std::string> envNames;
	std::vector<std::string> envContent;

	for (; *env; env++) {
		for(auto cPtr = env[0]; *cPtr; cPtr++) {
			if(*cPtr==';') {
				*cPtr = '\n';
			}
		}
		std::string envString = std::string(*env);
		int presentIndex = envString.find('=');
		envNames.push_back(envString.substr(0, presentIndex));
		envContent.push_back(envString.substr(presentIndex+1));
	}
	return std::make_pair(envNames, envContent);
}

bool doesEnvContainArg(std::vector<std::pair<char*, bool>>& argv, const std::string& env) {
	bool doesContain = false;

	for (auto &arg : argv) {
		if (env.find(arg.first) != std::string::npos) {
			doesContain = true;
			arg.second = true;
		}
	}

	return doesContain;
}

std::pair<std::vector<int>, std::vector<char*>> selectEnvs(int argc, char* argv[],
                                                           std::vector<std::string> envNames, bool isSilence,
                                                           int silenceIndex) {
	std::vector<int> selectedEnvs;
	std::vector<std::pair<char*, bool>> argvVector;

	for (int i = 1; i < argc; i++) {
		if (!isSilence || i != silenceIndex) {
			argvVector.push_back(std::make_pair(argv[i], false));
		}
	}

	for (int i = 0; i < envNames.size(); i++) {
		if (doesEnvContainArg(argvVector, envNames[i])) {
			selectedEnvs.push_back(i);
		}
	}

	std::vector<char*> notUsedArgs;
	for (auto arg : argvVector) {
		if (!arg.second) {
			notUsedArgs.push_back(arg.first);
		}
	}

	return std::make_pair(selectedEnvs, notUsedArgs);
}

void printResult(std::pair<std::vector<std::string>, std::vector<std::string>> splitedEnv,
                 std::pair<std::vector<int>, std::vector<char*>> selectedEnvs, bool isSilence) {
	for (int i : selectedEnvs.first) {
		std::cout << splitedEnv.first[i] << "\n=\n";
		std::cout << splitedEnv.second[i] << "\n\n";
	}

	if(!isSilence) {
		for (auto notUsedArg : selectedEnvs.second) {
			std::cout << notUsedArg<<" = NONE\n";
		}
	}
}

int main(int argc, char* argv[], char* env[]) {
	auto silenceMode = isSilence(argc, argv);
	auto splitedEnv = splitEnv(env);
	auto selectedEnvs = selectEnvs(argc, argv, splitedEnv.first, silenceMode.first, silenceMode.second);
	printResult(splitedEnv, selectedEnvs, silenceMode.first);
}
