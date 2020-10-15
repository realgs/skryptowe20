
#include <iostream>
using namespace std;


int main(int argc, char* argv[], char* envp[]) 
{
	bool silent = false;
	if(argc > 1) if(string(argv[1]) == "/s" || string(argv[1]) == "/S")silent = true;
	for (int i = 1; i < argc; i++) 
	{
		bool none = true;
		if (i == 1 && silent) continue;
		string str = string(argv[i]);
		int j = 0;
		while(envp[j]!=nullptr)
		{
			string var = envp[j];
			if (var.find(str) != string::npos)
			{
				none = false;
				cout <<endl << var.substr(0, var.find("=")) << endl << "=\n";
				int start = var.find("=") + 1;
				while (start < var.length()) {
					int next = var.find(';',start);
					if (next != string::npos) {
						cout << var.substr(start, next+1-start) << endl;
						start = next + 1;
					}
					else {
						cout << var.substr(start) << endl;
						start = var.length();
					}
				}
			}
			j++;
		}
		if (!silent && none) cout << endl << str << "=NONE\n";
	}
}

