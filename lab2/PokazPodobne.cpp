#include <iostream>

using namespace std;

bool isSilent(char* param)
{
	if (param[0] == '\\' && (param[1] == 's' || param[1] == 'S') && param[2] == NULL) {
		return true;
	}
	else {
		return false;
	}
}

int main(int argc, char* argv[], char* env[])
{
    bool isSilentP = false;
	char* param = nullptr;
    for (int i = 0; i < argc; i++) {
        if (isSilent(argv[i])) {
            isSilentP = true;
        }
        else {
			param = argv[i];
        }
    }

	int i = 0;
	bool isThereParameter = false;
	while (env[i] != nullptr) {	
		string tekst = string(env[i]);
		if (!tekst.find(string(param))) {
			isThereParameter = true;
			int j = 0;
			while (tekst[j] != NULL) {
				if (tekst[j] == ';') {
					cout << "\n\t";
				}
				else {
					cout << tekst[j];
				}
				j++;
			}
			cout << endl;
		}
		
		i++;
	}
	if (!isThereParameter && !isSilentP) {
		cout << param << " = NONE" << endl;
	}
	return 0;
}
