#include <iostream>
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

		for (int k = 1; k < argc; k++)
		{
			int val = atoi(argv[k]);

			if (val <= out.size() && val > 0)
				cout << out.at(val - 1) << '\t';

		}
		cout << "\n";
	}
}
