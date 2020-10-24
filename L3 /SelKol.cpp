#include <iostream>
#include <vector>
using std::cin, std::cout, std::endl, std::string, std::vector, std::stoi;

int main(int argc, const char * argv[])
{
	vector<string> values;
	string input = "\t";
	getline(cin, input);

	while (input != "" && !cin.eof())
	{
		long position = input.find('\t');

		while (position != string::npos)
		{
			values.push_back(input.substr(0, position));
			input = input.substr(position + 1);
			position = input.find('\t');
		}
		values.push_back(input);

		for (int i = 1; i < argc; i++)
		{
			try
			{
				int column = stoi(argv[i]) - 1;

				if(column >= 0 && column < values.size())
					cout << values[column] << '\t';
				else
					cout << "invalid column\t";
			}
			catch (std::invalid_argument error) { cout << "invalid column\t"; }
		}

		cout << endl;
		values.clear();
		getline(cin, input);
	}

	return 0;
}
