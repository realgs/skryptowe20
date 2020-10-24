#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;


int main(int argc, char* argv[], char* env[]) {
	
	string inp;
	
	while (getline(cin, inp)) {
			
		vector<string> out;

		string tok;
		istringstream tokenStream(inp);

		while (getline(tokenStream, tok, '\t'))
		{
			out.push_back(tok);
		}

		bool lookFor = false;

		for (int i = 1; i < argc; i++) {
			
			for (size_t j = 0; j < out.size(); j++) 
				if ((string)argv[i] == out[j])
					lookFor = true;		
		}
		if (lookFor) 
			cout << inp << '\n';
	}
}
